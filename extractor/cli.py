import typer
from extractor.logger import Logger
from extractor.main import ExtractorAPI

app = typer.Typer()
logger = Logger()
make_api_call = ExtractorAPI()

@app.command('start-source')
def start_source():
    """ Starts the extraction from the source (endpoint) """
    logger.print_and_log_info('Starting extraction from the source')
    make_api_call.process_endpoints_from_source()

@app.command('start-file')
def start_file():
    """ Starts the extraction from a file """
    logger.print_and_log_info('Starting extraction from a file')
    make_api_call.process_custom_endpoints()
