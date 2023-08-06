from setuptools import setup

VERSION = '0.1.9'

setup(
    name='zucked',
    version=VERSION,
    py_modules=['zucked'],
    url='https://github.com/Jordan-Milne/zucked',
    download_url='https://github.com/Jordan-Milne/zucked'.format(VERSION),
    license='MIT',
    author='Jordan Milne',
    author_email='jordan.milne2@gmail.com',
    description='Python library for parsing through facebook messenger data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    python_requires=">=3.6",
    setup_requires=["setuptools>=38.6.0"],
    classifiers=[
        'Development Status :: 4 - Beta',

    ]
)
