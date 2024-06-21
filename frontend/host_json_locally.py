#!/usr/bin/env python3
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler, test

from typeguard import typechecked


class CORSRequestHandler(SimpleHTTPRequestHandler):
    @typechecked
    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        SimpleHTTPRequestHandler.end_headers(self)


if __name__ == "__main__":
    test(
        CORSRequestHandler,
        HTTPServer,
        port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000,
    )
