# This makes the 'backend' a proper Python package
from .app import app
from .models import db

__all__ = ['app', 'db']