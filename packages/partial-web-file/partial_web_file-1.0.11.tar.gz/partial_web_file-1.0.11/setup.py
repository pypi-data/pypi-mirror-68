from setuptools import setup, find_packages
 

desc = 'Utilities to get the partial content of the web file or to unarchive a single file from a huge remote web zip.'

setup(
    name='partial_web_file',
    version='1.0.11',
    url='https://github.com/alexappsnet/pypartialwebfile',
    license='MIT',
    author='Alex Malko',
    author_email='alex@alexapps.net',
    description=desc,
    packages=find_packages(exclude=['tests']),
    long_description=desc,
    long_description_content_type="text/plain"
)
