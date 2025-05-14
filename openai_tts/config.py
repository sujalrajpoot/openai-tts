"""Configuration classes for TTS functionality."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import List
import os

class VoiceType(Enum):
    """Enumeration of available voice types for text-to-speech."""
    ALLOY = "alloy"
    ASH = "ash"
    BALLAD = "ballad"
    CORAL = "coral"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SAGE = "sage"
    SHIMMER = "shimmer"
    VERSE = "verse"

    @classmethod
    def get_voice_names(cls) -> List[str]:
        """Get list of all available voice names."""
        return [voice.name for voice in cls]

@dataclass
class TTSConfig:
    """Configuration class for Text-to-Speech settings."""
    timeout: int = 30
    verbose: bool = True
    output_path: str = os.path.join(os.getcwd(), "output.mp3")
    voice: VoiceType = VoiceType.SHIMMER
