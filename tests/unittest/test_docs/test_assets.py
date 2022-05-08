from .docs import AssetsParse


def test_assets():
    assets_mismatch_info = AssetsParse().validate_path()
    if len(assets_mismatch_info):
        assert False, f"Assets path not match: {assets_mismatch_info}"
