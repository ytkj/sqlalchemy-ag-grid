# sqlalchemy-ag-grid
SQLAlchemy Query class suitable for AgGrid request.
This library is server-side counter part for [ag-grid-axios](https://www.npmjs.com/package/@ytkj/ag-grid-axios).

## Installation

`pip install sqlalchemy_ag_grid`

## Usage

`sqlalchemy_ag_grid` is effective in webapp with
`SQLAlchemy` and `Flask` and `AgGrid`.

### Basic usage

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
        name = sa.Column(sa.String, nullable=False)
        age = sa.Column(sa.Integer, nullable=False)
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
 
        # query records with filter and sort condition
        rows_this_block = ItemMapper.query \
            .sort_filter_by_args(ItemMapper, request.args) \
            .offset(start_row) \
            .limit(end_row - start_row) \
            .all()
         
        # number of records with filter condition
        last_row = ItemMapper.query.filter_count_by_args(ItemMapper, request.args)
        
        # return response
    ``` 
    
    - example GET request and SQL query
        - `GET /api/grid[0:20]?sortColId=age&sortType=asc&filterColId=name&filterType=startsWith&filterWord=a&filterCategory=text`
        - `select * from item where name like 'a%' order by age offset 0 limit 20`

### Advanced usage

- POST/PUT request

    ```python
    from flask import request

    @app.route('/api/grid', methods=['PUT'])
    def put_grid():
 
        items = ItemMapper.query \
            .sort_filter_by_json(ItemMapper, request.json()) \
            .all()
        
        # return response
    ```

- mapping GET request parameter to DB field name

    ```python
    @app.route('/api/grid[<int:start_row>:<int:end_row>]')
    def get_grid(start_row: int, end_row: int):

        mapper = {
            'lastName': 'last_name',
            'firstName': 'first_name,'
        }
      
        items = ItemMapper.query \
            .sort_filter_by_args(ItemMapper, request.args, mapper) \
            .offset(start_row) \
            .limit(end_row) \
            .all()
    ```
   
    - example GET request and SQL query
        - `GET /api/grid[0:20]?sortColId=firstName&sortType=asc&sortColId=lastName&sortType=asc`
        - `select * from item order by first_name, last_name offset 0 limit 20`
  

## API

### `SortFilterQuery#sort_filter_by_args()`

```python
def sort_filter_by_args(
    cls: db.Model,
    args: werkzeug.datastructures.ImmutableMultiDict,
    mapper: Dict[str, str] = None
) -> SortFilterQuery:
    pass
```

### `SortFilterQuery#sort_filter_by_json()`

```python
def sort_filter_by_json(
    cls: db.Model,
    json: Dict[str, List[str]],
    mapper: Dict[str, str] = None
) -> SortFilterQuery:
    pass
```

### `SortFilterQuery#filter_count_by_args()`

```python
def filter_count_by_args(
    cls: db.Model,
    args: werkzeug.datastructures.ImmutableMultiDict,
    mapper: Dict[str, str] = None
) -> int:
    pass
```

### `SortFilterQuery#filter_count_by_json()`

```python
def filter_count_by_json(
    cls: db.Model,
    json: Dict[str, List[str]],
    mapper: Dict[str, str] = None
) -> int:
    pass
```
