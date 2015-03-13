#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import json
import os

from httq import HTTP, POST


http = HTTP()
http.connect(b"localhost", 7474)

try:
    LOOPS = int(os.getenv("LOOPS", "1"))
except (IndexError, ValueError):
    LOOPS = 1
BODY = json.dumps({"statements": [{"statement": "RETURN 1"}]}, ensure_ascii=True, separators=",:").encode("UTF-8")


def query():
    http.request(POST, b"/db/data/transaction/commit", {b"Content-Type": b"application/json"}, BODY)
    if http.response() == 200:
        raw = http.read()
        if LOOPS == 1:
            print(raw)
            content = json.loads(raw.decode("UTF-8"))
            print(content)
    else:
        raise RuntimeError()


def main():
    for i in range(LOOPS):
        query()


if __name__ == "__main__":
    main()