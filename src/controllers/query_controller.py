# src/controllers/query_controller.py

from ..models.query_1 import Query1
from ..models.query_2 import Query2
from ..models.query_3 import Query3
from ..models.query_test import Query_Test

class QueryController:
    def __init__(self):
        self.queries = {
            'query_1': Query1(),
            'query_2': Query2(),
            'query_3': Query3(),
            'query_test': Query_Test()
        }

    def execute_query(self, query_name, params):
        """
        Execute a specific query with given parameters
        Args:
            query_name (str): Name of the query to execute
            params (dict): Dictionary containing all parameters for the query
                Common parameters:
                - date_range: dict with 'start' and 'end'
                - locations: list of primary locations
                Query specific parameters:
                - secondary_locations: list of secondary locations (for query 2)
                - extra_params: any additional parameters needed
        Returns:
            dict: Contains 'data' and 'headers' if successful
            None: If query fails or returns no results
        """
        try:
            if query_name not in self.queries:
                print(f"Error: Query '{query_name}' no encontrada")
                return None

            query = self.queries[query_name]
            
            # Validate parameters
            if not query.validate_params(params):
                return None

            # Execute query
            results = query.execute(params)
            print(results)
            
            if results and len(results) > 0:
                # Get headers for the results
                headers = query.fetch_headers(results)
                if headers:
                    return {
                        'data': results,
                        'headers': headers
                    }
            
            print("✗ La consulta no retornó resultados")
            return None

        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def get_available_queries(self):
        """Return list of available queries with their parameter requirements"""
        query_info = {}
        for name, query in self.queries.items():
            query_info[name] = {
                'name': query.query_name,
                'required_params': query.get_required_params()  # New method to implement in query models
            }
        return query_info