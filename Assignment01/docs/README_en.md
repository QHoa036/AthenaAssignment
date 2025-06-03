# AI Content Generation Automation Project

## Introduction

This project was developed to address Assignment 1 of the Athena task, focusing on automating the process of generating content using AI. The system retrieves data from Google Sheets, generates content using AI models (like OpenAI or Claude), stores results in Google Drive, and provides notifications and analytical reports.

> **Note**: This codebase has been fully localized with Vietnamese comments, docstrings, and logger messages to support the Vietnamese development team.

## Project Structure

```
Assignment01/
│── src/                     # Main source code (localized in Vietnamese)
│   │── integrations/         # Integration modules
│   │   │── drive_uploader.py  # Google Drive uploader
│   │   └── sheets_reader.py   # Google Sheets data reader
│   │── generators/           # Content generators
│   │   │── ai_generator.py    # AI content generator
│   │   │── chart_generator.py # Analytics chart generator
│   │   │── report_generator.py # Report generator
│   │   └── pdf_report_generator.py # PDF report generator
│   │── notifications/        # Notification services
│   │   └── notifier.py        # Email and Slack notifier
│   │── persistence/          # Data persistence
│   │   └── database.py        # Database manager
│   └── main.py                # Main entry point
│── .env                     # Environment variables
│── data/                    # App data and database
│   └── google_credentials.json # Google API credentials
│── logs/                    # Log files
│── reports/                 # Output reports
│   └── charts/              # Analytics charts
│── docs/                    # Documentation
│   │── README_en.md         # English documentation
│   └── README_vi.md         # Vietnamese documentation
└── tests/                   # Unit tests
```

## How It Works

1. **Input Data Reading**: The system reads data from Google Sheets containing content descriptions, reference asset URLs, output formats, and AI model specifications.

2. **AI Content Generation**: For each row, the system uses either OpenAI or Claude to generate content (images or audio) based on descriptions and reference assets.

3. **Result Storage**: Generated content is uploaded to Google Drive with a logical organizational structure.

4. **Notifications**: The system sends notifications via email and Slack about successful or unsuccessful completions.

5. **Logging**: All activities and results are stored in an SQLite database.

6. **Analytical Reports**: Daily, the system generates an analytical report with statistical charts and emails it to the administrator.

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

3. Set up environment variables in `.env` file:
   ```
   # Google API credentials
   GOOGLE_APPLICATION_CREDENTIALS=./data/google_credentials.json
   GOOGLE_SHEETS_ID=your_sheet_id

   # AI API keys
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key

   # Notification settings
   EMAIL_SENDER=your_email@example.com
   EMAIL_PASSWORD=your_app_password
   EMAIL_RECIPIENT=admin@example.com

   # Slack settings
   SLACK_WEBHOOK_URL=your_slack_webhook_url

   # Storage settings
   GOOGLE_DRIVE_FOLDER_ID=your_folder_id
   ```

3. Ensure you have Google API credentials file (`google_credentials.json`) in the `data` directory.

## Usage

### Run the automation workflow:

```bash
python src/main.py
```

### Run with specific command-line arguments (overrides .env settings):

```bash
python src/main.py --sheet-id YOUR_SHEET_ID --openai-key YOUR_OPENAI_KEY --drive-folder YOUR_FOLDER_ID
```

### Run with a custom .env file:

```bash
python src/main.py --env-file path/to/.env.custom
```

## Google Sheets Format

The Google Sheets file should have the following columns:

- `id`: Unique ID for each item
- `description`: Description of content to generate
- `example_asset_url`: Reference URL (optional)
- `output_format`: Output format (png, jpg, gif, mp3)
- `model`: AI model to use (openai, claude)

## Reports

Daily reports include:
- Total number of processed items
- Success and failure rates
- Analytics charts
- Details for each item

## System Requirements

- Python 3.8+
- Internet connection to access Google APIs and AI APIs
- Access to Google Sheets and Google Drive
- Email account and Slack webhook (for notifications)
