from typing import List, Any, Dict
from itertools import zip_longest, chain
from flask_sqlalchemy import BaseQuery
from sqlalchemy import Column
from werkzeug.datastructures import ImmutableMultiDict

from .const import c


def _sort_criterion(cls: Any, col: str, s_type: str):

    column: Column = getattr(cls, col)

    if s_type == c.sort_type.ASC:
        return column.asc()

    elif s_type == c.sort_type.DESC:
        return column.desc()

    else:
        return None


def _filter_criterion(cls: Any, col: str, f_category: str, f_type: str, f_word: str, f_to: str):
    column: Column = getattr(cls, col)

    if f_category == c.filter_category.TEXT:

        if f_type == c.filter_type.EQUALS:
            return [column == f_word]

        elif f_type == c.filter_type.NOT_EQUAL:
            return [column != f_word]

        elif f_type == c.filter_type.STARTS_WITH:
            return [column.like(f_word + '%')]

        elif f_type == c.filter_type.ENDS_WITH:
            return [column.like('%' + f_word)]

        elif f_type == c.filter_type.CONTAINS:
            return [column.contains(f_word)]

        elif f_type == c.filter_type.NOT_CONTAINS:
            return [~column.contains(f_word)]

        else:
            return None

    elif f_category == c.filter_category.NUMBER:
        try:
            f_number = float(f_word)
        except ValueError:
            return None

        if f_type == c.filter_type.EQUALS:
            return [column == f_number]

        elif f_type == c.filter_type.NOT_EQUAL:
            return [column != f_number]

        elif f_type == c.filter_type.LESS_THAN:
            return [column < f_number]

        elif f_type == c.filter_type.LESS_THAN_OR_EQUAL:
            return [column <= f_number]

        elif f_type == c.filter_type.GREATER_THAN:
            return [column > f_number]

        elif f_type == c.filter_type.GREATER_THAN_OR_EQUAL:
            return [column >= f_number]

        elif f_type == c.filter_type.IN_RANGE and f_to is not None:
            try:
                f_number_to = float(f_to)
            except ValueError:
                return None
            return [column >= f_number, column <= f_number_to]

        else:
            return None

    elif f_category == c.filter_category.RANK:
        try:
            f_number = float(f_word)
        except ValueError:
            return None

        if f_type == c.filter_type.TOP:
            return None  # in case 'top', filter by SQL's LIMIT.

        elif f_type == c.filter_type.GREATER_THAN:
            return [column > f_number]

        elif f_type == c.filter_type.GREATER_THAN_OR_EQUAL:
            return [column >= f_number]

        else:
            return None

    else:
        return None


def _map_col_id(requested_col_ids: List[str], mapper: Dict[str, str]) -> List[str]:

    def map_if_exist(s: str, d: Dict[str, str]):
        if s in d:
            return d[s]
        else:
            return s

    return [map_if_exist(col_id, mapper) for col_id in requested_col_ids]


