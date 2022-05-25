import pytest

from pinferencia.utils import validate_url


@pytest.mark.parametrize(
    "url_and_expect_result",
    [
        ("http://abc.com", "http://abc.com"),
        ("http://abc.com:8080", "http://abc.com:8080"),
        ("http://abc.com/def/ghi/", "http://abc.com/def/ghi/"),
        ("http://abc.com:8080/def/ghi/", "http://abc.com:8080/def/ghi/"),
        ("https://abc.com", "https://abc.com"),
        ("https://abc.com:8080", "https://abc.com:8080"),
        ("https://abc.com/def/ghi", "https://abc.com/def/ghi"),
        ("https://abc.com:8080/def/ghi/", "https://abc.com:8080/def/ghi/"),
        ("https://1.1.1.1", "https://1.1.1.1"),
        ("https://1.1.1.1:8080", "https://1.1.1.1:8080"),
        ("https://1.1.1.1/def/ghi", "https://1.1.1.1/def/ghi"),
        ("https://1.1.1.1:8080/def/ghi/", "https://1.1.1.1:8080/def/ghi/"),
        ("abc.def.cccccc", False),
        ("abc.com", False),
        ("http://abc.com:88888", False),
        ("http://1.1.1.1.1", False),
    ],
)
def test(url_and_expect_result):
    url, expected_result = url_and_expect_result
    assert validate_url(url) == expected_result
