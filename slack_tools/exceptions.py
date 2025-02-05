class BaseSlackToolsError(Exception):
    """Base exception for all slack_tools errors."""

    pass


class ValidationError(BaseSlackToolsError):
    """Raised when validation fails for block schemas."""

    pass


class LengthValidationError(ValidationError):
    """Raised when field length validation fails."""

    def __init__(
        self,
        field_name: str,
        value_length: int,
        min_length: int | None = None,
        max_length: int | None = None,
    ):
        if min_length is not None and value_length < min_length:
            message = (
                f'{field_name}: Length {value_length} is less than minimum {min_length}'
            )
        elif max_length is not None and value_length > max_length:
            message = (
                f'{field_name}: Length {value_length} exceeds maximum {max_length}'
            )
        else:
            message = f'{field_name}: Invalid length {value_length}'
        super().__init__(message)


class BlockKitError(BaseSlackToolsError):
    """Base exception for all BlockKit-related errors."""

    pass


class ActionHandlerError(BaseSlackToolsError):
    """Raised when there are issues with action handling."""

    pass


class TemplateError(BaseSlackToolsError):
    """Raised when there are issues with template rendering."""

    pass


class MarkdownError(BaseSlackToolsError):
    """Raised when there are issues with markdown formatting."""

    pass
