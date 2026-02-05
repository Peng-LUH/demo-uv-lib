def add(a: float, b: float) -> float:
    return a + b


def greeting(name: str) -> str:
    name = name.strip()
    if not name:
        return "Hello!"
    return f"Hello, {name}!"
