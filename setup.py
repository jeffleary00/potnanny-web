from setuptools import setup

setup(
    name='potnanny-api',
    version='0.2.6',
    packages=['potnanny_api'],
    include_package_data=True,
    description='Part of the Potnanny greenhouse controller application. Contains Flask REST API and basic web interface.',
    author='Jeff Leary',
    author_email='potnanny@gmail.com',
    url='https://github.com/jeffleary00/potnanny-api',
    install_requires=[
        'requests',
        'passlib',
        'sqlalchemy',
        'marshmallow',
        'flask',
        'flask-restful',
        'flask-jwt-extended',
        'flask-wtf',
        'potnanny-core==0.2.9',
    ],
)
