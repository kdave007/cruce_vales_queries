# src/controllers/app_controller.py
from datetime import datetime
from dotenv import load_dotenv
import os

from .query_controller import QueryController
from ..services.excel_service import ExcelService

class AppController:
    def __init__(self):
        self.query_controller = QueryController()
        self.load_env_config()
    
    def load_config(self):
        """Load all configuration"""
        # Load query config from query_config.env
        load_dotenv('config/query_config.env')
        
        # Parse locations from comma-separated string
        locations_str = os.getenv('QUERY_LOCATIONS', '')
        self.query_params = {
            'date_range': {
                'start': os.getenv('QUERY_DATE_START'),
                'end': os.getenv('QUERY_DATE_END')
            },
            'locations': [loc.strip() for loc in locations_str.split(',') if loc.strip()]
        }

    def actions():
        """ selects the query or queries to execute"""    

    def query_exe():
        """
        executes a single query and returns results
        """    