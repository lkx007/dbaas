# Copyright (c) 2019, Oracle and/or its affiliates.
# This software is made available to you under the terms of the GPL 3.0 license or the Apache 2.0 license.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Apache License v2.0
# See LICENSE.TXT for details.

import pytest
import logging
from nose.plugins.skip import SkipTest
from ansible.modules.cloud.oracle import oci_cross_connect_location_facts
from ansible.module_utils.oracle import oci_utils

try:
    import oci
    from oci.util import to_dict
    from oci.core.models import CrossConnectLocation
    from oci.exceptions import ServiceError, MaximumWaitTimeExceeded
except ImportError:
    raise SkipTest("test_oci_cross_connect_location_facts.py requires `oci` module")


class FakeModule(object):
    def __init__(self, **kwargs):
        self.params = kwargs

    def fail_json(self, *args, **kwargs):
        self.exit_args = args
        self.exit_kwargs = kwargs
        raise Exception(kwargs["msg"])

    def exit_json(self, *args, **kwargs):
        self.exit_args = args
        self.exit_kwargs = kwargs


@pytest.fixture()
def virtual_network_client(mocker):
    mock_virtual_network_client = mocker.patch("oci.core.VirtualNetworkClient")
    return mock_virtual_network_client.return_value


@pytest.fixture()
def list_all_resources_patch(mocker):
    return mocker.patch.object(oci_utils, "list_all_resources")


def setUpModule():
    logging.basicConfig(
        filename="/tmp/oci_ansible_module.log", filemode="a", level=logging.INFO
    )
    oci_cross_connect_location_facts.set_logger(logging)


def test_list_cross_connect_locations_all(
    virtual_network_client, list_all_resources_patch
):
    module = get_module()
    cross_connect_locations = get_cross_connect_locations()
    list_all_resources_patch.return_value = cross_connect_locations
    result = oci_cross_connect_location_facts.list_cross_connect_locations(
        virtual_network_client, module
    )
    assert (
        result["cross_connect_locations"][0]["name"] == cross_connect_locations[0].name
    )


def get_cross_connect_locations():
    cross_connect_locations = []
    cross_connect_location = CrossConnectLocation()
    cross_connect_location.description = "Equinox"
    cross_connect_location.name = "Equinox"
    cross_connect_locations.append(cross_connect_location)
    return cross_connect_locations


def get_response(status, header, data, request):
    return oci.Response(status, header, data, request)


def get_module(additional_properties=None):
    params = {"compartment_id": "ocid1.compartment..axsd"}
    if additional_properties is not None:
        params.update(additional_properties)
    module = FakeModule(**params)
    return module
