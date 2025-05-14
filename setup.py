from setuptools import setup, find_packages

setup(
    name='openai_tts',
    version='1.0.0',
    description='A powerful and easy-to-use Python library for generating natural-sounding speech using OpenAI text-to-speech capabilities.',
    author='Sujal Rajpoot',
    author_email="sujalrajpoot70@gmail.com",
    packages=find_packages(),
    install_requires=[
        'requests'
    ]
)
