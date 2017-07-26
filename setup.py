from setuptools import setup


setup(
    name='httpie-httpsig-auth',
    description='HTTP Signatures plugin for HTTPie.',
    version='0.1.0',
    author='Mike Manuthu',
    author_email='mmanuthu@east36.co.ke',
    license='MIT',
    py_modules=['httpie_httpsig_auth'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_httpsig_auth = httpie_httpsig_auth:HTTPSignatureAuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.7.0',
        "six",
        "httpsig_cffi",
        "requests>=2.14.2"
    ],
    classifiers=[
        'Development Status :: Beta',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
