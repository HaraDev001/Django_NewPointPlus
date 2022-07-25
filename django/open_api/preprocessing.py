
import re


def console_preprocessing_hook(endpoints):
    format_path = '^/console/api/v[0-9]/*'
    return [
        (path, path_regex, method, callback)
        for path, path_regex, method, callback in endpoints
        if (re.search(format_path, path))
    ]


def shop_preprocessing_hook(endpoints):
    format_path = '^/shop/api/v[0-9]/*'
    return [
        (path, path_regex, method, callback)
        for path, path_regex, method, callback in endpoints
        if (re.search(format_path, path))
    ]


def card_preprocessing_hook(endpoints):
    format_path = '^/card/api/v[0-9]/*'
    return [
        (path, path_regex, method, callback)
        for path, path_regex, method, callback in endpoints
        if (re.search(format_path, path))
    ]


def terminal_preprocessing_hook(endpoints):
    format_path = '^/terminal/api/v[0-9]/*'
    return [
        (path, path_regex, method, callback)
        for path, path_regex, method, callback in endpoints
        if (re.search(format_path, path))
    ]
