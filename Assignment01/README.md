# Automation Task - AI Content Generation System

This project implements the Athena Assignment 1: Automation Task for generating AI content from Google Sheets inputs and managing the entire workflow automatically.

## Overview

This system provides a comprehensive automation workflow that:
1. Reads input data from Google Sheets (descriptions, asset URLs, output formats, model specifications)
2. Generates content using AI models (OpenAI or Claude)
3. Stores outputs in Google Drive with systematic organization
4. Sends email and Slack notifications on completion (success or failure)
5. Logs task details in a dedicated SQLite database
6. Creates daily analytical reports with success/error rate charts

## Documentation

Detailed documentation is available in both languages:
- [English Documentation](./docs/README_en.md)
- [Vietnamese Documentation](./docs/README_vi.md)

## Project Structure

The project follows a modular design with separate components handling different aspects of the automation workflow:

```
Assignment01/
├── src/                            # Source code
│   ├── main.py                     # Main entry point
│   ├── sheets_reader.py            # Google Sheets data reader
│   ├── ai_generator.py             # AI content generator
│   ├── drive_uploader.py           # Google Drive uploader
│   ├── notifier.py                  # Email and Slack notifier
│   ├── database.py                 # Database manager
│   ├── report_generator.py         # Report generator
│   ├── chart_generator.py          # Analytics chart generator
│   └── html_report_generator.py    # HTML report generator
├── config.py                        # Configuration settings
├── requirements.txt                # Dependencies
├── docs/                           # Documentation
├── data/                           # Data storage
├── logs/                           # Log files
└── reports/                        # Generated reports
```

## Setup and Usage

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure your settings in `config.py`:
   - Add your Google Sheets ID
   - Add your Google Drive folder ID
   - Configure API keys for AI services
   - Set up email and Slack notification parameters

3. Run the automation:
   ```
   python src/main.py
   ```

For more detailed instructions, see the documentation files in the `docs` directory.
