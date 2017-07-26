import unittest

from httpsig.utils import parse_authorization_header
from httpie_httpsig_auth import HTTPSignatureAuth


class TestHTTPSignatures(unittest.TestCase):
    def test_call(self):

        class RequestMock(object):
            def __init__(self, **kwargs):
                for k, v in kwargs.iteritems():
                    setattr(self, k, v)

        request_params = dict(
            headers={'date': 'Wed, 26 Jul 2017 11:02:39 GMT'},
            method='get',
            url='http:/example.com',
            path_url='/')
        request_mock = RequestMock(**request_params)
        httpsig_auth = HTTPSignatureAuth('key_id', 'private_key')

        # Make a GET signed request
        signed_request = httpsig_auth(request_mock)
        auth = parse_authorization_header(
            signed_request.headers['authorization'])[1]
        self.assertTrue(auth is not None)
        self.assertTrue(
            auth['signature'] == 'rrFf9OYggCCxjTCv2hIuH+OEI2gbeaFUlc1viEGQdfo=') # noqa
        self.assertTrue(auth['headers'] == 'date (request-target) host')
        self.assertTrue(auth['keyid'] == 'key_id')

        # Do a POST signed request
        request_params['method'] = 'post'
        request_params['body'] = {}
        request_mock = RequestMock(**request_params)
        signed_request = httpsig_auth(request_mock)
        auth = parse_authorization_header(
            signed_request.headers['authorization'])[1]
        self.assertTrue(
            auth['headers'] == 'date (request-target) host content-length content-type digest') # noqa
        self.assertTrue(
            auth['signature'] == 'Y9VjBPTbnV7KprGGb2eoUC0M8XAMDK7hqVfuMh2sxMA=') # noqa
