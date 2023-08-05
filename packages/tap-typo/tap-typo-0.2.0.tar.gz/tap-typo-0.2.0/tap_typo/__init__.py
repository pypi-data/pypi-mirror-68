#!/usr/bin/env python3

import sys
import singer
from singer import utils

from tap_typo.logging import log_critical, log_error, log_info
from tap_typo.typo import TapTypo


REQUIRED_CONFIG_KEYS = [
    'api_key', 'api_secret', 'cluster_api_endpoint'
]
LOGGER = singer.get_logger()


@utils.handle_top_exception(LOGGER)
def main():
    '''
    Called when the program is executed.
    '''
    # Parse command line arguments
    try:
        args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    except Exception as exception:  # pylint: disable=W0703
        log_critical(exception)
        sys.exit(1)

    config = args.config

    if args.discover:
        log_info('Starting in Discover Mode.')
    else:
        log_info('Starting in Sync Mode.')

    tap = TapTypo(
        catalog=args.catalog.to_dict() if args.catalog else None,
        config=config,
        state=args.state
    )

    if args.discover:
        tap.discover()
        log_info('Discover Mode completed.')
    else:
        catalog_mode = args.catalog is not None
        tap.sync(catalog_mode)
        log_info('Sync Mode completed.')


if __name__ == '__main__':
    log_error('__main__')
    main()
