#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0
from ocean_utils.agreements.service_types import ServiceTypes
from ocean_utils.utils.utilities import get_timestamp

from squid_py.ocean.keeper import SquidKeeper


def test_create_access_service(publisher_ocean_instance):
    service = publisher_ocean_instance.services.create_access_service({'a': 1}, 'service_endpoint')
    assert service[0] == 'access'
    assert service[1]['attributes'] == {'a': 1}
    assert service[1]['serviceEndpoint'] == 'service_endpoint'


def test_create_compute_service(publisher_ocean_instance):
    ocn_compute = publisher_ocean_instance.compute

    cluster = ocn_compute.build_cluster_attributes('kubernetes', '/cluster/url')
    container = ocn_compute.build_container_attributes(
        "tensorflow/tensorflow",
        "latest",
        "sha256:cb57ecfa6ebbefd8ffc7f75c0f00e57a7fa739578a429b6f72a0df19315deadc"
    )
    server = ocn_compute.build_server_attributes(
        "1",
        "xlsize",
        "16",
        "0",
        "128gb",
        "160gb",
        86400
    )
    provider_attributes = ocn_compute.build_service_provider_attributes(
        "Azure",
        "some description of the compute server instance",
        cluster,
        [container],
        [server]
    )
    attributes = ocn_compute.create_compute_service_attributes(
        "10",
        3600*24,
        publisher_ocean_instance.main_account.address,
        get_timestamp(),
        provider_attributes
    )
    service = publisher_ocean_instance.services.create_compute_service(
        attributes,
        'http://brizo.com:8030/api/v1/services/compute'
    )
    assert isinstance(service, tuple) and len(service) == 2
    assert service[0] == ServiceTypes.CLOUD_COMPUTE
    assert isinstance(service[1], dict)
    assert service[1]['templateId'] == SquidKeeper.get_instance().get_agreement_template_id(ServiceTypes.CLOUD_COMPUTE)
    assert service[1]['attributes'] == attributes
    assert service[1]['serviceEndpoint'] == 'http://brizo.com:8030/api/v1/services/compute'
