import os
import setuptools

_SHORT_DESCRIPTION = \
    "A Mistune renderer that embeds images into the final document."

_APP_PATH = os.path.dirname(__file__)

with open(os.path.join(_APP_PATH, 'mei', 'resources', 'README.rst')) as f:
    _LONG_DESCRIPTION = f.read()

with open(os.path.join(_APP_PATH, 'mei', 'resources', 'requirements.txt')) as f:
    _REQUIREMENTS = [s.strip() for s in f if s.strip() != '']

with open(os.path.join(_APP_PATH, 'mei', 'resources', 'version.txt')) as f:
    _VERSION = f.read().strip()

setuptools.setup(
    name="markdown-embedimages",
    version=_VERSION,
    description=_SHORT_DESCRIPTION,
    long_description=_LONG_DESCRIPTION,
    classifiers=[],
    keywords='mistune markdown',
    author='Dustin Oprea',
    author_email='myselfasunder@gmail.com',
    # url="",
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    package_data={
        'mei': [
            'resources/README.rst',
            'resources/requirements.txt',
        ],
    },
    scripts=[
    ],
    install_requires=_REQUIREMENTS,
)
