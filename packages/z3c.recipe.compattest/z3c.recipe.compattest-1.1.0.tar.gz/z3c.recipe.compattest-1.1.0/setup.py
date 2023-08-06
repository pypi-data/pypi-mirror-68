import os
from setuptools import setup, find_packages


def read(path):
    with open(os.path.join(path)) as f:
        return f.read()

setup(
    name='z3c.recipe.compattest',
    version='1.1.0',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    description='Buildout recipe to create testrunners for testing '
                'compatibility with other packages',
    url='https://github.com/zopefoundation/z3c.recipe.compattest',
    long_description=(
        read('README.rst')
        + '\n\n'
        + read('CHANGES.rst')
    ),
    keywords="zope setuptools egg kgs",
    classifiers=[
        'Framework :: Zope :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
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
    ],
    license='ZPL 2.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['z3c', 'z3c.recipe'],
    install_requires=[
        'setuptools',
        'zc.buildout >= 2.0.0',
        'zc.recipe.testrunner >= 2.0.0',
    ],
    extras_require={
        'test': [
            # zope.dottedname is just used as a dummy package to demonstrate things
            # with, it's not actually imported
            'zope.dottedname',
            'zope.testing',
            'manuel',
            'six',
        ],
    },
    entry_points={
        'zc.buildout': ['default = z3c.recipe.compattest.recipe:Recipe'],
    },
    include_package_data=True,
    zip_safe=False,
    python_requires=', '.join([
        '>=2.7',
        '!=3.0.*',
        '!=3.1.*',
        '!=3.2.*',
        '!=3.3.*',
        '!=3.4.*',
    ]),
)
