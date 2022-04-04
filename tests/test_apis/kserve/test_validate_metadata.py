import pytest


@pytest.mark.parametrize(
    "metadata",
    [{"inputs": {"a": 1}}, {"outputs": {"a": 1}}, {"platform": {"a": 1}}, []],
)
def test_invalid_metadata(json_model, json_model_kserve_service, metadata):
    with pytest.raises(Exception) as exc:
        json_model_kserve_service.register(
            model_name="json",
            model=json_model,
            version_name="v2",
            entrypoint="predict",
            metadata=metadata,
        )
    assert "Registration Failed" in str(exc.value)
