import unittest
from mock import MagicMock

import StringIO

from cdf.exceptions import MalformedFileNameError
from cdf.streams.stream_factory import (get_id_from_filename,
                                        StreamFactory,
                                        HostStreamFactory,
                                        PathStreamFactory,
                                        QueryStringStreamFactory,
                                        MetadataStreamFactory,
                                        _get_number_pages_from_stream)


class TestGetIdFromFileName(unittest.TestCase):
    def test_nominal_case(self):
        self.assertEqual(0, get_id_from_filename("urlcontents.txt.0.gz"))
        self.assertEqual(10, get_id_from_filename("urlcontents.txt.10.gz"))
        self.assertEqual(0, get_id_from_filename("/tmp/urlcontents.txt.0.gz"))

    def test_malformed_filename(self):
        self.assertRaises(MalformedFileNameError,
                          get_id_from_filename,
                          "urlcontents.txt.gz")

        self.assertRaises(MalformedFileNameError,
                          get_id_from_filename,
                          "urlcontents.txt.-1.gz")


class TestStreamFactory(unittest.TestCase):
    def test_constructor(self):
        #test that the constructor raises on unknow content
        self.assertRaises(Exception,
                          StreamFactory,
                          "/tmp",
                          "unknown_content")

    def test_get_file_regexp(self):
        dirpath = None
        content = "urlids"
        stream_factory = StreamFactory(dirpath, content)
        self.assertEqual("urlids.txt.*.gz", stream_factory._get_file_regexp())

        part_id = 1
        stream_factory = StreamFactory(dirpath, content, part_id)
        self.assertEqual("urlids.txt.1.gz", stream_factory._get_file_regexp())

    def test_get_stream_from_file(self):
        dirpath = None
        content = "urlids"
        stream_factory = StreamFactory(dirpath, content)
        #fake file object
        file_content = ("1\thttp\twww.foo.com\t/bar\t?param=value\n"
                        "3\thttp\twww.foo.com\t/bar/baz")
        file = StringIO.StringIO(file_content)

        expected_result = [[1, "http", "www.foo.com", "/bar", "?param=value"],
                           [3, "http", "www.foo.com", "/bar/baz"]]
        actual_result = stream_factory._get_stream_from_file(file)
        self.assertEqual(expected_result, list(actual_result))


class TestHostStreamFactory(unittest.TestCase):
    def test_nominal_case(self):
        stream_factory = MagicMock()
        urlids = [
            (0, "http", "www.foo.com"),
            (1, "http", "www.bar.com"),
            (3, "http", "www.bar.com"),
        ]
        stream_factory.get_stream.return_value = iter(urlids)
        stream_factory.get_max_crawled_urlid.return_value = 1

        path = None
        host_stream_factory = HostStreamFactory(path)
        host_stream_factory.set_stream_factory(stream_factory)

        #urlid 3 is not returned since it has not been crawled
        expected_result = [
            (0, "www.foo.com"),
            (1, "www.bar.com")
        ]

        self.assertEqual(expected_result,
                         list(host_stream_factory.get_stream()))


class TestPathStreamFactory(unittest.TestCase):
    def test_nominal_case(self):
        stream_factory = MagicMock()
        urlids = [
            (0, "http", "www.foo.com", "/"),
            (1, "http", "www.foo.com", "/bar"),
            (3, "http", "www.foo.com", "/bar/baz"),
        ]
        stream_factory.get_stream.return_value = iter(urlids)
        stream_factory.get_max_crawled_urlid.return_value = 1

        path = None
        path_stream_factory = PathStreamFactory(path)
        path_stream_factory.set_stream_factory(stream_factory)

        #urlid 3 is not returned since it has not been crawled
        expected_result = [
            (0, "/"),
            (1, "/bar")
        ]

        self.assertEqual(expected_result,
                         list(path_stream_factory.get_stream()))


class TestQueryStringStreamFactory(unittest.TestCase):
    def test_nominal_case(self):
        stream_factory = MagicMock()
        urlids = [
            (0, "http", "www.foo.com", "/", "?foo=1"),
            (1, "http", "www.foo.com", "/"),
            (2, "http", "www.foo.com", "/", "?foo=bar&baz=2"),
            (3, "http", "www.foo.com", "/", "?foo=2"),
        ]
        stream_factory.get_stream.return_value = iter(urlids)
        stream_factory.get_max_crawled_urlid.return_value = 2

        path = None
        qs_stream_factory = QueryStringStreamFactory(path)
        qs_stream_factory.set_stream_factory(stream_factory)

        #urlid 1 is not returned since it has no query string
        #urlid 3 is not returned since it has not been crawled
        expected_result = [
            (0, {"foo": ["1"]}),
            (2, {"foo": ["bar"], "baz": ["2"]})
        ]

        self.assertEqual(expected_result,
                         list(qs_stream_factory.get_stream()))


class TestMetadataStreamFactory(unittest.TestCase):
    def setUp(self):
        self.stream_factory = MagicMock()
        #setting hash to None since they should not be used in the test
        urlcontents = [
            (0, 1, None, "title"),
            (0, 3, None, "first h2"),
            (0, 3, None, "second h2"),
            (1, 1, None, "title"),
            (1, 2, None, "h1"),
            (1, 3, None, "h2"),
            (3, 1, None, "title"),
        ]
        self.stream_factory.get_stream.return_value = iter(urlcontents)
        self.stream_factory.get_max_crawled_urlid.return_value = 2

    def test_nominal_case_h1(self):
        path = None
        content_type = "h1"
        metadata_stream_factory = MetadataStreamFactory(path, content_type)
        metadata_stream_factory.set_stream_factory(self.stream_factory)

        #urlid 0 is not returned since it has no h1
        #urlid 3 is not returned since it has not been crawled
        expected_result = [
            (1, ["h1"])
        ]

        self.assertEqual(expected_result,
                         list(metadata_stream_factory.get_stream()))

    def test_nominal_case_h2(self):
        path = None
        content_type = "h2"
        metadata_stream_factory = MetadataStreamFactory(path, content_type)
        metadata_stream_factory.set_stream_factory(self.stream_factory)

        #urlid 3 is not returned since it has not been crawled
        expected_result = [
            (0, ["first h2", "second h2"]),
            (1, ["h2"])
        ]

        self.assertEqual(expected_result,
                         list(metadata_stream_factory.get_stream()))


class TestGetNumberPagesFromStream(unittest.TestCase):
    def test_nominal_case(self):
        urlinfos = [
            (1, 0, "text/html", 0, 0, 200),
            (2, 0, "text/html", 0, 0, 0),
            (3, 0, "text/html", 0, 0, 200),
            (4, 0, "text/html", 0, 0, 200),
        ]
        self.assertEqual(2, _get_number_pages_from_stream(iter(urlinfos),
                                                          3))
        self.assertEqual(3, _get_number_pages_from_stream(iter(urlinfos),
                                                          5))
