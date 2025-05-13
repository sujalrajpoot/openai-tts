from setuptools import setup, find_packages

setup(
    name='openai-tts',
    version='1.0.0',
    description='A powerful and easy-to-use Python library for generating natural-sounding speech using OpenAI text-to-speech capabilities.',
    author='Sujal Rajpoot',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'openai-tts=openai_tts.tts:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
