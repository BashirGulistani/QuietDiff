from quietdiff.diff import diff_tables
from quietdiff.io import Table


def test_basic_diff():
    left = Table(
        name="a.csv",
        columns=["id", "name", "total"],
        rows=[
            {"id": "1", "name": "A", "total": "10.00"},
            {"id": "2", "name": "B", "total": "20.00"},
        ],
    )
    right = Table(
        name="b.csv",
        columns=["id", "name", "total"],
        rows=[
            {"id": "1", "name": "A", "total": "10.01"},
            {"id": "3", "name": "C", "total": "30.00"},
        ],
    )

    d = diff_tables(left, right, keys=["id"], tolerance=0.02)
    assert len(d.added) == 1
    assert len(d.removed) == 1
    assert len(d.changed) == 0
