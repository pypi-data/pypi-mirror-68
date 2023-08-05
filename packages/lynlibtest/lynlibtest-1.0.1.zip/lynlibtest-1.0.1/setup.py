# from distutils.core import setup
from setuptools import setup


def readme_read():
    with open("README.rst", encoding="utf-8") as rstr:
        return rstr.read()


setup(name="lynlibtest", version="1.0.1", description="this is lyn's first lib123", packages=["onelib"],
      py_modules=["Tool"], author="Lyn", author_email="lyn207@163.com", url= "https://github.com/OldboyFzZF",
      long_description=readme_read(), license="MIT")
