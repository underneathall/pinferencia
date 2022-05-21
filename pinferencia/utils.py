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
    try:
        from IPython.lib.pretty import pretty

        return pretty(type_hint)
    except Exception:
        type_hint_name = ""
        if hasattr(type_hint, "__name__"):
            type_hint_name = type_hint.__name__
        if str(type_hint).startswith(type_hint_name):
            type_hint_name = str(type_hint)
        return type_hint_name
