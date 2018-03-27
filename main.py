from decor import simplify


@simplify
class A:
    def __init__(self, a, b):
        pass

    def __str__(self):
        return 'blah'


a = A(1, 2)
print(a)
