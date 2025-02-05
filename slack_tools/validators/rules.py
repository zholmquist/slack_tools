from dataclasses import dataclass
from typing import Any


class Rule:
    pass


@dataclass
class RuleViolation:
    """Rule violation."""

    field_name: str
    field_value: Any
    message: str

    def __str__(self) -> str:
        return f'- `{self.field_name}`: {self.message}'


class Constraints:
    """Constraints for a value."""

    min_length: int | None = None
    max_length: int | None = None

    def __init__(
        self,
        min_length: int | None = None,
        max_length: int | None = None,
    ):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, cls_name: str, field_name: str, value: Any):
        violations: list[RuleViolation] = []

        value_length = len(value) if isinstance(value, str) else len(str(value))
        if self.min_length is not None:
            if value_length < self.min_length:
                violations.append(
                    RuleViolation(
                        field_name=field_name,
                        field_value=value,
                        message=f'Too short. Minimum length is {self.min_length}.',
                    )
                )
        if self.max_length is not None:
            if value_length > self.max_length:
                violations.append(
                    RuleViolation(
                        field_name=field_name,
                        field_value=value,
                        message=f'Too long. Maximum length is {self.max_length}.',
                    )
                )
        if violations:
            raise ValueError(
                '\n'.join(f'\n{cls_name}:\n\t{violation!s}' for violation in violations)
            )