class SortFilterQuery(BaseQuery):

    def sort_filter_by_args(self, cls: Any, args: ImmutableMultiDict, mapper: Dict[str, str] = None):
        """
        querying based on `ImmutableMultiDict` type GET parameters, or `flask.request.args`.

        :param cls: model class which extends `flask_sqlalchemy.db.Model`.
        :param args: `ImmutableMultiDict` type GET parameters.
        :param mapper: dict associating GET parameter name (=dict's key) and model class field name (=dict's value).
        :return: self
        """
        return self.sort_filter(
            cls=cls,
            sort_col_id=args.getlist(c.query.SORT_COL_ID),
            sort_type=args.getlist(c.query.SORT_TYPE),
            filter_col_id=args.getlist(c.query.FILTER_COL_ID),
            filter_type=args.getlist(c.query.FILTER_TYPE),
            filter_word=args.getlist(c.query.FILTER_WORD),
            filter_to=args.getlist(c.query.FILTER_TO),
            filter_category=args.getlist(c.query.FILTER_CATEGORY),
            mapper=mapper
        )

    def sort_filter_by_json(self, cls: Any, json: dict, mapper: Dict[str, str] = None):
        """
        querying base on dict type request form, or `flask.request.get_json()`.

        :param cls: model class which extends `flask_sqlalchemy.db.Model`.
        :param json: dict type key-value (request form as JSON).
        :param mapper: dict associating form field name (=dict's key) and model class field name (=dict's value).
        :return: self
        """
        return self.sort_filter(
            cls=cls,
            sort_col_id=json.get(c.query.SORT_COL_ID, []),
            sort_type=json.get(c.query.SORT_TYPE, []),
            filter_col_id=json.get(c.query.FILTER_COL_ID, []),
            filter_type=json.get(c.query.FILTER_TYPE, []),
            filter_word=json.get(c.query.FILTER_WORD, []),
            filter_to=json.get(c.query.FILTER_TO, []),
            filter_category=json.get(c.query.FILTER_CATEGORY, []),
            mapper=mapper
        )

    def filter_count_by_args(self, cls: Any, args: ImmutableMultiDict, mapper: Dict[str, str] = None):
        """
        querying based on `ImmutableMultiDict` type GET parameters, or `flask.request.args`,
        and return number of records.

        :param cls: model class which extends `flask_sqlalchemy.db.Model`.
        :param args: `ImmutableMultiDict` type GET parameters.
        :param mapper: dict associating GET parameter name (=dict's key) and model class field name (=dict's value).
        :return: self
        """
        return self.filter_count(
            cls=cls,
            filter_col_id=args.getlist(c.query.FILTER_COL_ID),
            filter_type=args.getlist(c.query.FILTER_TYPE),
            filter_word=args.getlist(c.query.FILTER_WORD),
            filter_to=args.getlist(c.query.FILTER_TO),
            filter_category=args.getlist(c.query.FILTER_CATEGORY),
            mapper=mapper
        )

    def filter_count_by_json(self, cls: Any, json: dict, mapper: Dict[str, str] = None):
        """
        querying base on dict type request form, or `flask.request.get_json()`,
        and return number of records.

        :param cls: model class which extends `flask_sqlalchemy.db.Model`.
        :param json: dict type key-value (request form as JSON).
        :param mapper: dict associating form field name (=dict's key) and model class field name (=dict's value).
        :return: self
        """
        return self.filter_count(
            cls=cls,
            filter_col_id=json.get(c.query.FILTER_COL_ID, []),
            filter_type=json.get(c.query.FILTER_TYPE, []),
            filter_word=json.get(c.query.FILTER_WORD, []),
            filter_to=json.get(c.query.FILTER_TO, []),
            filter_category=json.get(c.query.FILTER_CATEGORY, []),
            mapper=mapper
        )

    def sort_filter(
            self,
            cls: Any,
            sort_col_id: List[str],
            sort_type: List[str],
            filter_col_id: List[str],
            filter_type: List[str],
            filter_word: List[str],
            filter_to: List[str],
            filter_category: List[str],
            mapper: Dict[str, str]
    ):
        if mapper is None:
            mapper = {}
        query = self._filter(
            cls, _map_col_id(filter_col_id, mapper), filter_type, filter_word, filter_to, filter_category
        )

        # sort
        if len(sort_col_id) > 0:

            criterion = [
                _sort_criterion(cls, s_col, s_type) for s_col, s_type in zip(
                    _map_col_id(sort_col_id, mapper),
                    sort_type
                )
            ]

            # drop None
            criterion = [cr for cr in criterion if cr is not None]

            query = query.order_by(*criterion)

        return query

    def filter_count(
            self,
            cls: Any,
            filter_col_id: List[str],
            filter_type: List[str],
            filter_word: List[str],
            filter_to: List[str],
            filter_category: List[str],
            mapper: Dict[str, str]
    ):
        if mapper is None:
            mapper = {}
        return self._filter(
            cls, _map_col_id(filter_col_id, mapper), filter_type, filter_word, filter_to, filter_category
        ).count()

    def _filter(
            self,
            cls: Any,
            filter_col_id: List[str],
            filter_type: List[str],
            filter_word: List[str],
            filter_to: List[str],
            filter_category: List[str]
    ):
        query = self

        if len(filter_col_id) > 0:

            # other than 'top' filter
            criterion = [
                _filter_criterion(
                    cls,
                    f_col,
                    f_category,
                    f_type,
                    f_word,
                    f_to
                ) for f_col, f_category, f_type, f_word, f_to in zip_longest(
                    filter_col_id,
                    filter_category,
                    filter_type,
                    filter_word,
                    filter_to
                )
            ]

            # drop None
            criterion = [cr for cr in criterion if cr is not None]

            # flatten
            criterion = list(chain.from_iterable(criterion))

            query = query.filter(*criterion)

            # filter 'top'
            top_filters = [
                (f_col, f_word) for f_col, f_category, f_type, f_word, f_to in zip_longest(
                    filter_col_id,
                    filter_category,
                    filter_type,
                    filter_word,
                    filter_to
                ) if f_category == c.filter_category.RANK and f_type == c.filter_type.TOP
            ]
            if len(top_filters) > 0:
                for f_col, f_word in top_filters:
                    try:
                        f_number = float(f_word)
                    except ValueError:
                        continue

                    query = query.order_by(getattr(cls, f_col).desc()).limit(f_number).from_self()

        return query
