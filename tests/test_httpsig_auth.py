import unittest

from httpie_httpsig_auth import HTTPSignatureAuth


class TestHTTPSignatures(unittest.TestCase):
    def test_call(self):

        class RequestMock(object):
            def __init__(self, headers, method, url, path_url):
                self.headers = headers
                self.method = method
                self.url = url
                self.path_url = path_url

        request_params = dict(
            headers={'date': 'Wed, 26 Jul 2017 11:02:39 GMT'},
            method='get',
            url='http:/example.com',
            path_url='/')
        request_mock = RequestMock(**request_params)
        httpsig_auth = HTTPSignatureAuth('key_id', 'private_key')
        # Make a signed request
        signed_request = httpsig_auth(request_mock)
        auth = signed_request.headers['authorization']
        assert auth is not None
        assert auth == 'Signature headers="date (request-target) host",keyId="key_id",algorithm="hmac-sha256",signature="rrFf9OYggCCxjTCv2hIuH+OEI2gbeaFUlc1viEGQdfo="' # noqa
