from nose2.tools import such
from werkzeug.datastructures import ImmutableMultiDict

from .driver import db, app, ItemMapper
from .data import data, words

with such.A('sort_filter_by_args()') as it:

    @it.has_setup
    def setup():
        with app.app_context():
            db.create_all()
            db.session.execute(ItemMapper.__table__.insert(), data)
            db.session.commit()

    @it.has_teardown
    def teardown():
        with app.app_context():
            db.drop_all()

    @it.should('single sort asc')
    def test1():
        with app.app_context():
            args = ImmutableMultiDict([('sortColId', 'text1'), ('sortType', 'asc')])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = [i.text1 for i in items]
            answer = words * 125
            answer.sort()
            it.assertEqual(answer, target)

    @it.should('single sort desc')
    def test2():
        with app.app_context():
            args = ImmutableMultiDict([('sortColId', 'text1'), ('sortType', 'desc')])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = [i.text1 for i in items]
            answer = words * 125
            answer.sort(reverse=True)
            it.assertEqual(answer, target)

    @it.should('double sort asc, desc')
    def test3():
        with app.app_context():
            args = ImmutableMultiDict([
                ('sortColId', 'text1'),
                ('sortColId', 'number1'),
                ('sortType', 'asc'),
                ('sortType', 'desc'),
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = [(i.text1, i.number1) for i in items]
            answer = []
            for w in words:
                for n in [5, 4, 3, 2, 1]:
                    answer.extend([(w, n)] * 25)
            it.assertEqual(answer, target)

    @it.should('single filter text equals')
    def test4():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'text1'),
                ('filterType', 'equals'),
                ('filterWord', 'bravo'),
                ('filterCategory', 'text')
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = [i.text1 for i in items]
            answer = ['bravo'] * 125
            it.assertEqual(answer, target)

    @it.should('filter single text notEqual')
    def test5():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'text1'),
                ('filterType', 'notEqual'),
                ('filterWord', 'bravo'),
                ('filterCategory', 'text'),
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set([i.text1 for i in items])
            answer = set(words) - {'bravo'}
            it.assertEqual(answer, target)

    @it.should('filter single text startsWith')
    def test6():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'text1'),
                ('filterType', 'startsWith'),
                ('filterWord', 'b'),
                ('filterCategory', 'text'),
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set([i.text1 for i in items])
            answer = {'bravo'}
            it.assertEqual(answer, target)

    @it.should('filter single text endsWith')
    def test57():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'text1'),
                ('filterType', 'endsWith'),
                ('filterWord', 'o'),
                ('filterCategory', 'text'),
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set([i.text1 for i in items])
            answer = {'bravo', 'echo'}
            it.assertEqual(answer, target)

    @it.should('filter single text contains')
    def test7():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'text1'),
                ('filterType', 'contains'),
                ('filterWord', 'ch'),
                ('filterCategory', 'text'),
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set([i.text1 for i in items])
            answer = {'charlie', 'echo'}
            it.assertEqual(answer, target)

    @it.should('filter single text notContains')
    def test8():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'text1'),
                ('filterType', 'notContains'),
                ('filterWord', 'ch'),
                ('filterCategory', 'text'),
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set([i.text1 for i in items])
            answer = set(words) - {'charlie', 'echo'}
            it.assertEqual(answer, target)

    @it.should('filter single number equals')
    def test9():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'number1'),
                ('filterType', 'equals'),
                ('filterWord', 1),
                ('filterCategory', 'number')
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set([i.number1 for i in items])
            answer = {1}
            it.assertEqual(answer, target)

    @it.should('filter single number notEqual')
    def test10():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'number1'),
                ('filterType', 'notEqual'),
                ('filterWord', 1),
                ('filterCategory', 'number')
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set([i.number1 for i in items])
            answer = {2, 3, 4, 5}
            it.assertEqual(answer, target)

    @it.should('filter single number lessThan')
    def test11():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'number1'),
                ('filterType', 'lessThan'),
                ('filterWord', 3),
                ('filterCategory', 'number')
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set([i.number1 for i in items])
            answer = {1, 2}
            it.assertEqual(answer, target)

    @it.should('filter single number lessThanOrEqual')
    def test12():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'number1'),
                ('filterType', 'lessThanOrEqual'),
                ('filterWord', 3),
                ('filterCategory', 'number')
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set([i.number1 for i in items])
            answer = {1, 2, 3}
            it.assertEqual(answer, target)

    @it.should('filter single number greaterThan')
    def test13():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'number1'),
                ('filterType', 'greaterThan'),
                ('filterWord', 3),
                ('filterCategory', 'number')
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set([i.number1 for i in items])
            answer = {4, 5}
            it.assertEqual(answer, target)

    @it.should('filter single number greaterThanOrEqual')
    def test14():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'number1'),
                ('filterType', 'greaterThanOrEqual'),
                ('filterWord', 3),
                ('filterCategory', 'number')
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set([i.number1 for i in items])
            answer = {3, 4, 5}
            it.assertEqual(answer, target)

    @it.should('filter single number inRange')
    def test15():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'number1'),
                ('filterType', 'inRange'),
                ('filterWord', 2),
                ('filterTo', 4),
                ('filterCategory', 'number')
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set([i.number1 for i in items])
            answer = {2, 3, 4}
            it.assertEqual(answer, target)

    @it.should('filter single rank top')
    def test16():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'number1'),
                ('filterType', 'top'),
                ('filterWord', 100),
                ('filterCategory', 'rank'),
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set([i.number1 for i in items])
            answer = {5}
            it.assertEqual(answer, target)
            it.assertEqual(len(items), 100)

    @it.should('filter single rank greaterThan')
    def test17():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'number1'),
                ('filterType', 'greaterThan'),
                ('filterWord', 3),
                ('filterCategory', 'rank'),
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set([i.number1 for i in items])
            answer = {4, 5}
            it.assertEqual(answer, target)

    @it.should('filter single rank greaterThanOrEqual')
    def test18():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'number1'),
                ('filterType', 'greaterThanOrEqual'),
                ('filterWord', 3),
                ('filterCategory', 'rank'),
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set([i.number1 for i in items])
            answer = {3, 4, 5}
            it.assertEqual(answer, target)

    @it.should('filter double text equals and number greaterThan')
    def test19():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'text1'),
                ('filterType', 'equals'),
                ('filterWord', 'bravo'),
                ('filterCategory', 'text'),
                ('filterColId', 'number1'),
                ('filterType', 'greaterThan'),
                ('filterWord', 3),
                ('filterCategory', 'number'),
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target1 = set([i.text1 for i in items])
            answer1 = {'bravo'}
            target2 = set([i.number1 for i in items])
            answer2 = {4, 5}
            it.assertEqual(answer1, target1)
            it.assertEqual(answer2, target2)

    @it.should('filter double text equals and number inRange')
    def test20():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'text1'),
                ('filterType', 'equals'),
                ('filterWord', 'bravo'),
                ('filterTo', None),
                ('filterCategory', 'text'),
                ('filterColId', 'number1'),
                ('filterType', 'inRange'),
                ('filterWord', 2),
                ('filterTo', 4),
                ('filterCategory', 'number'),
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target1 = set([i.text1 for i in items])
            answer1 = {'bravo'}
            target2 = set([i.number1 for i in items])
            answer2 = {2, 3, 4}
            it.assertEqual(answer1, target1)
            it.assertEqual(answer2, target2)

    @it.should('filter double text equals and rank top')
    def test21():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'text1'),
                ('filterType', 'equals'),
                ('filterWord', 'bravo'),
                ('filterCategory', 'text'),
                ('filterColId', 'number1'),
                ('filterType', 'top'),
                ('filterWord', 10),
                ('filterCategory', 'rank'),
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = ['{0}{1}'.format(i.text1, i.number1) for i in items]
            answer = ['bravo5'] * 10
            it.assertEqual(answer, target)

    @it.should('filter double rank top and text equals')
    def test22():
        with app.app_context():
            args = ImmutableMultiDict([
                ('filterColId', 'number1'),
                ('filterType', 'top'),
                ('filterWord', '10'),
                ('filterCategory', 'rank'),
                ('filterColId', 'text1'),
                ('filterType', 'equals'),
                ('filterWord', 'bravo'),
                ('filterCategory', 'text'),
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = ['{0}{1}'.format(i.text1, i.number1) for i in items]
            answer = ['bravo5'] * 10
            it.assertEqual(answer, target)

    @it.should('filter and sort')
    def test23():
        with app.app_context():
            args = ImmutableMultiDict([
                ('sortColId', 'text1'),
                ('sortType', 'asc'),
                ('sortColId', 'number1'),
                ('sortType', 'desc'),
                ('filterColId', 'text1'),
                ('filterType', 'contains'),
                ('filterWord', 'ch'),
                ('filterCategory', 'text'),
                ('filterColId', 'number1'),
                ('filterType', 'greaterThan'),
                ('filterWord', 3),
                ('filterCategory', 'number'),
            ])
            items = ItemMapper.query.sort_filter_by_args(ItemMapper, args).all()
            target = set(['{0}{1}'.format(i.text1, i.number1) for i in items])
            answer = {'echo5', 'echo4', 'charlie5', 'charlie4'}
            it.assertEqual(answer, target)


it.createTests(globals())
