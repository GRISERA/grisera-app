from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Grisera-api package'
LONG_DESCRIPTION = 'Graph Representation Integrating Signals for Emotion Recognition and Analysis (GRISERA) framework provides a persistent model for storing integrated signals and methods for its creation.'

# Setting up
setup(
    name="grisera",
    version=VERSION,
    author="",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['fastapi', 'uvicorn', 'requests', 'fastapi-utils', 'pydantic', 'starlette'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)