"""Response helper utilities for future envelope standardization."""


def to_envelope(data: dict | list, message: str = "ok") -> dict:
    """Wrap arbitrary payloads in a consistent top-level structure."""
    return {"message": message, "data": data}
