import pprint
import logging
import traceback

log = logging.getLogger(__name__)

def tracelog(msg, object):
    """
        print traceback for an exception
    """

    log.info('******************** {}'.format(msg))
    log.info('******************** TRACEBACK')

    pp = pprint.PrettyPrinter(indent=1)
    pstr = pp.pprint(object)
    log.info(traceback.format_exc())
