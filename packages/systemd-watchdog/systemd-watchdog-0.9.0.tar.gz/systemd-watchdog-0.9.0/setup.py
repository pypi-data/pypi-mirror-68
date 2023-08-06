from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="systemd-watchdog",
    version="0.9.0",
    py_modules=["systemd_watchdog"],
    author="AaronDMarasco",
    author_email="systemd-watchdog@marascos.net",
    description="sd_notify and sd_watchdog_enabled functionality for writing Python daemons under systemd",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="sd_notify sd_watchdog_enabled systemd python3 watchdog",
    url="http://github.com/AaronDMarasco/systemd-watchdog/",
    project_urls={
        "Bug Tracker": "http://github.com/AaronDMarasco/systemd-watchdog/issues",
        "Documentation": "http://github.com/AaronDMarasco/systemd-watchdog/",
        "Source Code": "http://github.com/AaronDMarasco/systemd-watchdog/",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.5",
)
