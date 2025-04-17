# src/services/config_service.py
from dotenv import load_dotenv
import os
from pathlib import Path

class ConfigService:
    def __init__(self):
        self.query_params = None
        self.load_all_config()

    def load_all_config(self):
        """Load all configuration from env files"""
        self.load_query_config()

    def load_query_config(self):
        """Load query parameters from env"""
        # Get the project root directory
        project_root = Path(__file__).parent.parent.parent
        env_path = project_root / 'config' / 'config.env'
        
        # Load the .env file
        load_dotenv(env_path)
        
        # Parse locations from comma-separated string
        locations_str = os.getenv('QUERY_LOCATIONS', '')
        
        # Get and sanitize file name
        file_name = self._sanitize_filename(os.getenv('FILE_NAME', 'Reporte'))
        
        # Get test mode (default to 'on')
        test_mode = os.getenv('TEST_MODE', 'on').lower()
        
        self.query_params = {
            'date_range': {
                'start': os.getenv('QUERY_DATE_START'),
                'end': os.getenv('QUERY_DATE_END')
            },
            'locations': [loc.strip() for loc in locations_str.split(',') if loc.strip()],
            'file_name': file_name,
            'test_mode': test_mode == 'on'  # Convert to boolean
        }

    def _sanitize_filename(self, filename):
        """
        Sanitize filename by removing invalid characters
        """
        # Replace invalid characters with underscore
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Remove control characters
        filename = "".join(char for char in filename if ord(char) >= 32)
        
        # Trim spaces and dots from ends
        filename = filename.strip(". ")
        
        # If empty after sanitizing, return default
        return filename if filename else "Reporte"

    def get_query_params(self):
        """Get query parameters"""
        return self.query_params

    def validate_config(self):
        """Validate that all required configuration is present"""
        if not self.query_params:
            raise ValueError("Query parameters are missing")
            
        date_range = self.query_params['date_range']
        if not date_range or not date_range['start'] or not date_range['end']:
            raise ValueError("Date range is incomplete")
            
        if not self.query_params['locations']:
            raise ValueError("No locations specified")