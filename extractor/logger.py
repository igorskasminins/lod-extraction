import logging
import os
from datetime import date

class Logger:
    """
    Logger wrapper class for logging messages with predefined configuration
    """
    def __init__(self):
        """ Initialize and configure logger """
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            filename='logs/system.log', 
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        self.logger = logging.getLogger()

    def print_and_log_info(self, message):
        """ Prints and logs the message on info level """
        self.logger.info(message)
        today = date.today()
        print(today, ':', message)

    def print_and_log_error(self, message):
        """ Prints and logs the message on error level """
        self.logger.error(message)
        today = date.today()
        print(today, ':', message)