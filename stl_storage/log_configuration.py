import logging
import os

project = 'stl_storage'

class RelativePathFilter(logging.Filter):
    def filter(self, record):
        try:
            record.relative_path = os.path.relpath(record.pathname)
        except ValueError:
            record.relative_path = record.pathname
        return True

def configure():
    config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                'format': r'%(asctime)s.%(msecs)03d [%(levelname)s] %(relative_path)s:%(lineno)d: %(message)s',
                'datefmt': r'%Y-%m-%d %H:%M:%S',
            },
        },
        'filters': {
            'relative_path': {
                '()': RelativePathFilter
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'filters': ['relative_path'],
                'formatter': 'default',
                'level': 'DEBUG',
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console'],
                'level': 'WARN',
                'propagate': False,
            },
            'asyncio': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'nicegui': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            },
            project: {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }

    logging.config.dictConfig(config)
    return logging.getLogger(project)
