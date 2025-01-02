import logging
import logging.config
import sys


def setup_logging():
    """Configura o logging para toda a API usando um dicionário."""
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,  # Mantém loggers existentes
        'formatters': {
            'default': {
                'format': '[%(levelname)s] - %(asctime)s - %(message)s',
                'datefmt': '%H:%M:%S',
            },
        },
        'handlers': {
            'stream_handler': {
                'class': 'logging.StreamHandler',
                'stream': sys.stdout,
                'level': 'INFO',
                'formatter': 'default',
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['stream_handler'],
        },
        'loggers': {
            'httpx': {
                'level': 'WARNING',  # Configura o logger do httpx para suprimir mensagens de DEBUG
                'handlers': ['stream_handler'],
                'propagate': False,  # Evita que as mensagens sejam propagadas para o root logger
            },
        },
    }

    # Aplica a configuração
    logging.config.dictConfig(logging_config)
