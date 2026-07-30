"""Simple Chinese UI strings for FastSD CPU."""

from __future__ import annotations

from frontend.i18n import zh_CN

_LOCALE = zh_CN


def tr(key: str, **kwargs) -> str:
    """Return localized text for *key*, formatting with *kwargs* when present."""
    text = _LOCALE.MESSAGES.get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text
