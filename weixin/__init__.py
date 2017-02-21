import logging
from logging.config import dictConfig

from access_token_manager import Manager
from api import WxApiPublic

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s %(funcName)s(%(filename)s:%(lineno)s) %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'raw': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': 'weixin.log',
            'maxBytes': 1024,
            'backupCount': 3
        }
    },
    'loggers': {
        'weixin': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}

dictConfig(LOGGING)

logging.debug("[weixin] start success")