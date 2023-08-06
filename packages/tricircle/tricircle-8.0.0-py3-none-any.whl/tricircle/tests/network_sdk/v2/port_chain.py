# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack import resource


class PortChain(resource.Resource):
    resource_key = 'port_chain'
    resources_key = 'port_chains'
    base_path = '/sfc/port_chains'

    allow_create = True
    allow_get = True
    allow_update = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters('name')

    name = resource.Body('name')
    description = resource.Body('description')
    port_pair_groups = resource.Body('port_pair_groups', type=list)
    flow_classifiers = resource.Body('flow_classifiers', type=list)
    chain_parameters = resource.Body('chain_parameters', type=dict)
    chain_id = resource.Body('chain_id')
