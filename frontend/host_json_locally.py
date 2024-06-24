#!/usr/bin/env python3
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
from json import dumps

from typeguard import typechecked


class CORSRequestHandler(SimpleHTTPRequestHandler):
    @typechecked
    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        SimpleHTTPRequestHandler.end_headers(self)

    @typechecked
    def do_GET(self):
        if self.path == "/folders":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            folder_list = get_folder_list("../output_data")
            self.wfile.write(dumps(folder_list).encode())
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    @typechecked
    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        SimpleHTTPRequestHandler.end_headers(self)


def get_folder_list(path):
    """Retrieves the list of folders in the specified directory.

    Args:     path (str): The path to the directory.

    Returns:     list: A list of folder names within the directory.
    """
    try:
        return [
            f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))
        ]
    except FileNotFoundError:
        return []


if __name__ == "__main__":
    test(
        CORSRequestHandler,
        HTTPServer,
        port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000,
    )
