DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': '1234',
    'database': 'documents'
}

# Настройки парсера
PARSER_CONFIG = {
    'input_folder': 'documents',
    'output_csv': 'output.csv',
    'supported_formats': ['.txt', '.docx', '.pdf', '.xlsx', '.xls']
}