"""Example usage of OpenAI TTS."""

import time
from openai_tts import OpenaiTTS
from openai_tts.config import VoiceType

if __name__ == "__main__":
    start_time = time.time()
    
    tts = OpenaiTTS()
    
    text = "The sun was setting over the distant mountains, painting the sky in brilliant shades of orange and pink. Hey there! 😊 Welcome to your personalized Text-to-Speech experience with OpenAI-TTS! 🎉. This package can turn any text into a voice, just like magic! ✨."
    
    tts.speak(text, voice=VoiceType.NOVA, output_path="NOVA.mp3", verbose=True)  # All parameters
    tts.speak(text, voice=VoiceType.ALLOY, output_path="ALLOY.mp3", verbose=True)  # All parameters
    tts.speak(text, voice=VoiceType.ASH, output_path="ASH.mp3", verbose=True)  # All parameters
    tts.speak(text, voice=VoiceType.BALLAD, output_path="BALLAD.mp3", verbose=True)  # All parameters
    tts.speak(text, voice=VoiceType.CORAL, output_path="CORAL.mp3", verbose=True)  # All parameters
    tts.speak(text, voice=VoiceType.ECHO, output_path="ECHO.mp3", verbose=True)  # All parameters
    tts.speak(text, voice=VoiceType.ONYX, output_path="ONYX.mp3", verbose=True)  # All parameters
    tts.speak(text, voice=VoiceType.SAGE, output_path="SAGE.mp3", verbose=True)  # All parameters
    tts.speak(text, voice=VoiceType.SHIMMER, output_path="SHIMMER.mp3", verbose=True)  # All parameters
    tts.speak(text, voice=VoiceType.VERSE, output_path="VERSE.mp3", verbose=True)  # All parameters
    tts.speak(text, voice=VoiceType.FABLE, output_path="FABLE.mp3", verbose=True)  # All parameters
    print(f"Time Taken: {time.time() - start_time:.2f} Seconds.")
