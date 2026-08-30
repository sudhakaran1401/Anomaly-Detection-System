import os
from pathlib import Path

from django.conf import settings


class SecurityService:
    """Centralized security checks for user-controlled file references."""

    @staticmethod
    def safe_basename(filename):
        if not filename:
            raise ValueError("Filename is required.")
        normalized = str(filename).replace("\\", "/")
        basename = os.path.basename(normalized)
        if basename != normalized or basename in {".", "..", ""}:
            raise ValueError("Invalid filename.")
        if any(ord(ch) < 32 for ch in basename):
            raise ValueError("Invalid filename.")
        return basename

    @staticmethod
    def is_within_media_root(path):
        try:
            candidate = Path(path).resolve()
            media_root = Path(settings.MEDIA_ROOT).resolve()
            candidate.relative_to(media_root)
            return True
        except (ValueError, OSError):
            return False
