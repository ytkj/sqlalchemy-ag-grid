import setuptools

install_requires = [
    'SQLAlchemy',
    'Werkzeug',
    'Flask-SQLAlchemy',
]

extras_require = {
    'test': [
        'nose2',
        'Flask',
    ]
}

setuptools.setup(
    name='sqlalchemy_ag_grid',
    version='0.0.3',
    describtion='SQLAlchemy Query class suitable for AgGrid request',
    url='https://github.com/ytkj/sqlalchemy-ag-grid',
    author='ytkj',
    author_email='y.kojima.1989@gmail.com',
    license='MIT',
    keywords='Flask SQLAlchemy AgGrid',
    install_requires=install_requires,
    test_requires=extras_require['test'],
    extras_require=extras_require,
    package_dir={
        'sqlalchemy_ag_grid': 'sqlalchemy_ag_grid',
    },
    packages=[
        'sqlalchemy_ag_grid',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
    ],
)
