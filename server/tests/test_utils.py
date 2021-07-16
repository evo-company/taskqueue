from itertools import islice

from taskqueue.server.worker import delay_gen


def test_delay_gen():
    assert list(islice(delay_gen(), 0, 9)) == [1, 2, 4, 8, 16, 32, 64, 64, 64]
