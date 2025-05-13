"""OpenAI TTS provider implementation."""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Optional

import requests

from openai_tts.config import TTSConfig, VoiceType
from openai_tts.exceptions import TTSException, TTSRequestError
from openai_tts.providers.base import TTSProvider
from openai_tts.utils import split_into_sentences


class OpenaiTTS(TTSProvider):
    """OpenAI TTS implementation using the openai.fm API."""
    
    def __init__(self, config: Optional[TTSConfig] = None):
        """Initialize OpenAI TTS provider.
        
        Args:
            config: Optional configuration settings. If not provided, defaults will be used.
        """
        self.config = config or TTSConfig()
        self._setup_session()
        
    def _setup_session(self) -> None:
        """Set up the HTTP session with required headers."""
        self.PROVIDER_HEADERS: Dict[str, str] = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,hi;q=0.8",
            "dnt": "1",
            "origin": "https://www.openai.fm",
            "referer": "https://www.openai.fm/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        self.PROVIDER_URL: str = "https://www.openai.fm/api/generate"
        self.session = requests.Session()
        self.session.headers.update(self.PROVIDER_HEADERS)
        
    def _generate_audio_chunk(self, text: str, chunk_number: int) -> tuple[int, bytes]:
        """Generate audio for a single text chunk.
        
        Args:
            text: The text chunk to convert
            chunk_number: The sequence number of the chunk
            
        Returns:
            tuple[int, bytes]: Chunk number and audio data
            
        Raises:
            TTSRequestError: If the request fails
        """
        
        while True:
            try:
                payload = {
                    'input': text,
                    'prompt': 'Standard clear voice.',
                    'voice': self.config.voice.value,
                    'vibe': 'null'
                }
                print(payload)
                
                response = self.session.post(
                    self.PROVIDER_URL,
                    headers=self.PROVIDER_HEADERS,
                    data=payload,
                    timeout=self.config.timeout
                )
                response.raise_for_status()
                
                if response.content:
                    if self.config.verbose:
                        print(f"Chunk {chunk_number} processed successfully")
                    return chunk_number, response.content
                    
                if self.config.verbose:
                    print(f"No data received for chunk {chunk_number}")
                    
            except requests.RequestException as e:
                if self.config.verbose:
                    print(f"Error processing chunk {chunk_number}: {str(e)}")
                    raise TTSRequestError(f"Failed to generate audio for chunk {chunk_number}: {str(e)}")
            time.sleep(1)
            
    def speak(
        self,
        text: str,
        voice: Optional[VoiceType] = None,
        output_path: Optional[str] = None,
        verbose: Optional[bool] = None,
        config: Optional[TTSConfig] = None
    ) -> str:
        """Convert text to speech using OpenAI TTS.
        
        Args:
            text: The text to convert to speech
            voice: Optional voice type to use. If not provided, uses config voice
            output_path: Optional path to save the audio file. If not provided, uses config output_path
            verbose: Optional flag to control verbosity. If not provided, uses config verbose
            config: Optional configuration settings. If not provided, uses instance config
            
        Returns:
            str: Path to the generated audio file
            
        Raises:
            TTSException: If there's an error during the conversion process
            ValueError: If invalid parameters are provided
        """
        # Use provided config or instance config
        current_config = config or self.config
        
        # Override config values with direct parameters if provided
        if voice is not None:
            current_config = TTSConfig(
                timeout=current_config.timeout,
                verbose=current_config.verbose if verbose is None else verbose,
                output_path=current_config.output_path if output_path is None else output_path,
                voice=voice
            )
        elif any(param is not None for param in [output_path, verbose]):
            current_config = TTSConfig(
                timeout=current_config.timeout,
                verbose=verbose if verbose is not None else current_config.verbose,
                output_path=output_path if output_path is not None else current_config.output_path,
                voice=current_config.voice
            )
        
        assert isinstance(current_config, TTSConfig), "config must be an instance of TTSConfig"
        assert current_config.voice in VoiceType, f"Voice must be one of {VoiceType.get_voice_names()}"
        
        sentences = split_into_sentences(text)
        
        try:
            with ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(self._generate_audio_chunk, sentence.strip(), chunk_num): chunk_num 
                    for chunk_num, sentence in enumerate(sentences, start=1)
                }
                
                audio_chunks: Dict[int, bytes] = {}
                
                for future in as_completed(futures):
                    chunk_num = futures[future]
                    try:
                        part_number, audio_data = future.result()
                        audio_chunks[part_number] = audio_data
                    except Exception as e:
                        raise TTSException(f"Failed to generate audio for chunk {chunk_num}: {str(e)}")
                
                with open(current_config.output_path, 'wb') as f:
                    for chunk_num in sorted(audio_chunks.keys()):
                        f.write(audio_chunks[chunk_num])
                
                if current_config.verbose:
                    print(f"Audio saved to {current_config.output_path}")
                return current_config.output_path
                
        except Exception as e:
            raise TTSException(f"Failed to generate audio: {str(e)}")