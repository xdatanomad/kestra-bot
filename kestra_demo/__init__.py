"""
Kestra Bot Demo Package

A Textual terminal application for building Kestra ETL Flows using OpenAI agents.
"""

__version__ = "0.1.0"
__author__ = "Parham Parvizi"
__email__ = "parham.parvizi@gmail.com"

from .app import KestraBotApp, run_app

__all__ = ["KestraBotApp", "run_app"]