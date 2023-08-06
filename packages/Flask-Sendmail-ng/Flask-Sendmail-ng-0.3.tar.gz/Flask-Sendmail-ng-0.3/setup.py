from setuptools import setup


setup(
    name='Flask-Sendmail-ng',
    version='0.3',
    url='http://github.com/ncrocfer/flask-sendmail-ng',
    license='BSD',
    author='Anthony Ford',
    author_email='ford.anthonyj@gmail.com',
    description='Flask extension for sendmail',
    long_description=__doc__,
    packages=['flask_sendmail'],
    test_suite='nose.collector',
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
    ],
    tests_require=[
        'nose',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
