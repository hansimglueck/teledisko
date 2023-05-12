import logging
import logging.handlers

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    #create syslog-handler
    syslog = logging.handlers.SysLogHandler(address='/dev/log')
    syslog.setLevel(logging.DEBUG)
    # add formatter to syslog
    syslog.setFormatter(formatter)
    # add syslog to logger
    logger.addHandler(syslog)

    return logger
