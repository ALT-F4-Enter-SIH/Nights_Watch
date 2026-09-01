"""Custom exceptions used by services, translated to HTTP errors in routers."""
from __future__ import annotations


class NotFoundError(Exception):
    pass


class ValidationError(Exception):
    pass
