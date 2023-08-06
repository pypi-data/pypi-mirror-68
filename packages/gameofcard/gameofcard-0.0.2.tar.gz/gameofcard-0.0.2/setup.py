from distutils.core import setup

with open("README", "r") as fh:
    long_description = fh.read()

setup(
    name='gameofcard',
    packages=['gameofcard'],
    version='0.0.2',
    description='Just a humble implementation of different card games.',
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    author='EPgg92',
    author_email='poggio.enzo@gmail.com',
    url='https://github.com/EPgg92/gameofcard/releases/tag/0.0.2',
    download_url='https://github.com/EPgg92/gameofcard/archive/0.0.2.tar.gz',
    keywords=['card', 'game'],
    classifiers=["Programming Language :: Python :: 3",
                 "Operating System :: OS Independent", ],
    # python_requires='>=3.6',
)
