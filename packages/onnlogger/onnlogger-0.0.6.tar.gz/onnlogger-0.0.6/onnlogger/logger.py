import logging
import os
import pathlib
from base64 import b64encode

PRINT_LOG_LEVELS = ['INFO', 'WARNING', 'ERROR', 'CRITICAL']


class Loggers:
    def __init__(self, logger_name, console_logger=False, print_logger=False, log_level='INFO', log_file_path='',
                 log_file_json=False):
        log_level = log_level.upper()
        self.log_file_json = log_file_json

        if log_level == 'DEBUG':
            PRINT_LOG_LEVELS.append('DEBUG')

        if log_file_path:
            log_dir = os.path.dirname(log_file_path)

            if not os.path.isdir(log_dir):
                pathlib.Path(log_dir).mkdir(parents=True, exist_ok=True)

            elif os.path.exists(log_file_path):
                os.remove(log_file_path)

        self.print_logger = print_logger
        self.console_logger = self.enable_console_logger(logger_name, log_level) if console_logger else False
        self.file_logger = self.enable_file_logger(logger_name, log_level, log_file_path, self.log_file_json) \
            if log_file_path else False

        logger_types = [self.console_logger, self.file_logger]
        self.log_handlers = [logger_type for logger_type in logger_types if logger_type]

    @staticmethod
    def enable_console_logger(logger_name, log_level):
        logger_name = f'console-{logger_name}'
        console_log = logging.getLogger(logger_name)
        console_log.setLevel(log_level)

        # required to avoid Lambda duplicate logs
        console_log.propagate = False

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(hostname)s - %(message)s',
                                           datefmt='%d-%b-%y %H:%M:%S')
        console_handler.setFormatter(console_format)
        console_log.addHandler(console_handler)

        return console_log

    @staticmethod
    def enable_file_logger(logger_name, log_level, log_file_path, log_file_json):
        logger_name = f'file-{logger_name}'

        if not os.path.exists(log_file_path):
            open(log_file_path, 'w').close()

        file_log = logging.getLogger(logger_name)
        file_log.setLevel(log_level)

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)

        if log_file_json:
            file_format = logging.Formatter('["%(asctime)s","%(levelname)s", "%(hostname)s", "%(message)s"]',
                                            datefmt='%d-%b-%y %H:%M:%S')

        else:
            file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(hostname)s - %(message)s',
                                            datefmt='%d-%b-%y %H:%M:%S')

        file_handler.setFormatter(file_format)
        file_log.addHandler(file_handler)

        return file_log

    def entry(self, level, msg, hostname='system', to_base64=False, hide_base64=True, replace_newlines=True,
              replace_json=False):

        # escape replace double quotes (") with single quotes (') when logging JSON output to file
        if self.log_file_json:
            replace_json = True

        if self.print_logger and level.upper() in PRINT_LOG_LEVELS:
            print(f'{level.upper()} - {msg}')

        for handler in self.log_handlers:
            log_level = getattr(handler, level)

            if handler == self.file_logger:
                if to_base64:
                    if hide_base64:
                        msg = f'Base64 log message hidden due to its length'

                    else:
                        encoded_msg = b64encode(bytes(msg, 'utf-8'))
                        msg = f'Base64 encoded log: {encoded_msg}'

                else:
                    if isinstance(msg, str):
                        if replace_json:
                            msg = msg.replace('"', "'")

                        if replace_newlines:
                            msg = msg.replace('\n', ' ')

            add_hostname = {'hostname': hostname}
            log_level(msg, extra=add_hostname)

