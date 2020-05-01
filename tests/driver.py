from flask import Flask
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy_ag_grid import SortFilterQuery

db = SQLAlchemy(query_class=SortFilterQuery)


class ItemMapper(db.Model):

    __tablename__: str = 'item'

    id = sa.Column(sa.Integer, primary_key=True)
    text1 = sa.Column(sa.String, nullable=False)
    text2 = sa.Column(sa.String, nullable=False)
    number1 = sa.Column(sa.Integer, nullable=False)
    number2 = sa.Column(sa.Integer, nullable=False)


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db.init_app(app)
