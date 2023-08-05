import sys
import pkg_resources
import singer

# Singer Logger
LOGGER = singer.get_logger()


def format_log_message(message, new_line):
    '''
    Adds tap-typo label and version to log messages
    '''
    return '\'tap-typo:{}\'{}{}'.format(
        pkg_resources.get_distribution('tap_typo').version,
        '\n' if new_line else ' ',
        message
    )


def log_info(message, *args, exc_info=False, new_line=False, **kwargs):
    '''
    Logs an info message
    '''
    LOGGER.info(format_log_message(message, new_line), exc_info=exc_info, *args, **kwargs)


def log_error(message, *args, exc_info=False, new_line=False, **kwargs):
    '''
    Logs a normal error
    '''
    LOGGER.error(format_log_message(message, new_line), exc_info=exc_info, *args, **kwargs)


def log_critical(message, *args, exc_info=False, new_line=False, **kwargs):
    '''
    Logs a critical error
    '''
    LOGGER.critical(format_log_message(message, new_line), exc_info=exc_info, *args, **kwargs)


def log_backoff(details):
    '''
    Logs a backoff retry message
    '''
    (_, exc, _) = sys.exc_info()

    log_info(
        'Network error receiving data from Typo. Sleeping {:.1f} seconds before trying again: {}'.format(
            details['wait'], exc))
