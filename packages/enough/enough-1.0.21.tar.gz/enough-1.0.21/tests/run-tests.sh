#!/bin/bash

set -ex

name=enough-tox-$(date +%s)

trap "docker rm -f $name >& /dev/null || true ; docker rmi --no-prune $name >& /dev/null || true"  EXIT

cat > inventory/group_vars/all/clouds.yml <<EOF
---
clouds:
  ovh:
    auth:
      auth_url: "$OS_AUTH_URL"
      project_name: "$OS_PROJECT_NAME"
      project_id: "$OS_PROJECT_ID"
      user_domain_name: "$OS_USER_DOMAIN_NAME"
      username: "$OS_USERNAME"
      password: "$OS_PASSWORD"
    region_name: "$OS_REGION_NAME"
EOF

cat > inventory/group_vars/all/domain.yml <<EOF
---
domain: enough.community
EOF

(
    cat enough/common/data/base.dockerfile
    cat tests/tox.dockerfile
) | docker build --tag $name -f - .

docker run --rm --name $name -e SKIP_OPENSTACK_INTEGRATION_TESTS=true -v /var/run/docker.sock:/var/run/docker.sock $name tox
