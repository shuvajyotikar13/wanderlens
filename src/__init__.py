"""
WanderLens Core Module

This package contains the agentic orchestration logic, 
embedding generation, vector retrieval, and external API integrations 
required to power the multimodal RAG workflow.
"""

from .orchestrator import AgenticOrchestrator
from .config import Config

# Expose these classes at the module level for cleaner imports in app.py
__all__ = [
    "AgenticOrchestrator",
    "Config"
]
