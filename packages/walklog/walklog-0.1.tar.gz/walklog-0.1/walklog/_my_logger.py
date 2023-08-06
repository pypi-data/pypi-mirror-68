import logger from _logger.Logger  

class MyLogger:

    def __init__(self, core, exception, depth, record, lazy, colors, raw, patcher, extra):
        Logger.__init__(self, core, exception, depth, record, lazy, colors, raw, patcher, extra)
    
    def __repr__(self):
        logger.__repr__(self)

    def traceLOG(__self, __message, *args, **kwargs):
        logger.trace(__self, __message, *args, **kwargs)

    def debugLOG(__self, __message, *args, **kwargs):
        logger.debug(__self, __message, *args, **kwargs)

    def infoLOG(__self, __message, *args, **kwargs):
        logger.info(__self, __message, *args, **kwargs)

    def successLOG(__self, __message, *args, **kwargs):
        logger.success(__self, __message, *args, **kwargs)

    def warningLOG(__self, __message, *args, **kwargs):
        logger.warning(__self, __message, *args, **kwargs)

    def errorLOG(__self, __message, *args, **kwargs):
        logger.error(__self, __message, *args, **kwargs)

    def criticalLOG(__self, __message, *args, **kwargs):
        logger.critical(__self, __message, *args, **kwargs)

    def exceptionLOG(__self, __message, *args, **kwargs):
        logger.exception(__self, __message, *args, **kwargs)

    def logLOG(__self, __level, __message, *args, **kwargs):
        logger.log(__self, __level, __message, *args, **kwargs)
