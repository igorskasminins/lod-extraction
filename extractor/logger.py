import logging

class Logger:
    """
    Logger wrapper class for logging messages with predefined configuration
    """
    def __init__(self):
        """ Initialize and configure logger """
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
        print(message)

    def print_and_log_error(self, message):
        """ Prints and logs the message on error level """
        self.logger.error(message)
        print(message)