"""OpenAI TTS provider implementation."""

import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Union, List, Generator, AsyncGenerator
from typing_extensions import TypeAlias
from uuid import uuid4

from curl_cffi import Session, exceptions

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
        self.session = Session()
        self.session.headers.update({
            'sec-ch-ua-platform': '"Windows"',
            'Referer': 'https://www.openai.fm/',
            'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
            'DNT': '1',
            'Range': 'bytes=0-',
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
        params = {
            'input': text.strip(),
            'prompt': 'Voice: High quality, crisp, clear and with full of emotions like Excitement, confusion, surprise, frustration, anger, disappointment, happiness, calmness, sarcasm, friendliness, flirtatiousness, curiosity, and more. I use my tones, inflections, and pauses to convey these emotions just like a human would.',
            'voice': str(self.config.voice.value),
            'generation': str(uuid4()),
        }

        while True:
            try:
                response = self.session.get(
                    self.PROVIDER_URL,
                    params=params,
                    timeout=self.config.timeout
                )
                response.raise_for_status()

                if response.content:
                    if self.config.verbose:
                        print(f"Chunk {chunk_number} processed successfully.")
                    return chunk_number, response.content

                if self.config.verbose:
                    print(f"No data received for chunk {chunk_number}.")

            except exceptions.RequestException as e:
                if self.config.verbose:
                    print(f"Error processing chunk {chunk_number}: {e}")
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
                    print(f"Audio saved to {output_file.absolute()}")
                return str(output_file)

        except Exception as e:
            raise TTSException(f"Failed to generate audio: {e}")
