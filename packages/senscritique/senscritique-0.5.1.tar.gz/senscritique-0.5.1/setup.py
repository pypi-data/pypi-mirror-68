from distutils.core import setup

# noinspection PyUnresolvedReferences
import setuptools

setup(
    name='senscritique',
    packages=['senscritique'],
    install_requires=[
        'beautifulsoup4',
        'requests',
        'lxml',
    ],
    version='0.5.1',
    description='SensCritique Takeout on PyPI',
    long_description='Export your data from SensCritique.com, similarly to Google Takeout.',
    long_description_content_type='text/x-rst',
    author='Wok',
    author_email='wok@tuta.io',
    url='https://github.com/woctezuma/SensCritique-Takeout',
    download_url='https://github.com/woctezuma/SensCritique-Takeout/archive/0.5.1.tar.gz',
    keywords=['senscritique', 'takeout', 'takeaway'],
    classifiers=[
        'Topic :: Games/Entertainment',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: French',
    ],
)
