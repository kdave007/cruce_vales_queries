# SQL Query Tool

A tool for executing SQL queries and generating Excel reports.

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `credentials.secure.env` file in the `config` directory with the following structure:
```env
# Database Credentials - KEEP THIS FILE SECURE AND NEVER COMMIT TO GIT
DB_NAME=your_db_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_host_ip
DB_PORT=5432
```

**Important**: Never commit the `credentials.secure.env` file to git as it contains sensitive information.

## Configuration

1. Database Connection:
   - Set up database credentials in `config/credentials.secure.env`
   - The tool uses psycopg2 to connect to PostgreSQL databases

2. Query Parameters:
   - Edit `config/config.env` to set default query parameters:
     ```env
     QUERY_DATE_START=20240101    # Start date in YYYYMMDD format
     QUERY_DATE_END=20240131      # End date in YYYYMMDD format
     QUERY_LOCATIONS=LOC1,LOC2    # Comma-separated list of locations
     FILE_NAME=My_Report_Name      # Excel file name (optional, defaults to 'Reporte')
     TEST_MODE=on                  # Test mode (optional, defaults to 'on')
     ```
   Notes:
   - If FILE_NAME is not set, files will be named `Reporte_YYYYMMDD_HHMMSS.xlsx`
   - Invalid filename characters will be replaced with underscores
   - Leading/trailing spaces and dots are removed
   - Empty filenames will default to 'Reporte'

3. Excel Output:
   - Reports are generated with timestamp names (e.g., `{FILE_NAME}_{timestamp}.xlsx`)
   - Each query result is saved in a separate sheet
   - Headers are formatted with bold text and colored background

## Usage

Run the main script:
```bash
python test_completed.py
```

The tool will:
1. Connect to the database using credentials from `credentials.secure.env`
2. Execute selected queries (test or production based on TEST_MODE)
3. Generate Excel reports with results

### Available Options:
1. Execute individual queries (1-3)
2. Run test query
3. Execute all queries at once
4. Use environment config or manual input for parameters