# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
        name='facturacion_electronica',
        version='0.11.4',
        packages=find_packages(),
        package_data={'facturacion_electronica': ['xsd/*.xsd']},
        install_requires=[
            'lxml',
            'cryptography>=2.9.1',
            'pyOpenSSL',
            'certifi',
            'pytz',
            'pdf417gen>=0.6.0',
            'suds-jurko',
            'urllib3==1.24.3',
            'requests==2.21.0',
        ],
        author='Daniel Santibáñez Polanco',
        author_email='dansanti@gmail.com',
        url='https://gitlab.com/dansanti/facturacion_electronica',
        license='GPLV3+',
        long_description='Módulo de Facturación Electrónica Chilena',
        classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Programming Language :: Python :: 3.6',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Environment :: Console',
        ]
       )
