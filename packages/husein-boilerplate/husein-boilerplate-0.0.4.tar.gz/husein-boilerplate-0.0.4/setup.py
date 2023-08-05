import setuptools


__packagename__ = 'husein-boilerplate'

setuptools.setup(
    name = __packagename__,
    packages = setuptools.find_packages(),
    version = '0.0.4',
    python_requires = '>=3.7.*',
    description = 'Boilerplate for Husein',
    author = 'huseinzol05',
    author_email = 'husein.zol05@gmail.com',
    url = 'https://github.com/huseinzol05/husein-boilerplate',
    install_requires = ['emoji', 'gensim'],
    license = 'MIT',
    classifiers = [
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
