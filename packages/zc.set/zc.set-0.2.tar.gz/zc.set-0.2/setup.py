from setuptools import setup, find_packages


def read(filename):
    with open(filename) as f:
        return f.read()


setup(
    name="zc.set",
    version="0.2",
    license='ZPL 2.1',
    long_description='\n\n'.join([
        read('CHANGES.txt'),
        read('src/zc/set/README.txt'),
    ]),
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    description="Persistent sets are persistent objects that have the API of standard Python sets",
    url="https://github.com/zopefoundation/zc.set/",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['zc'],
    include_package_data=True,
    install_requires=[
        'setuptools',
        'persistent',
    ],
    extras_require=dict(
        test=[
            'ZODB[test]',
            'zope.app.folder',
        ],
    ),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
    ],
    test_suite='zc.set.tests.test_suite',
    zip_safe=False,
)
