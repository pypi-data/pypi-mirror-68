from setuptools import setup

setup(
    name = "actions-pipeline-example",
    version = "0.2.0",
    description = "Dummy project to test GitHub actions",
    url = "https://github.com/cognitedata/actions-pipeline-example",
    author = "Carlos",
    author_email = "carlos.pereira@cognite.com",
    packages = ["hello"],
    entry_points =  {
        "console_scripts": ["say-hello=hello.app:main"]
    }
)
