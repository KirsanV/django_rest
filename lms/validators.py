from django.core.exceptions import ValidationError
from urllib.parse import urlparse


def validate_youtube_url(value):
    if value in (None, ""):
        return value

    try:
        result = urlparse(value)
        if not result.scheme or not result.netloc:
            raise ValidationError(
                "Некорректная ссылка. Укажите полный URL (например, https://www.youtube.com/...)"
            )

        domain = result.netloc.lower()
        if not (domain.endswith("youtube.com") or domain.endswith("youtu.be")):
            raise ValidationError(
                "Ссылка должна вести на YouTube (youtube.com или youtu.be)."
            )
    except Exception:
        raise ValidationError("Некорректная ссылка.")

    return value
