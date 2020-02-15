from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='norm4phone',
    version='0.1.2',
    description='a tool to normalize different writing of phone numbers into standard format',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT License',
    url='https://github.com/xuxingya/norm4phone',
    author='xingya.xu',
    author_email='xingya.xu@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    package_data={'norm4phone':'iso3166Data.json'}
)