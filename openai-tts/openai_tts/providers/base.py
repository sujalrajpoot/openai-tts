"""Base classes for TTS providers."""

from abc import ABC, abstractmethod
from typing import Optional

from openai_tts.config import TTSConfig


class TTSProvider(ABC):
    """Abstract base class for TTS providers."""
    
    @abstractmethod
    def speak(self, text: str, config: Optional[TTSConfig] = None) -> str:
        """Convert text to speech and save to file.
        
        Args:
            text: The text to convert to speech
            config: Configuration settings for the TTS operation
            
        Returns:
            str: Path to the generated audio file
            
        Raises:
            TTSException: If there's an error during the conversion process
        """
        pass