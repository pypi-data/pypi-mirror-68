try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name='doubao-config-sdk',
    version='1.0.0',
    author='biao.xu',
    author_email='biao.xu@baodanyun-inc.com',
    description='Doubao Configuration Center Python SDK',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.5",
    install_requires=['requests'],
    packages=['doubao_config'],
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
