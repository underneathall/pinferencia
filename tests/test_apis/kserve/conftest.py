import copy

import pytest

from pinferencia import Server


@pytest.fixture(scope="function")
def api():
    return "kserve"


@pytest.fixture(scope="function")
def json_model_kserve_service(
    json_model,
    api,
):
    service = Server(api=api)
    service.register(
        model_name="json",
        model=json_model,
        entrypoint="predict",
        metadata={},
    )
    service.register(
        model_name="json",
        model=json_model,
        version_name="v1",
        entrypoint="predict",
        metadata={},
    )
    return service


@pytest.fixture(scope="function")
def json_model_with_path_kserve_service(
    json_model_dir,
    json_model_path,
    json_model_handler,
    api,
):
    service = Server(api="kserve", model_dir=json_model_dir)
    service.register(
        model_name="json",
        model=json_model_path,
        handler=json_model_handler,
        entrypoint="predict",
        metadata={},
        load_now=False,
    )
    service.register(
        model_name="json",
        model=json_model_path,
        handler=json_model_handler,
        version_name="v1",
        entrypoint="predict",
        metadata={},
        load_now=False,
    )
    service.register(
        model_name="json",
        model=json_model_path,
        handler=json_model_handler,
        version_name="loaded",
        entrypoint="predict",
        metadata={},
    )
    return service


@pytest.fixture(scope="function")
def sum_product_model_kserve_service(
    sum_product_model,
    sum_product_model_metadata,
    api,
):
    service = Server(api=api)
    service.register(
        model_name="sum_prod",
        model=sum_product_model,
        entrypoint="predict",
        metadata=sum_product_model_metadata,
    )
    service.register(
        model_name="sum_prod",
        model=sum_product_model,
        version_name="v1",
        entrypoint="predict",
        metadata=sum_product_model_metadata,
    )
    return service


@pytest.fixture(scope="function")
def sum_product_model_kserve_v2_partial_output_service(
    sum_product_model,
    sum_product_model_metadata,
    api,
):
    service = Server(api=api)
    partial_output_meta = copy.deepcopy(sum_product_model_metadata)
    partial_output_meta["outputs"] = [partial_output_meta["outputs"][0]]
    service.register(
        model_name="sum_prod",
        model=sum_product_model,
        entrypoint="predict",
        metadata=partial_output_meta,
    )
    service.register(
        model_name="sum_prod",
        model=sum_product_model,
        version_name="v1",
        entrypoint="predict",
        metadata=partial_output_meta,
    )
    return service


@pytest.fixture(scope="function")
def sum_product_model_kserve_v2_invalid_output_datatype_service(
    sum_product_model,
    sum_product_model_metadata,
    api,
):
    service = Server(api=api)
    invalid_output_datatype_meta = copy.deepcopy(sum_product_model_metadata)
    invalid_output_datatype_meta["outputs"][0]["datatype"] = "invalid"
    invalid_output_datatype_meta["outputs"][1]["datatype"] = "invalid"
    service.register(
        model_name="sum_prod",
        model=sum_product_model,
        entrypoint="predict",
        metadata=invalid_output_datatype_meta,
    )
    service.register(
        model_name="sum_prod",
        model=sum_product_model,
        version_name="v1",
        entrypoint="predict",
        metadata=invalid_output_datatype_meta,
    )
    return service
