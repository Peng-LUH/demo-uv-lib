from demo_uv_lib import add, greeting


def test_add():
    assert add(1, 2) == 3


def test_greeting_normal():
    assert greeting("Ada") == "Hello, Ada!"


def test_greeting_empty():
    assert greeting("  ") == "Hello!"
