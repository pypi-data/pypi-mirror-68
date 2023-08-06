import datetime as dt
import logging

import pyles

class TelesFormatter(logging.Formatter):
    converter = dt.datetime.fromtimestamp

    # \ref: https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

    #These are the sequences need to get colored ouput
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[1;%dm"
    BOLD_SEQ = "\033[1m"

    COLORS = {
        logging.DEBUG: BLUE,
        logging.INFO: GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: MAGENTA,
    }

    def __init__(self, fmt=None):
        super().__init__(fmt=fmt)

    def formatMessage(self, record):
        record.levelname = record.levelname.lower()
        color = TelesFormatter.COLORS.get(
                record.levelno,
                TelesFormatter.WHITE
                )
        record.colorlvl = TelesFormatter.COLOR_SEQ % (30 + color) + record.levelname + TelesFormatter.RESET_SEQ
        return super().formatMessage(record)

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        return dt.datetime.isoformat(ct.astimezone(dt.timezone.utc), " ", "milliseconds")

class TelesHandler(logging.Handler):
    def __init__(self, master):
        super().__init__()
        self.master = master

    def emit(self, record):
        logobj = pyles.create_log(record.levelno, self.master.name,
            record.message, int(record.created), round(record.msecs * 1e6))
        self.master.network.sendLog(logobj)
