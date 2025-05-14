"""OpenAI TTS provider implementation."""

import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Union, List, Generator, AsyncGenerator
from typing_extensions import TypeAlias

import requests

from openai_tts.config import TTSConfig, VoiceType
from openai_tts.exceptions import TTSException, TTSRequestError
from openai_tts.providers.base import TTSProvider
from openai_tts.utils import split_into_sentences


class OpenaiTTS(TTSProvider):
    """OpenAI TTS implementation using the openai.fm API."""

    def __init__(self, config: Optional[TTSConfig] = None):
        """
        Initialize OpenAI TTS provider.
        
        Args:
            config (Optional[TTSConfig]): Configuration settings. Defaults to TTSConfig().
        """
        self.config = config or TTSConfig()
        self._setup_session()

    def _setup_session(self) -> None:
        """Set up the HTTP session with required headers."""
        self.PROVIDER_URL: str = "https://www.openai.fm/api/generate"
        self.session = requests.Session()
        self.session.headers.update({
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,hi;q=0.8",
            "dnt": "1",
            "origin": "https://www.openai.fm",
            "referer": "https://www.openai.fm/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        })

    def _generate_audio_chunk(self, text: str, chunk_number: int) -> tuple[int, bytes]:
        """
        Generate audio for a single text chunk.

        Args:
            text (str): The text chunk to convert.
            chunk_number (int): The sequence number of the chunk.

        Returns:
            tuple[int, bytes]: Chunk number and audio data.

        Raises:
            TTSRequestError: If the request fails.
        """
        payload = {
            'input': text,
            'prompt': 'Standard clear voice.',
            'voice': self.config.voice.value,
            'vibe': 'null'
        }

        while True:
            try:
                response = self.session.post(
                    self.PROVIDER_URL,
                    data=payload,
                    timeout=self.config.timeout
                )
                response.raise_for_status()

                if response.content:
                    if self.config.verbose:
                        print(f"Chunk {chunk_number} processed successfully.")
                    return chunk_number, response.content

                if self.config.verbose:
                    print(f"No data received for chunk {chunk_number}.")

            except requests.RequestException as e:
                if self.config.verbose:
                    print(f"Error processing chunk {chunk_number}: {e}")
                raise TTSRequestError(f"Failed to generate audio for chunk {chunk_number}: {e}")

            time.sleep(1)

    def speak(
        self,
        text: str,
        voice: Optional[VoiceType] = None,
        output_path: Optional[Union[str, Path]] = None,
        verbose: Optional[bool] = None,
        config: Optional[TTSConfig] = None
    ) -> str:
        """
        Convert text to speech using OpenAI TTS.

        Args:
            text (str): The text to convert to speech.
            voice (Optional[VoiceType]): Optional voice override.
            output_path (Optional[Union[str, Path]]): Optional output file path.
            verbose (Optional[bool]): Optional verbosity override.
            config (Optional[TTSConfig]): Optional configuration override.

        Returns:
            str: Path to the generated audio file.

        Raises:
            TTSException: If conversion fails.
        """
        current_config = config or self.config

        if voice is not None or output_path is not None or verbose is not None:
            current_config = TTSConfig(
                timeout=current_config.timeout,
                voice=voice or current_config.voice,
                output_path=Path(output_path) if output_path else current_config.output_path,
                verbose=verbose if verbose is not None else current_config.verbose
            )

        assert isinstance(current_config, TTSConfig), "config must be an instance of TTSConfig"
        assert current_config.voice in VoiceType, f"Voice must be one of {VoiceType.get_voice_names()}"

        sentences = split_into_sentences(text)

        try:
            with ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(self._generate_audio_chunk, sentence.strip(), i): i
                    for i, sentence in enumerate(sentences, start=1)
                }

                audio_chunks: Dict[int, bytes] = {}

                for future in as_completed(futures):
                    chunk_num = futures[future]
                    try:
                        part_number, audio_data = future.result()
                        audio_chunks[part_number] = audio_data
                    except Exception as e:
                        if verbose:
                            print(f"Failed to generate audio for chunk {chunk_num}: {e}")

                output_file = Path(current_config.output_path)
                with output_file.open('wb') as f:
                    for chunk_num in sorted(audio_chunks.keys()):
                        f.write(audio_chunks[chunk_num])

                if current_config.verbose:
                    print(f"Audio saved to {output_file}")
                return str(output_file)

        except Exception as e:
            raise TTSException(f"Failed to generate audio: {e}")
