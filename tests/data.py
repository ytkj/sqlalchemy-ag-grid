import random

words = [
    'alpha',
    'bravo',
    'charlie',
    'delta',
    'echo',
]
numbers = [1, 2, 3, 4, 5]

data = []
for w1 in words:
    for w2 in words:
        for n1 in numbers:
            for n2 in numbers:
                data.append(dict(
                    text1=w1,
                    text2=w2,
                    number1=n1,
                    number2=n2,
                ))
random.shuffle(data)
for i, d in enumerate(data):
    d['id'] = i
