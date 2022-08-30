import logging

_log_format = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"


def get_file_handler(filename):
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(name, filename):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler(filename))
    logger.addHandler(get_stream_handler())
    return logger

# import logging.config
# import sys
#
#
# LOGGING_CONFIG = {
#     'version': 1,
#     'disable_existing_loggers': True,
#
#     'formatters': {
#         'default_formatter': {
#             'format': '[%(levelname)s:%(asctime)s] %(message)s'
#         },
#     },
#
#     'handlers': {
#         'file_handler': {
#             'level': logging.DEBUG,
#             'class': 'logging.FileHandler',
#             'formatter': 'default_formatter',
#             # 'path': '/var/tmp',
#             'filename': '1',
#             'mode': 'w'
#         },
#     },
#
#     'loggers': {
#         'logger': {
#             'handlers': ['file_handler'],
#             'level': 'DEBUG'
#             # 'propagate': True
#         }
#     }
# }
#
# #
# # def log():
# #     log.config.dictConfig(LOGGING_CONFIG)
# #     logger = log.getLogger('my_logger')
# #     # logger.debug('debug log')
# #     return logger
#
#
# # logging.config.dictConfig({
# #     "version": 1,
# #     "formatters": {
# #         "default": {
# #             "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
# #         },
# #     },
# #     "handlers": {
# #         "console": {
# #             "level": 'DEBUG',
# #             "class": "logging.StreamHandler",
# #             "stream": "ext://sys.stdout"
# #         }
# #     },
# #     "loggers": {
# #         "": {
# #             "level": "DEBUG",
# #             "handlers": ["console"]
# #         }
# #     }
# # })
#
#
# def logger(path):
#     # # logger = logging
#     # # logger.basicConfig(format='%(asctime)s - %(message)s',
#     # level=logging.INFO)
#     # # # logger.info('hello')
#     # # return logger
#     # result = logging.getLogger(sys._getframe(1).f_globals['__name__'])
#     # LOGGING_CONFIG['handlers']['file_handler']['filename'] = path
#     # logging.config.dictConfig(LOGGING_CONFIG)
#     # result.debug('test mess')
#     # return result
#     # import logging.config
#
#     # logging.basicConfig(
#     #     level=logging.DEBUG,
#     #     format="%(asctime)s [%(levelname)s] %(message)s",
#     #     handlers=[
#     #         logging.FileHandler(path),
#     #     ]
#     # )
#     # return logging.getLogger(sys._getframe(1).f_globals['__name__'])
