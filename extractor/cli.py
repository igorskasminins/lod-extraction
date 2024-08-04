import typer
from extractor.logger import Logger
from extractor.main import ExtractorAPI

app = typer.Typer()
logger = Logger()
make_api_call = ExtractorAPI()

@app.command('start-source')
def start_source(
        include_most_used_properties: bool = typer.Option(
            False,
            '--include-most-used-properties',
            '-imup'
        ),
        ignore_existing_records: bool = typer.Option(
            False,
            '--ignore-existing-records',
            '-f'
        )
    ):
    """ Starts the extraction from the source (endpoint) """
    logger.print_and_log_info('Starting extraction from the source')
    make_api_call.process_endpoints_from_source(include_most_used_properties, ignore_existing_records)

@app.command('start-file')
def start_file(
        generic_only: bool = typer.Option(
            False,
            '--generic-only',
            '-go'
        ),
        include_most_used_properties: bool = typer.Option(
            False,
            '--include-most-used-properties',
            '-imup'
        ),
        ignore_existing_records: bool = typer.Option(
            False,
            '--ignore-existing-records',
            '-f'
        )
    ):
    """ Starts the extraction from a file """
    logger.print_and_log_info('Starting extraction from a file')
    make_api_call.process_custom_endpoints(generic_only, include_most_used_properties, ignore_existing_records)
