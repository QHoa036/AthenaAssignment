# AI Content Generation Automation Project

## Introduction

This project was developed to address Assignment 1 of the Athena task, focusing on automating the process of generating content using AI. The system retrieves data from Google Sheets, generates content using AI models (like OpenAI or Claude), stores results in Google Drive, and provides notifications and analytical reports.

## Project Structure

```
Assignment01/
├── src/                     # Main source code
│   ├── main.py              # Main entry point
│   ├── sheets_reader.py     # Google Sheets data reader
│   ├── ai_generator.py      # AI content generator
│   ├── drive_uploader.py    # Google Drive uploader
│   ├── notifier.py          # Email and Slack notifier
│   ├── database.py          # Database manager
│   ├── report_generator.py  # Report generator
│   ├── chart_generator.py   # Analytics chart generator
│   └── html_report_generator.py # HTML report generator
├── config.py                # Application configuration
├── data/                    # App data and database
├── logs/                    # Log files
├── reports/                 # Output reports
│   └── charts/              # Analytics charts
├── docs/                    # Documentation
└── tests/                   # Unit tests
```

## How It Works

1. **Input Data Reading**: The system reads data from Google Sheets containing content descriptions, reference asset URLs, output formats, and AI model specifications.

2. **AI Content Generation**: For each row, the system uses either OpenAI or Claude to generate content (images or audio) based on descriptions and reference assets.

3. **Result Storage**: Generated content is uploaded to Google Drive with a logical organizational structure.

4. **Notifications**: The system sends notifications via email and Slack about successful or unsuccessful completions.

5. **Logging**: All activities and results are stored in an SQLite database.

6. **Analytical Reports**: Daily, the system generates an analytical report with statistical charts and emails it to the administrator.

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure parameters in `config.py`:
   - Add Google API information (Google Sheets, Google Drive)
   - Configure API keys for OpenAI or Claude
   - Configure email settings and Slack webhook

3. Ensure you have Google API credentials file (`google_credentials.json`) in the `data` directory.

## Usage

### Run the automation workflow:

```bash
python src/main.py
```

### Run with specific Google Sheet:

```bash
python src/main.py --sheet-id YOUR_SHEET_ID
```

### Run with different configuration file:

```bash
python src/main.py --config path/to/custom_config.py
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
