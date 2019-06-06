import setuptools

install_requires = [
    'SQLAlchemy',
    'Werkzeug',
]

extras_require = {
    'test': [
        'nose2',
    ]
}

setuptools.setup(
    name='sqlalchemy_ag_grid',
    install_requires=install_requires,
    test_requires=extras_require['test'],
    extras_require=extras_require,
    package_dir={
        'sqlalchemy_ag_grid': 'sqlalchemy_ag_grid',
    },
    packages=[
        'sqlalchemy_ag_grid',
    ]
)
