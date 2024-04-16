""" Module for providing an entry-point script to run the app from the package using the python -m extraction command """

from extractor import cli, __app_name__

def main():
    cli.app(prog_name=__app_name__)

if __name__ == '__main__':
    main()