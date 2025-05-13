"""Exception classes for TTS functionality."""


class TTSException(Exception):
    """Base exception class for TTS-related errors."""
    pass


class TTSRequestError(TTSException):
    """Exception raised when there's an error in TTS request."""
    pass