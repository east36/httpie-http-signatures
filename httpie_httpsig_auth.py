import six
import hashlib
import base64
import requests
import email.utils
import httpsig_cffi.sign
from httpie.plugins import AuthPlugin

__version__ = '0.1.0'
__author__ = 'Mike Manuthu'
__licence__ = 'MIT'


class HTTPSignatureAuth(requests.auth.AuthBase):
    """
    HTTP Signature Request auth.

    This class signs HTTP messages base on the draft specs. https://tools.ietf.org/html/draft-cavage-http-signatures-07 # noqa
    """

    generic_headers = [
        "date",
        "(request-target)",
        "host"
    ]
    body_headers = [
        "content-length",
        "content-type",
        "digest",
    ]
    required_headers = {
        "get": generic_headers,
        "head": generic_headers,
        "delete": generic_headers,
        "put": generic_headers + body_headers,
        "post": generic_headers + body_headers
    }

    def __init__(self, key_id, private_key, algorithm="hmac-sha256"):
        self.signers = {}
        for method, headers in six.iteritems(self.required_headers):
            signer = httpsig_cffi.sign.HeaderSigner(
                key_id=key_id, secret=private_key,
                algorithm=algorithm, headers=headers[:])
            use_host = "host" in headers
            self.signers[method] = (signer, use_host)

    def inject_missing_headers(self, request, sign_body):
        request.headers.setdefault(
            "date", email.utils.formatdate(usegmt=True))
        request.headers.setdefault("content-type", "application/json")
        request.headers.setdefault(
            "host", six.moves.urllib.parse.urlparse(request.url).netloc)

        if sign_body:
            body = request.body or ""
            if "digest" not in request.headers:
                m = hashlib.sha256(body.encode("utf-8"))
                base64digest = base64.b64encode(m.digest())
                # base64string = base64digest.decode("utf-8")
                request.headers["digest"] = 'SHA-256=' + base64digest
            request.headers.setdefault("content-length", len(body))

    def __call__(self, request):
        verb = request.method.lower()
        # nothing to sign for options
        if verb == "options":
            return request
        signer, use_host = self.signers.get(verb, (None, None))
        if signer is None:
            raise ValueError(
                "Don't know how to sign request verb {}".format(verb))

        # Inject body headers for put/post requests, date for all requests
        sign_body = verb in ["put", "post"]
        self.inject_missing_headers(request, sign_body=sign_body)

        if use_host:
            host = six.moves.urllib.parse.urlparse(request.url).netloc
        else:
            host = None

        signed_headers = signer.sign(
            request.headers, host=host,
            method=request.method, path=request.path_url)
        request.headers.update(signed_headers)
        return request


class HTTPSignatureAuthPlugin(AuthPlugin):
    """HTTPSignatureRequestAuth plugin registration."""

    name = 'HTTPSignature auth'
    auth_type = 'httpsig'
    description = 'Sign requests using HTTPSignatures'

    def get_auth(self, username, password):
        return HTTPSignatureAuth(username, password)
