from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='onnlogger',
    version='0.0.6',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['onnlogger'],
    url='http://oznetnerd.com',
    license='',
    author='Will Robinson',
    author_email='will@oznetnerd.com',
    description='Convenience module for logging'
)
