from kabooki.pipes import batch, keep, same, transform, unbatch
from test.tests import check, validate


def test_branch(): (
    (i for i in range(3))
    - same()
    + [
        transform(lambda a: a + 1)
        > validate(iter([
            lambda i: check(i == 1),
            lambda i: check(i == 2),
            lambda i: check(i == 3),
        ])),

        transform(lambda a: a + 2)
        > validate(iter([
            lambda i: check(i == 2),
            lambda i: check(i == 3),
            lambda i: check(i == 4),
        ]))
    ]
)


def test_keep(): (
    (i for i in range(3))
    - keep(lambda i: i > 0)
    > validate(iter([
        lambda i: check(i == 1, i),
        lambda i: check(i == 2, i),
    ]))
)


def test_batch(): (
    (i for i in range(3))
    - batch(batch_size=2)
    > validate(iter([
        lambda i: check(i == [0, 1]),
        lambda i: check(i == [2]),
    ]))
)


def test_unbatch():
    def v(l): assert l == [0, 1, 2]
    (
        (i for i in range(3))
        - batch(batch_size=2)
        - unbatch()
        > validate(iter([
            lambda i: check(i == 0),
            lambda i: check(i == 1),
            lambda i: check(i == 2),
        ]))
    )
