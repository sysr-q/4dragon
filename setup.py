from setuptools import setup

if __name__ != "__main__":
    import sys
    sys.exit(1)

kw = {
    "name": "4dragon",
    "version": "1.0-dev",
    "description": "Turn any post on /b/ into a dragon slaying match.",
    "long_description": "",
    "url": "https://github.com/plausibility/4dragon",
    "author": "plausibility",
    "author_email": "chris@gibsonsec.org",
    "license": "MIT",
    "packages": ["fourdragon"],
    "install_requires": [
        "4ch",
    ],
    "zip_safe": False,
}

if __name__ == "__main__":
    setup(**kw)
