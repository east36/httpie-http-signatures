from setuptools import setup


setup(
    name='httpie-httpsig-auth',
    description='HTTP Signatures plugin for HTTPie.',
    version='0.1.1',
    author="Mike Manuthu",
    author_email='mmanuthu@east36.co.ke',
    url='https://github.com/east36/httpie-http-signatures',
    download_url='https://github.com/east36/httpie-http-signatures',
    license="BSD",
    py_modules=['httpie_httpsig_auth'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_httpsig_auth = httpie_httpsig_auth:HTTPSignatureAuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.7.0',
        "six>=1.10.0",
        "httpsig-cffi>=15.0.0",
        "requests>=2.14.2"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Environment :: Plugins',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities',
        'Topic :: System :: Networking',
    ],
)
