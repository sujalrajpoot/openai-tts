"""Example usage of OpenAI TTS."""

import time
from openai_tts import OpenaiTTS
from openai_tts.config import VoiceType

if __name__ == "__main__":
    start_time = time.time()
    
    tts = OpenaiTTS()
    
    text = """The sun was setting over the distant mountains, painting the sky in brilliant shades of orange and pink. A gentle breeze rustled through the trees, carrying the sweet scent of blooming flowers. Birds sang their evening songs as they returned to their nests."Hey there! 😊 Welcome to your personalized Text-to-Speech experience with OpenAI-TTS! 🎉. This package can turn any text into a voice, just like magic! ✨. Whether you're working late 🌙, studying hard 📚, or just having fun 🕹️, this TTS is here to speak your mind—literally! 💬 Let's bring your words to life with sound 🔊. Ready? Let's talk! 🗣️"""
    
    # Example usage with different parameter combinations
    tts.speak(text)  # Uses default config
    tts.speak(text, voice=VoiceType.ECHO)  # Uses ECHO voice
    tts.speak(text, output_path="custom_output.mp3", verbose=False)  # Custom output path and verbosity
    tts.speak(text, voice=VoiceType.NOVA, output_path="nova_output.mp3", verbose=True)  # All parameters
    
    print(f"Time Taken: {time.time() - start_time:.2f} Seconds.")
