from setuptools import setup

setup(
    name="h",
    version="0.1",
    py_modules=["h"],
    install_requires=[
        'openai',
        'rich',
    ],
    entry_points={
        "console_scripts": ["h=h:main"],
    },
)
