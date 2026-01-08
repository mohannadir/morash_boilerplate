from CONFIG.logging import USE_BETTERSTACK

import logging
logtail_logger = logging.getLogger('logtail')

def log_to_betterstack(message, level='info', extra=None):
    if not USE_BETTERSTACK:
        raise Exception('BetterStack logging is not enabled.')
    
    if level == 'info':
        logtail_logger.info(message, extra=extra)
    elif level == 'warning':
        logtail_logger.warning(message, extra=extra)
    elif level == 'error':
        logtail_logger.error(message, extra=extra)
    elif level == 'critical':
        logtail_logger.critical(message, extra=extra)
    else:
        logtail_logger.debug(message, extra=extra)