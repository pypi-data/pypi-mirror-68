# Copyright 2017 Huawei Technologies Co., Ltd.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from neutron_lib.plugins.ml2 import api
from oslo_config import cfg
from oslo_log import log

from neutron.plugins.ml2.drivers import type_vxlan
from neutron_lib import constants as q_lib_constants
from neutron_lib import exceptions as n_exc

from tricircle.common import constants
import tricircle.common.context as t_context
import tricircle.db.api as db_api

LOG = log.getLogger(__name__)


class VxLANTypeDriver(type_vxlan.VxlanTypeDriver):
    def __init__(self):
        super(VxLANTypeDriver, self).__init__()

    def get_type(self):
        return constants.NT_VxLAN

    def initialize(self):
        try:
            self._initialize(cfg.CONF.tricircle.vni_ranges)
        except n_exc.NetworkTunnelRangeError:
            LOG.exception("Failed to parse vni_ranges. "
                          "Service terminated!")
            raise SystemExit()

    def reserve_provider_segment(self, context, segment, filters=None):
        res = super(VxLANTypeDriver,
                    self).reserve_provider_segment(context, segment, filters)
        res[api.NETWORK_TYPE] = constants.NT_VxLAN
        return res

    def allocate_tenant_segment(self, context, filters=None):
        res = super(VxLANTypeDriver,
                    self).allocate_tenant_segment(context, filters)
        res[api.NETWORK_TYPE] = constants.NT_VxLAN
        return res

    def get_mtu(self, physical_network=None):
        pass

    def get_endpoint_by_host(self, host):
        LOG.debug("get_endpoint_by_host() called for host %s", host)
        host_endpoint = {'ip_address': None}
        context = t_context.get_db_context()
        agents = db_api.get_agent_by_host_type(
            context, host, q_lib_constants.AGENT_TYPE_OVS)
        if agents:
            host_endpoint['ip_address'] = agents['tunnel_ip']
        return host_endpoint
