# 🎙️ openai-tts

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![Status](https://img.shields.io/badge/status-alpha-orange.svg)

A powerful and easy-to-use Python library for generating natural-sounding speech using OpenAI's text-to-speech capabilities.

## ✨ Features

- 🔊 Convert text to high-quality speech using OpenAI's TTS API
- 🎭 Multiple voice options (Alloy, Echo, Fable, Onyx, Nova, Shimmer)
- 🚀 Concurrent processing for faster generation of audio files
- 🧩 Modular and extensible architecture for adding new providers
- 📝 Intelligent sentence splitting for natural-sounding speech
- 🛠️ Comprehensive error handling and retry mechanism

## 🚨 Disclaimer

**IMPORTANT**: This library is developed for **educational and research purposes only**. It is not affiliated with, endorsed by, or connected to OpenAI in any way. Using this library to circumvent API restrictions, terms of service, or to access services without proper authorization may violate OpenAI's terms of service. 

The developers of this library are not responsible for any misuse or violations of terms of service that may result from using this code. Users are solely responsible for ensuring their use of this library complies with all applicable terms of service and laws.

## Project Structure

```
openai-tts/
├── LICENCE
├── README.md
├── requirements.txt
├── setup.py
├── example.py
├── openai_tts/
│   ├── __init__.py
│   ├── config.py
│   ├── utils.py
│   ├── exceptions.py
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base.py
└───└───└── openai.py
```

## 🛠️ Installation

**Using pip command**
```bash
pip install openai-tts
```

**Clone Locally**
```bash
git clone https://github.com/sujalrajpoot/openai-tts.git
cd openai-tts
pip install -r requirements.txt
```

## 🔍 Dependencies

- Python 3.8+
- requests

## 📋 Quick Start

```python
from openai_tts import OpenaiTTS
from openai_tts.config import VoiceType

# Initialize the TTS engine
tts = OpenaiTTS()

# Generate speech with default settings
text = "Hello world! This is a demonstration of the OpenAI TTS library."
tts.speak(text)  # Saves to default "output.mp3"

# Try different voices
tts.speak(text, voice=VoiceType.ECHO, output_path="echo_voice.mp3")
tts.speak(text, voice=VoiceType.NOVA, output_path="nova_voice.mp3")

# Control verbosity
tts.speak(text, verbose=False, output_path="quiet_output.mp3")
```

## 🎯 How It Works

The OpenAI TTS Library operates through a series of sophisticated steps:

1. **Text Preprocessing**: The input text is divided into natural sentences using our custom SentenceTokenizer, ensuring that the generated speech will sound natural with appropriate pauses.

2. **Parallel Processing**: Each sentence is processed concurrently using a thread pool, maximizing efficiency especially for longer texts.

3. **API Interaction**: The library communicates with OpenAI's TTS API, handling authentication, request formatting, and response processing.

4. **Error Handling**: Robust retry mechanisms and error handling ensure reliability even when network issues occur.

5. **Output Generation**: The audio chunks are assembled in the correct order and saved to the specified output file.

## 🌟 Voice Options

Choose from a variety of voice options:

| ALLOY | ASH | BALLAD | CORAL | ECHO | FABLE | ONYX | NOVA | SAGE | SHIMMER | VERSE |

## 📚 Advanced Usage

### Custom Configuration

```python
from openai_tts import OpenaiTTS, TTSConfig
from openai_tts.config import VoiceType

# Create custom configuration
config = TTSConfig(
    timeout=30,  # Increase timeout to 30 seconds
    verbose=True,  # Print detailed progress
    output_path="custom.mp3",  # Default output path
    voice=VoiceType.NOVA  # Default voice
)

# Initialize with custom config
tts = OpenaiTTS(config=config)

# Use the configured TTS
tts.speak("This text will be converted using the custom configuration.")

# Override specific settings for a single call
tts.speak(
    "This will use different settings just for this call.",
    voice=VoiceType.ECHO,
    output_path="override.mp3"
)
```

### Error Handling

```python
from openai_tts import OpenaiTTS
from openai_tts.exceptions import TTSException

tts = OpenaiTTS()

try:
    tts.speak("This is a test of error handling.")
except TTSException as e:
    print(f"An error occurred: {e}")
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run the tests**:
   ```bash
   python -m unittest discover
   ```
5. **Commit your changes**:
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to your branch**:
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

Please ensure your code follows the project's style guide and includes appropriate tests.

## 📊 Performance Considerations

The library is designed to handle large text inputs efficiently through parallel processing. However, very large texts may still take considerable time to process due to API rate limits and processing requirements.

For optimal performance:
- Split very large texts into reasonable chunks before processing
- Consider running resource-intensive operations in a background process
- Use the `verbose=True` option to monitor progress during long operations

## 🔒 Security

This library communicates with external services. Always be mindful of:
- The content you're sending to the API
- Where you're storing the generated audio files
- Who has access to your implementation

## 💡 Use Cases

- 🎙️ **Content Creation**: Generate voiceovers for videos, podcasts, or presentations
- 📚 **Accessibility**: Convert written content to audio for accessibility purposes
- 🤖 **Chatbots and Virtual Assistants**: Give your applications a voice
- 🎮 **Gaming**: Create dynamic dialogue for game characters
- 📱 **Mobile Apps**: Add speech capabilities to your applications

## ❓ FAQ

**Q: Is this an official OpenAI library?**  
A: No, this is an unofficial, community-developed library for educational purposes.

**Q: Do I need an OpenAI account to use this?**  
A: This library uses OpenAI's public TTS interface and does not require an API key.

**Q: Can I use this for commercial projects?**  
A: Please refer to OpenAI's terms of service regarding the usage of their TTS capabilities. This library is for educational purposes only.

**Q: How can I improve the speech quality?**  
A: Try different voices, ensure proper punctuation in your text, and break long paragraphs into natural sentences.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

🌟 If you find this library helpful, please consider starring the repository on GitHub!

📧 Questions or suggestions? Open an issue on GitHub or contact the maintainers.
