import pytest


def test_already_registered(json_model, json_model_kserve_service):
    with pytest.raises(Exception) as exc:
        json_model_kserve_service.register(
            model_name="json",
            model=json_model,
            version_name="v1",
            entrypoint="predict",
            metadata={},
        )
    assert "[Model Register] v1 already registered." == str(exc.value)
