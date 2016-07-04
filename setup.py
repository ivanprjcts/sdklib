from setuptools import setup, find_packages


EXCLUDE_FROM_PACKAGES = []

REQUIRES = ["urllib3 >= 1.10"]

setup(
    name='sdklib',
    version='1.2',
    description='SDK helper library',
    author='Ivan Martin',
    author_email='ivanprjcts@gmail.com',
    url='https://github.com/ivanprjcts/sdklib',
    install_requires=REQUIRES,
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
