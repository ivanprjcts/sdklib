from setuptools import setup, find_packages
from sdklib import __version__


def read_file(filepath):
    with open(filepath) as f:
        return f.read()


EXCLUDE_FROM_PACKAGES = []


setup(
    name='sdklib',
    version=__version__,
    description='SDK helper library',
    long_description=read_file('README.rst'),
    author='Ivan Martin',
    author_email='ivanprjcts@gmail.com',
    url='https://github.com/ivanprjcts/sdklib',
    install_requires=read_file('requirements.txt').splitlines(),
    keywords=['sdk', 'api', 'REST', 'client', 'http', 'requests'],
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    zip_safe=False
)
