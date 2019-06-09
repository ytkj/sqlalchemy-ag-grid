# sqlalchemy-ag-grid
SQLAlchemy Query class suitable for AgGrid request.
This library is server-side counter part for [ag-grid-axios](https://www.npmjs.com/package/@ytkj/ag-grid-axios).

## Installation

`pip install sqlalchemy_ag_grid`

## Usage

`sqlalchemy_ag_grid` is effective in webapp with
`SQLAlchemy` and `Flask` and `AgGrid`.

1. create `db`.

    ```python
    from flask_sqlalchemy import SQLAlchemy
    from sqlalchemy_ag_grid import SortFilterQuery

    db = SQLAlchemy(query_class=SortFilterQuery)
    ```
    
1. define `Model` class
    
    ```python
    import sqlalchemy as sa

    class ItemMapper(db.Model):
    
        __tablename__: str = 'item'
    
        id = sa.Column(sa.Integer, primary_key=True)
        text1 = sa.Column(sa.String, nullable=False)
        text2 = sa.Column(sa.String, nullable=False)
        number1 = sa.Column(sa.Integer, nullable=False)
        number2 = sa.Column(sa.Integer, nullable=False)
    ```

1. define `Flask` application
    
    ```python
    from flask import Flask

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    ```

1. query from 'item' table with filter and sort condition.
    
    ```python
    from flask import request

    @app.route('/api/grid[<int:start_row>:<int:end_row>]')
    def get_grid(start_row: int, end_row: int):
 
        items = ItemMapper.query \
            .sort_filter_by_args(ItemMapper, args) \
            .offset(start_row) \
            .limit(end_row - start_row) \
            .all()
        
        # return response
    ``` 
    