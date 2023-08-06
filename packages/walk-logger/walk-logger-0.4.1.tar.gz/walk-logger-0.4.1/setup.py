import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("walk-logger/__init__.py", "r") as file:
    regex_version = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'
    version = re.search(regex_version, file.read(), re.MULTILINE).group(1)



setup(
    name="walk-logger",
    version=version,
    packages=["walk-logger"],
    package_data={"walk-logger": ["__init__.pyi", "py.typed"]},
    description="Made Python logger Simple",
    long_description_content_type="text/x-rst",
    keywords=["walk-logger", "logging", "logger", "log"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: System :: Logging",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=[
        "colorama>=0.3.4 ; sys_platform=='win32'",
        "aiocontextvars>=0.2.0 ; python_version<'3.7'",
        "win32-setctime>=1.0.0 ; sys_platform=='win32'",
    ],
    extras_require={
        "dev": [
            "black>=19.3b0 ; python_version>='3.6'",
            "codecov>=2.0.15",
            "colorama>=0.3.4",
            "flake8>=3.7.7",
            "isort>=4.3.20",
            "tox>=3.9.0",
            "tox-travis>=0.12",
            "pytest>=4.6.2",
            "pytest-cov>=2.7.1",
            "Sphinx>=2.2.1",
            "sphinx-autobuild>=0.7.1",
            "sphinx-rtd-theme>=0.4.3",
        ]
    },
    python_requires=">=3.5",
)