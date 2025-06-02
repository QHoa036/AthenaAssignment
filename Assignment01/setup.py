#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="ai_content_automation",
    version="0.1.0",
    description="Automation workflow for AI content generation",
    author="Athena Assignment",
    packages=find_packages(include=["ai_content_automation", "ai_content_automation.*"]),
    python_requires=">=3.8.0",
    install_requires=[
        "requests>=2.28.2",
        "google-api-python-client>=2.70.0",
        "google-auth>=2.16.1",
        "google-auth-httplib2>=0.1.0",
        "google-auth-oauthlib>=0.5.3",
        "matplotlib>=3.7.0",
        "numpy>=1.24.2",
        "jinja2>=3.1.2",
        "openai>=1.3.0",
        "anthropic>=0.5.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-content-automation=ai_content_automation.cli:main",
        ],
    },
)
