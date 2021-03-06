
from unittest import TestCase, main

from httq import HTTP, HTTPS


class ConnectTestCase(TestCase):

    def test_can_establish_http_connection_without_port(self):
        http = HTTP(b"eu.httpbin.org")
        assert http.host == b"eu.httpbin.org"
        http.close()

    def test_can_establish_http_connection_with_port(self):
        http = HTTP(b"eu.httpbin.org:80")
        assert http.host == b"eu.httpbin.org:80"
        http.close()

    def test_can_establish_https_connection_without_port(self):
        http = HTTPS(b"eu.httpbin.org")
        assert http.host == b"eu.httpbin.org"
        http.close()

    def test_can_establish_https_connection_with_port(self):
        http = HTTPS(b"eu.httpbin.org:443")
        assert http.host == b"eu.httpbin.org:443"
        http.close()


class GetMethodTestCase(TestCase):

    def test_can_use_get_method_long_hand(self):
        http = HTTP(b"httq.io:8080")
        http.get(b"/hello")
        http.response()
        assert http.readable()
        assert http.status_code == 200
        assert http.reason == "OK"
        assert http.content_type == "text/plain"
        assert http.readable()
        assert http.content == "hello, world"
        assert not http.readable()
        http.close()

    def test_can_use_get_method_short_hand(self):
        assert HTTP(b"httq.io:8080").get(b"/hello").response().content == "hello, world"

    def test_can_use_get_method_with_unicode_args(self):
        http = HTTP(u"httq.io:8080")
        http.get(u"/hello").response()
        assert http.status_code == 200
        assert http.reason == "OK"
        assert http.content_type == "text/plain"
        assert http.readable()
        assert http.content == "hello, world"
        assert not http.readable()
        http.close()

    def test_can_pipeline_multiple_get_requests(self):
        count = 3
        turns = range(1, count + 1)
        http = HTTP(b"httq.io")
        for i in turns:
            http.get("/?%d" % i)
            assert len(http._requests) == i
        for i in reversed(turns):
            assert len(http._requests) == i
            assert http.response().status_code == 200
            http.readall()
        assert len(http._requests) == 0
        http.close()


if __name__ == "__main__":
    main()
