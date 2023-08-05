from setuptools import setup, find_packages

version = '1.0'

requires = [
    'setuptools',
    'collective.beaker',
    'beaker',
    'Zope2',
    'zope.interface'
]

setup(
    name='Products.BeakerZopeSessionManager',
    version=version,
    description="Zope4 session implementation using Beaker",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords='zope sessions beaker',
    author='Gisoldo, Gabriel Diniz',
    author_email='gabrielgisoldi@gmail.com',
    url='https://github.com/gabrielgisoldo/Products.BeakerZopeSessionManager',
    license='MIT',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    python_requires='>=3.7'
)
