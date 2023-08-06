from setuptools import setup

with open('README.rst') as readme_file:
    README = readme_file.read()

setup(
    name='tc-player',
    description='A Time Clickers automaton.',
    url='https://github.com/colons/tc',
    author='colons',
    author_email='pypi@colons.co',
    version='1.0.1',
    license='LICENSE',
    platforms=['any'],
    packages=['tc'],
    scripts=['scripts/tc'],
    long_description=README,
    classifiers=[
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'selenium<4',
    ],
    include_package_data=True,
)
