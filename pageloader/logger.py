import os
import logging
LOGNAME = 'page_loader.log'


def set_log_path(path):
    log_path = os.path.join(path, LOGNAME)
    logging.basicConfig(filename=log_path, filemode='a',
                        encoding='utf-8', level=logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

# import logging
# import logging.config
# from getpass import getuser
# import os
#
# LOGGING_CONFIG = {
#     'version': 1,
#     'disable_existing_loggers': True,
#
#     'formatters': {
#         'file_formatter': {
#             'format': '%(asctime)s - [%(levelname)s] %(name)s - %(message)s'
#         },
#         'console_formatter': {
#             'format': '%(levelname)s:%(username)s:%(message)s'
#         }
#
#     },
#
#     'handlers': {
#         "console": {
#             "level": 'INFO',
#             "class": "logging.StreamHandler",
#             'formatter': 'console_formatter',
#             "stream": "ext://sys.stdout"
#         },
#
#         'file_handler': {
#                 'level': 'DEBUG',
#                 'class': 'logging.FileHandler',
#                 'formatter': 'file_formatter',
#                 'filename': 'page-loader.log',
#                 'mode': 'a'
#             }
#     },
#     'loggers': {
#         __name__: {
#             'handlers': ['file_handler', 'console'],
#             'level': 'INFO',
#             'propagate': True
#         }
#     }
# }
#
# #
# #
# # _log_format = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
#
# #
# # def get_file_handler(filename):
# # file_handler = logging.FileHandler(filename)
# # file_handler.setLevel(logging.INFO)
# # file_handler.setFormatter(logging.Formatter(_log_format))
# # return file_handler
# #
#
# # def get_stream_handler():
# # stream_handler = logging.StreamHandler()
# # stream_handler.setLevel(logging.INFO)
# # stream_handler.setFormatter(logging.Formatter(_log_format))
# # return stream_handler
#
#
# def get_logger(name):
#     log_path = os.path.join(os.getcwd(), 'log')
#     LOGGING_CONFIG['handlers']['file_handler']['filename'] = log_path
#     logging.config.dictConfig(LOGGING_CONFIG)
#     logger = logging.LoggerAdapter(
#         logging.getLogger(__name__),
#         {"username": getuser()}
#     )
#     return logger
#
# # import logging.config
# # import sys
# #
# #     'handlers': {
# #         'file_handler': {
# #             'level': logging.DEBUG,
# #             'class': 'logging.FileHandler',
# #             'formatter': 'default_formatter',
# #             # 'path': '/var/tmp',
# #             'filename': '1',
# #             'mode': 'w'
# #         },
# #     },
# #
# # }
# #
# # #
# # # def log():
# # #     logger = log.getLogger('my_logger')
# # #     # logger.debug('debug log')
# # #     return logger
# #
# #
# # # logging.config.dictConfig({
# # #     "version": 1,
# # #     "formatters": {
# # #         "default": {
# # #             "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
# # #         },
# # #     },
# # #     "handlers": {
# # #         "console": {
# # #             "level": 'DEBUG',
# # #             "class": "logging.StreamHandler",
# # #             "stream": "ext://sys.stdout"
# # #         }
# # #     },
# # #     "loggers": {
# # #         "": {
# # #             "level": "DEBUG",
# # #             "handlers": ["console"]
# # #         }
# # #     }
# # # })
# #
# #
# # def logger(path):
# #     # # logger = logging
# #     # # logger.basicConfig(format='%(asctime)s - %(message)s',
# #     # level=logging.INFO)
# #     # # # logger.info('hello')
# #     # # return logger
# #     # result = logging.getLogger(sys._getframe(1).f_globals['__name__'])
# #     # LOGGING_CONFIG['handlers']['file_handler']['filename'] = path
# #     # logging.config.dictConfig(LOGGING_CONFIG)
# #     # result.debug('test mess')
# #     # return result
# #     # import logging.config
# #
# #     # logging.basicConfig(
# #     #     level=logging.DEBUG,
# #     #     format="%(asctime)s [%(levelname)s] %(message)s",
# #     #     handlers=[
# #     #         logging.FileHandler(path),
# #     #     ]
# #     # )
# #     # return logging.getLogger(sys._getframe(1).f_globals['__name__'])
