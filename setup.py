try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name = 'sdklib',
    version = '0.4.1',
    description = 'SDK helper library',
    author='Ivan Martin',
    author_email='ivanmar_91@hotmail.com',
    url='https://github.com/ivanprjcts/sdklib',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    py_modules = ['sdklib.util.parser', 'sdklib.sdklib', 'sdklib.util.bytearray', 'sdklib.util.urlvalidator',
                  'sdklib.util.timetizer'],
    packages=['sdklib', 'sdklib.util'],
)
