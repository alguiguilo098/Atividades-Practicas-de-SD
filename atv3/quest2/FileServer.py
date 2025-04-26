import logging
import os
from threading import Thread
import socket


logging.basicConfig(
    level=logging.INFO,
    format="{asctime} - {levelname} - {message}",
    datefmt="%d-%m-%Y %H:%M",
    style="{",
    filename="./logs/logs.log",
    encoding="utf-8",
    filemode="a"
)

class FileServer:
    def __init__(self, host='0.0.0.0', port=777):
        pass


if __name__ == "__main__":
    pass

    