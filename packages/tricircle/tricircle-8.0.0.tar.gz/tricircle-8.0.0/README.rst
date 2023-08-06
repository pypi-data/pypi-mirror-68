========================
Team and repository tags
========================

.. image:: https://governance.openstack.org/tc/badges/tricircle.svg
    :target: https://governance.openstack.org/tc/reference/tags/index.html

.. Change things from this point on

=========
Tricircle
=========

The purpose of the Tricircle project is to provide networking automation
across Neutron servers in multi-region OpenStack clouds deployment.

Each OpenStack cloud includes its own Nova, Cinder and Neutron, the Neutron
servers in these OpenStack clouds are called local Neutron servers, all these
local Neutron servers will be configured with the Tricircle Local Neutron
Plugin. A separate Neutron server will be installed and run standalone as
the coordinator of networking automation across local Neutron servers, this
Neutron server will be configured with the Tricircle Central Neutron Plugin,
and is called central Neutron server.

Leverage the Tricircle Central Neutron Plugin and the Tricircle Local Neutron
Plugin configured in these Neutron servers, the Tricircle can ensure the
IP address pool, IP/MAC address allocation and  network segment allocation
being managed globally without conflict, and the Tricircle handles tenant
oriented data link layer(Layer2) or network layer(Layer3) networking
automation across local Neutron servers, resources like VMs, bare metal or
containers of the tenant can communicate with each other via Layer2 or Layer3,
no matter in which OpenStack cloud these resources are running on.

Note: There are some our own definitions of Layer2/Layer3 networking
across Neutron. To make sure what they are, please read our design
documentation, especially "6.5 L2 Networking across Neutron". The wiki and
design documentation are linked below.

The Tricircle and multi-region OpenStack clouds will use shared
KeyStone(with centralized or distributed deployment) or federated KeyStones.

The Tricircle source code is distributed under the terms of the Apache
License, Version 2.0. The full terms and conditions of this license are
detailed in the LICENSE file.

* Free software: Apache license
* Design documentation: `Tricircle Design Blueprint <https://docs.google.com/document/d/1zcxwl8xMEpxVCqLTce2-dUOtB-ObmzJTbV1uSQ6qTsY/>`_
* Wiki: https://wiki.openstack.org/wiki/tricircle
* Installation guide: https://docs.openstack.org/tricircle/latest/install/index.html
* Admin guide: https://docs.openstack.org/tricircle/latest/admin/index.html
* Configuration guide: https://docs.openstack.org/tricircle/latest/configuration/index.html
* Networking guide: https://docs.openstack.org/tricircle/latest/networking/index.html
* Source: https://opendev.org/openstack/tricircle
* Bugs: https://bugs.launchpad.net/tricircle
* Blueprints: https://blueprints.launchpad.net/tricircle
* Release notes: https://docs.openstack.org/releasenotes/tricircle
* Contributing: https://docs.openstack.org/tricircle/latest/contributor/index.html
