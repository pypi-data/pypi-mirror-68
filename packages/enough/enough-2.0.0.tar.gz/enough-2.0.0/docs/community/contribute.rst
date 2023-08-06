Contribute
==========

This is the contribution guide to the `enough.community` infrastructure
which is based on Ansible. If you're a seasoned Free Software
contributor looking for a quick start, take a look at the `list of
bugs and features
<https://lab.enough.community/main/infrastructure/issues>`__,
otherwise keep reading.

.. note:: If you want to contribute to the Enoug code base, take
          a look at `the repository <https://lab.enough.community/main/app>`__. 

Resources
---------

* Repository and issue tracking: http://lab.enough.community/main/infrastructure
* Forum: https://forum.enough.community/
* Instant messenging: https://chat.enough.community/enough/
* License: `AGPLv3 <https://lab.enough.community/main/infrastructure/blob/master/LICENSE>`__
* :doc:`Who's who <team>`
* Requirement: `Integration testing`_

Bugs and features list
----------------------

Each service under the `enough.community` domain can be worked on
independently and have their own integration tests. There is no need
to understand how `Weblate` is deployed if you're improving
`Discourse`, for instance.

Organization
------------

All contributors are `organized horizontally <https://enough.community/blog/2018/07/20/manifesto/>`__

* People with access to an exclusive resource must register themselves
  in the :doc:`team directory <team>`

.. _getting_started:

Getting started
---------------

* ``apt install virtualenv``
* ``deactivate || true ; source bootstrap``
* ``./dev-links.sh``
* get OpenStack credentials (ask :doc:`anyone in the <team>`) and store then in `openrc.sh`
* ``source openrc.sh``
* ``openstack server list``: should successfully return nothing on a new tenant
* ``cp clouds.yml.example ~/.enough/dev/inventory/clouds.yml`` and edit to match `openrc.sh`
* ``cp ~/.enough/dev/inventory/clouds.yml ~/.enough/dev/clone-clouds.yml`` and change the region for backup testing
* Login https://api.enough.community/ to get the ENOUGH_API_TOKEN and set it in the environment. See below for more information on how to get the token.
* ``tox -e bind``: create VMs for the scenario `bind` and run ansible playbook defined for this service
* ``enough --domain bind.test ssh bind-host``: ssh to the bind-host machine

Ansible repository layout
-------------------------

The `ansible repository
<http://lab.enough.community/main/infrastructure/>`_ groups playbooks
and roles in separate directories to reduce the number of files to
consider when working on improving a playbook or a service.

* ``playbooks/authorized_keys``: distribute SSH public keys
* ``playbooks/backup``: daily VMs snapshots
* ``playbooks/bind``: DNS server and client
* ``playbooks/letsencrypt-nginx``: nginx reverse proxy with letsencrypt integration
* ``playbooks/icinga``: resources monitoring
* ``playbooks/infrastructure``: VMs creation and firewalling
* ``playbooks/postfix``: outgoing mail relay for all VMs
* etc.

The other scenarii found in the `playbooks` directory are services such
as `weblate <https://weblate.org/>`_ or `discourse <https://discourse.org/>`_.

The toplevel directory contains the `playbook that applies to the
enough.community production environment
<http://lab.enough.community/main/infrastructure/blob/master/enough-playbook.yml>`_. It
imports playbooks found in the `playbooks` directory.

Integration testing
-------------------

Unit tests are welcome, integration tests are mandatory. When
modifying a role or a playbook in the directory `playbooks/ABC` one is
expected to add a test for the new behavior and verify it runs
successfully:

* ``tox -e ABC``

Ansible being declarative for the most part, unit tests are only
beneficial to verify loops and conditionals work as expected. For
instance by checking a file is created only if **--tag something** is
provided. An integration test is necessary to checks if the service is
actually doing anything useful. For instance the integration tests for
weblate request that the weblate server sends a mail and
verify it is relayed by the postfix server.

When possible integration tests should be created as `icinga` monitoring
checks so they can be run on a regular basis in the production
environment to verify it keeps working.

After all tests pass, integration with online services must be
verified manually inside the preproduction environment.

The value of ``ENOUGH_API_TOKEN`` below is displayed to signed-in
users at https://api.enough.community. Members of the `group
enough <https://lab.enough.community/groups/enough/-/group_members>`_
can sign-in, others can `request access <https://lab.enough.community/groups/enough/-/group_members/request_access>`_.

* ``ENOUGH_API_TOKEN=XXXXXXX tox -e bind``
* The domain name used for testing is in `~/.enough/bind.test/inventory/group_vars/all/domain.yml`

Uprade testing
--------------

The ``converge-from-tag.sh`` script can be used to setup a scenario
based on a previous version of the repository:

  ::

     $ export ENOUGH_API_TOKEN=XXXXXXX
     $ converge-from-tag.sh 1.0.7 icinga
     ...

It essentially does the following:

* checkout the ``1.0.7``  tag into ``../infrastructure-versions/1.0.7/infrastructure``
* and run ``tox -e icinga`` from this directory

When ``converge-from-tag.sh`` completes,

  ::

     $ tox -e icinga

from the working directory will re-use the hosts created by the
``converge-from-tag.sh`` run above and upgrade from ``1.0.7``.
