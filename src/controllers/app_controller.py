# src/controllers/app_controller.py
from datetime import datetime
from ..services.config_service import ConfigService
from .query_controller import QueryController
from ..services.excel_service import ExcelService

class AppController:
    def __init__(self):
        self.config_service = ConfigService()
        self.query_controller = QueryController()
        self.available_queries = {
            '1': 'query_1',
            '2': 'query_2',
            '3': 'query_3',
            '4': 'query_test',
            '5': 'all'
        }
    
    def actions(self):
        """ selects the query or queries to execute"""    

    def show_menu(self):
        """ Display main menu and get user choice"""
        print("\n=== Menú Principal ===")
        print("1. Ejecutar Query 1")
        print("2. Ejecutar Query 2")
        print("3. Ejecutar Query 3")
        print("4. Ejecutar Query Test")
        print("5. Ejecutar Todas (sin Test)")
        print("0. Salir")

        return input("\nSeleccione una opción: ")

    def get_config_preference(self):
        """Ask if user wants to use env config"""
        print("\n¿Desea usar la configuración del archivo .env?")
        choice = input("(S/N): ").upper()
        return choice == 'S'

    def get_input_user_params(self):
        """Get parameters from user input"""
        print("\n=== Configuración de Parámetros ===")
        
        while True:
            try:
                # Get date range
                print("\nIngrese el rango de fechas (formato: YYYYMMDD)")
                start_date = input("Fecha inicial: ")
                end_date = input("Fecha final: ")
                
                # Validate date format
                if not (len(start_date) == 8 and len(end_date) == 8 and 
                       start_date.isdigit() and end_date.isdigit()):
                    raise ValueError("Las fechas deben tener formato YYYYMMDD y ser números")
                
                # Convert to int to validate ranges
                year_start = int(start_date[:4])
                month_start = int(start_date[4:6])
                day_start = int(start_date[6:])
                
                year_end = int(end_date[:4])
                month_end = int(end_date[4:6])
                day_end = int(end_date[6:])
                
                # Basic date validation
                if not (2000 <= year_start <= 2100 and 2000 <= year_end <= 2100):
                    raise ValueError("El año debe estar entre 2000 y 2100")
                if not (1 <= month_start <= 12 and 1 <= month_end <= 12):
                    raise ValueError("El mes debe estar entre 01 y 12")
                if not (1 <= day_start <= 31 and 1 <= day_end <= 31):
                    raise ValueError("El día debe estar entre 01 y 31")
                
                # Get locations
                print("\nIngrese las ubicaciones (separadas por coma)")
                print("Ejemplo: BAJAC,GUADA")
                locations_input = input("Ubicaciones: ")
                locations = [loc.strip() for loc in locations_input.split(',') if loc.strip()]
                
                if not locations:
                    raise ValueError("Debe ingresar al menos una ubicación")
                
                return {
                    'date_range': {
                        'start': start_date,
                        'end': end_date
                    },
                    'locations': locations
                }
            except ValueError as e:
                print(f"\n✗ Error: {str(e)}")
                print("Por favor intente nuevamente.")

    def execute_all(self, params):
        """Execute all queries"""
        results = {}
        total_queries = 3
        completed = 0

        for key, query_name in self.available_queries.items() :
        
            if query_name != 'all' and  query_name != 'query_test':

                print(f"\nEjecutando {query_name}...")
                
                start_time = datetime.now()
                print(f"\n[{completed + 1}/{total_queries}] Ejecutando {query_name}...")

                try:
                  
                   # results[query_name] = self.query_exe(debug_query, params)

                    results[query_name] = self.query_exe(query_name, params)
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()

                    print(f"✓ {query_name} completada en {duration:.2f} segundos")

                    
                except Exception as e:    
                    print(f"✗ Error en {query_name}: {str(e)}")
                    results[query_name] = None

                completed += 1

        print(f"\n=== Resumen de Ejecución ===")
        print(f"Queries completadas: {completed}/{total_queries}")
        return results
                
        
    def query_exe(self, query_name, params):
        """
        executes a single query and returns results
        """   
        #DEBUG PURPOSES HERE ---------------------------------------
        if self.config_service.get_query_params()['test_mode']:  
            query_name = "query_test"
            print(f"\nEjecutando con bandera activada de prueba {query_name}...")
        
        return self.query_controller.execute_query(query_name, params)

    def generate_excel(self, results):
        """ generate excel """
        if not results:
            print("✗ No hay resultados para generar el archivo Excel")
            return

        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{self.config_service.get_query_params().get('file_name', 'Reporte')}_{current_time}"
        excel = ExcelService(file_name + ".xlsx")
        sheets = {}
        no_data_queries = []

        # Process each query result
        for idx, (query_name, query_result) in enumerate(results.items(), 1):
            if query_result and query_result.get('data'):  # Only create sheet if we have data
                print(f"[{idx}/{len(results)}] Generando hoja para {query_name}...")
                
                # Create sheet with query name
                sheet = excel.create_sheet(query_name)
                sheets[query_name] = sheet

                headers = query_result.get('headers', [])
                data = query_result.get('data', [])

                if headers and data:
                    excel.write_headers(sheet, headers)
                    excel.write_data(sheet, data)
            else:
                no_data_queries.append(query_name)
        
        # Only save if we have at least one sheet with data
        if sheets:
            try:
                excel.save()
                print(f"✓ Archivo generado: {file_name}.xlsx")
                print(f"Hojas creadas: {', '.join(sheets.keys())}")
                if no_data_queries:
                    print(f"✗ Queries sin resultados: {', '.join(no_data_queries)}")
            except Exception as e:
                print(f"✗ Error generando Excel: {str(e)}")
        else:
            print("✗ No hay datos para generar el archivo Excel")
            print(f"✗ Queries sin resultados: {', '.join(no_data_queries)}")

    def run(self):
        """Main execution flow"""
        results = {}
        while True:
            choice = self.show_menu()

            if(choice == '0'):
                print('Proceso finalizado')
                break

            if(choice not in self.available_queries):
                print('Opción no válida')
                continue    

            use_env = self.get_config_preference()
            params = None

            if(use_env):
                params = self.config_service.get_query_params()
            else:
                params = self.get_input_user_params()
            
            if(choice == '5'):
                results = self.execute_all(params)
            else:
                query_name = self.available_queries[choice]
                results = {query_name : self.query_exe(query_name, params)}

            if results:
                try:
                    self.generate_excel(results)
                except Exception as e:
                    print(f"✗ Error generando Excel: {str(e)}")

        
        
