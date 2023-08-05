from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='awesomedict',
    version='0.1.1',
    url='https://github.com/aayla-secura/awesomedict',
    author='AaylaSecura1138',
    author_email='aayla.secura.1138@gmail.com',
    description='No more KeyError! Set default values and filter via regex',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    zip_safe=False)
