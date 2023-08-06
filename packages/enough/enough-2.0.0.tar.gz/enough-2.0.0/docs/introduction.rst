Introduction
============

The enough CLI controls an OpenStack based infrastructure and the
services that run on top of it, with Ansible.

Requirements
------------

* The ``openrc.sh`` credentials for a ``Public cloud`` project at `OVH
  <https://www.ovh.com/manager/public-cloud/>`__. No other OpenStack
  provider is supported.

* The ``Public cloud`` project has a `Private network
  <https://www.ovh.com/world/solutions/vrack/>`__.

Quick start
-----------

* `Install Docker <http://docs.docker.com/engine/installation/>`__.

* Copy ``openrc.sh`` in ``~/.enough/myname.d.enough.community/openrc.sh`` and edit
  to replace ``$OS_PASSWORD_INPUT`` with the actual password.

* Add the ``enough`` CLI to ``~/.bashrc``:
  ::

     eval "$(docker run --rm enoughcommunity/enough:latest install)"

* Create the ``Nextcloud`` service with:
  ::

     $ enough --domain myname.d.enough.community service create cloud

..  note::
    If the command fails, because of a network failure or any other reason,
    it is safe to run it again. It is idempotent.

* Login ``https://cloud.myname.d.enough.community`` with user ``admin`` password ``mynextcloud``
