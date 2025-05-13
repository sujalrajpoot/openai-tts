"""
OpenAI TTS - A Python library for using OpenAI's text-to-speech API.
"""

from openai_tts.providers.openai import OpenaiTTS
from openai_tts.config import TTSConfig, VoiceType
from openai_tts.exceptions import TTSException, TTSRequestError

__all__ = ['OpenaiTTS', 'TTSConfig', 'VoiceType', 'TTSException', 'TTSRequestError']