"""Intentional type violation retained for native type-checker migration.

Do not repair the typed call until its owning migration cycle replaces this fixture.

@layer: Tests (Fixtures)
@dependencies: type-checking validation fixture consumers
"""

# gate4_types: mypy type error — str passed where int expected
def typed_add(a: int, b: int) -> int:
    return a + b


wrong_call: int = typed_add("hello", "world")  # type: error
