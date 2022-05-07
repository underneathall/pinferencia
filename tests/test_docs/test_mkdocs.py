from .docs import MkdocsParse


def test_mkdocs():
    nav_translations_mismatch, nav_mismatch = MkdocsParse().validate_path()
    message = (
        "Mkdocs nav_translations title not match: "
        + f"{nav_translations_mismatch}.\n"
        if nav_translations_mismatch
        else ""
    )
    message += (
        f"Mkdocs nav path not match: {nav_mismatch}" if nav_mismatch else ""
    )
    if message:
        assert False, message
