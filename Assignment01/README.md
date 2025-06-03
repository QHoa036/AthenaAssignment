# Automation Task - AI Content Generation System

This project implements the Athena Assignment 1: Automation Task for generating AI content from Google Sheets inputs and managing the entire workflow automatically. The system has been fully localized with Vietnamese comments, docstrings, and logger messages to support the Vietnamese development team.

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
├── src/                     # Source code (localized in Vietnamese)
│   ├── integrations/         # Integration modules
│   │   ├── drive_uploader.py  # Google Drive uploader
│   │   └── sheets_reader.py   # Google Sheets data reader
│   ├── generators/           # Content generators
│   │   ├── ai_generator.py    # AI content generator
│   │   ├── chart_generator.py # Analytics chart generator
│   │   ├── report_generator.py # Report generator
│   │   └── pdf_report_generator.py # PDF report generator
│   ├── notifications/        # Notification services
│   │   └── notifier.py        # Email and Slack notifier
│   ├── persistence/          # Data persistence
│   │   └── database.py        # Database manager
│   └── main.py                # Main entry point
├── .env                     # Environment variables
├── requirements.txt                # Dependencies
├── docs/                           # Documentation
│   ├── README_en.md         # English documentation
│   └── README_vi.md         # Vietnamese documentation
├── data/                           # Data storage
│   └── google_credentials.json # Google API credentials
├── logs/                           # Log files
├── reports/                        # Generated reports
│   └── charts/              # Analytics charts
└── tests/                   # Unit tests
```

## Setup and Usage

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up Google API authentication:
   - Create a new project in [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Google Sheets API and Google Drive API for the project
   - Create a Service Account and download the JSON credentials file
   - Place this file in the `data/google_credentials.json` directory
   - Create a Google Sheet with the following columns: `id`, `description`, `example_asset_url`, `output_format`, `model`
   - Share your Google Sheet with the Service Account email address

   Example Google Sheet data structure:

   | id | description | example_asset_url | output_format | model |
   |----|-------------|-------------------|---------------|-------|
   | asset-001 | Logo game phong cách pixel art với hình con rồng | https://example.com/reference/dragon_logo.jpg | PNG | openai |
   | asset-002 | Nhân vật game chibi với kiếm và áo giáp | https://example.com/reference/warrior_character.jpg | PNG | anthropic |
   | asset-003 | Cảnh nền rừng nhiệt đới với thác nước | https://example.com/reference/jungle_background.jpg | JPG | openai |

3. Configure your settings in `.env` file:
   ```
   # Google API credentials
   GOOGLE_APPLICATION_CREDENTIALS=./data/google_credentials.json
   GOOGLE_SHEETS_ID=your_sheet_id
   GOOGLE_DRIVE_FOLDER_ID=your_folder_id

   # AI API keys
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key

   # Notification settings
   EMAIL_SMTP_SERVER=smtp.gmail.com
   EMAIL_SMTP_PORT=587
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   ADMIN_EMAIL=admin_email@example.com

   # Slack settings
   SLACK_WEBHOOK_URL=your_slack_webhook_url
   ```

3. Ensure you have Google API credentials file (`google_credentials.json`) in the `data` directory.

4. Run the automation:
   ```
   python src/main.py
   ```

   With specific command-line arguments (overrides .env settings):
   ```
   python src/main.py --sheet-id YOUR_SHEET_ID --openai-key YOUR_OPENAI_KEY --drive-folder YOUR_FOLDER_ID
   ```

   With a custom .env file:
   ```
   python src/main.py --env-file path/to/.env.custom
   ```

For more detailed instructions, see the documentation files in the `docs` directory.
