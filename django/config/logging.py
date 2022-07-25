import logging
import os

import environ
from boto3 import Session

ADMIN = "admin"
TRANS = "transaction"
DJANGO = "django"
API = "api"
CONSOLE = "console"
CLOUDWATCH = "cloudwatch"

env = environ.Env()
env.read_env('.env')


class ApiLogFilter(logging.Filter):

    def filter(self, record):
        if record.name == 'api':
            return True


class AdminLogFilter(logging.Filter):

    def filter(self, record):
        if record.name == 'admin':
            return True


# logging設定
# 実行環境に寄ってログレベルを設定
LOG_LEVELS = {
    'local': logging.DEBUG,
    'dev': logging.INFO,
    'prod': logging.WARNING
}
log_level = LOG_LEVELS[env('APP_ENV')]

# 共通のhandler
handler_names = ['console']
handlers = {
    'console': {
        'level': log_level,
        'filters': ['require_debug_true'],
        'class': 'logging.StreamHandler',
        'formatter': 'console',
    }
}

# 環境ごとのhandler
if env('APP_ENV') == 'local':
    # localで実行する場合はログをファイルに出力する
    os.makedirs('logs', exist_ok=True)
    handler_names.append('file')
    handlers['file'] = {
        'level': log_level,
        'formatter': 'console',
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'filename': 'logs/django.log',
        'when': 'H',
        'interval': 1,
    }
else:
    # local以外で実行する場合はログをCloudWatchに出力する
    boto3_session = Session(region_name=env('AWS_REGION_NAME'))
    handler_names.append('watchtower')
    handlers['watchtower'] = {
        'level': log_level,
        'class': 'watchtower.CloudWatchLogHandler',
        'boto3_session': boto3_session,
        'use_queues': False,
        'log_group': env('AWS_CLOUD_WATCH_LOG_GROUP'),
        'create_log_group': True,
        'formatter': 'cloudwatch',
    }

handler_names.append(API)
handlers[API] = {
    'level': log_level,
    'formatter': API,
    'filters': [API],
    'class': 'logging.handlers.TimedRotatingFileHandler',
    'filename': f'logs/{API}.log',
    'when': 'H',
    'interval': 1,
}

handler_names.append(ADMIN)
handlers[ADMIN] = {
    'level': log_level,
    'formatter': ADMIN,
    'filters': [ADMIN],
    'class': 'logging.handlers.TimedRotatingFileHandler',
    'filename': f'logs/{ADMIN}.log',
    'when': 'H',
    'interval': 1,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': log_level,
        'handlers': handler_names,
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        API: {
            '()': 'config.logging.ApiLogFilter',
        },
        ADMIN: {
            '()': 'config.logging.AdminLogFilter',
        }
    },
    'formatters': {
        'console': {
            'format': ' [%(levelname)s] [%(asctime)s] [%(module)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        API: {
            'format': '[{levelname}] [{asctime}] [{request_id}] [{ip}] [{method}] [{url_name} => {uri}]'
                      '[{status_code}] [{class_name}.{function_name}] [{total_time}] {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
        ADMIN: {
            'format': '[{asctime}] [ADMIN] [{levelname}] [{username}] [{action}] {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
        'cloudwatch': {
            'format': '[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': handlers,
    'loggers': {
        'django': {
            'level': log_level,
            'handlers': handler_names,
            'propagate': False,
        },
        API: {
            'level': log_level,
            'handlers': [API],
            'propagate': False,
        },
        ADMIN: {
            'level': log_level,
            'handlers': [ADMIN],
            'propagate': False,
        },
    },
}
