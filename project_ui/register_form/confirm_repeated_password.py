import requests
from configuration.path_urls import Urls


def confirm_password(password, repeated_password):
    return password == repeated_password
