from .docs import MkdocsParse


def test_mkdocs():
    nav_mismatch = MkdocsParse().validate_path()
    if len(nav_mismatch):
        assert False, f"Mkdocs nav path incorrect/missing: {nav_mismatch}"


def test_title():
    nav_mismatch = MkdocsParse().validate_title()
    if len(nav_mismatch):
        assert False, f"Mkdocs nav_translations incorrect/missing: {nav_mismatch}"
