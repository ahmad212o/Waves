# Bing Search Automation Tool

## Overview
Automated web scraping tool for extracting search results from Bing using Selenium and SQLite.

## Prerequisites
- Python 3.8+
- Chrome browser
- ChromeDriver

## Installation

1. **Clone Repository**
   ```bash
   git clone git@github.com:ahmad212o/Waves.git  
   cd Waves

## Database Schema
The database consists of two main tables: `search_terms` and `search_results`. The `search_terms` table stores unique search terms along with their timestamps, 
while the `search_results` table contains the results associated with those search terms, including titles, URLs, snippets, and content types.

## Usage
To run the tool, execute the following command:
```bash
pip3 install -r requirments.txt
python main.py
```

## Logging
- Comprehensive logging in each module
- Log level: INFO
- Logs stored in console output

## Error Handling
- Robust exception management
- Contextual error logging
- Graceful failure mechanisms 
