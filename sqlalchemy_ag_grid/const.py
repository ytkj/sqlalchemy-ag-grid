from .util import Const

c = Const()
c.sort_type = Const()
c.filter_type = Const()
c.filter_category = Const()
c.query = Const()

c.sort_type.ASC = 'asc'
c.sort_type.DESC = 'desc'

c.filter_category.TEXT = 'text'
c.filter_category.NUMBER = 'number'
c.filter_category.RANK = 'rank'

c.filter_type.EQUALS = 'equals'
c.filter_type.NOT_EQUAL = 'notEqual'
c.filter_type.STARTS_WITH = 'startsWith'
c.filter_type.ENDS_WITH = 'endsWith'
c.filter_type.CONTAINS = 'contains'
c.filter_type.NOT_CONTAINS = 'notContains'
c.filter_type.LESS_THAN = 'lessThan'
c.filter_type.LESS_THAN_OR_EQUAL = 'lessThanOrEqual'
c.filter_type.GREATER_THAN = 'greaterThan'
c.filter_type.GREATER_THAN_OR_EQUAL = 'greaterThanOrEqual'
c.filter_type.IN_RANGE = 'inRange'
c.filter_type.TOP = 'top'

c.query.SORT_COL_ID = 'sortColId'
c.query.SORT_TYPE = 'sortType'
c.query.FILTER_COL_ID = 'filterColId'
c.query.FILTER_TYPE = 'filterType'
c.query.FILTER_WORD = 'filterWord'
c.query.FILTER_TO = 'filterTo'
c.query.FILTER_CATEGORY = 'filterCategory'
