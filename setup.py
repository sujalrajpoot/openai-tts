from setuptools import setup, find_packages

# Read the content of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='openai_tts',
    version='2.0.0',
    description='A powerful and easy-to-use Python library for generating natural-sounding speech using OpenAI text-to-speech capabilities.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sujal Rajpoot',
    author_email='sujalrajpoot70@gmail.com',
    packages=find_packages(),
    install_requires=[
        'curl-cffi',
        'future'
    ],
)

