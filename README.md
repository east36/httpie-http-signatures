# HTTPIE-http-signatures

 [HTTP Signatures](https://tools.ietf.org/html/draft-cavage-http-signatures-07) auth plugin for HTTPie

 ## Installation

Latest stable version:

```bash
pip install -U httpie-httpsignature-auth
```
Latest developing version:
```
pip install -U https://github.com/manuthu/httpie-http-signatures/archive/master.zip
```

## Usage

```bash
(env) mike@mike:~$ http --auth 'username:password' --auth-type=httpsig localhost -v
GET / HTTP/1.1
accept: */*
accept-encoding: gzip, deflate
authorization: Signature headers="date (request-target) host",keyId="username",algorithm="hmac-sha256",signature="h5DO6glOKFMZ3hGpNWrstFNWe5mNaSckjgvS3ENAoPM="
connection: keep-alive
content-type: application/json
date: Wed, 26 Jul 2017 10:20:31 GMT
host: localhost
user-agent: HTTPie/0.9.9

```
