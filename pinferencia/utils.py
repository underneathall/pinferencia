import typing

from pydantic import BaseModel, HttpUrl, ValidationError


class URLValidator(BaseModel):
    url: HttpUrl


def get_type_hint_name(type_hint: object) -> str:
    """Convert type hint to its literal name

    Args:
        type_hint (object): type hint class

    Returns:
        str: literal name of the type hint

    Example:
        > get_type_hint_name(typing.List[str])
        "typing.List[str]"
        > get_type_hint_name(list)
        "list"
    """
    return typing._type_repr(type_hint)


def validate_url(url):
    try:
        URLValidator(url=url)
        return url
    except ValidationError:
        return False
