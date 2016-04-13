from setuptools import setup, find_packages


EXCLUDE_FROM_PACKAGES = []

REQUIRES = ["urllib3 >= 1.10"]

setup(
    name='sdklib',
    version='1.0',
    description='SDK helper library',
    author='Ivan Martin',
    author_email='ivanprjcts@gmail.com',
    url='https://github.com/ivanprjcts/sdklib',
    install_requires=REQUIRES,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    zip_safe=False
)
