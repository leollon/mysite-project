"""
extra feature:
    such as, processing account registered notification content,
    send email to user and so on.
"""
from pathlib import Path


def get_notification(filename):
    file = Path(__file__).parent.joinpath(filename).as_posix()
    with open(file, "r") as f:
        return f.read()
