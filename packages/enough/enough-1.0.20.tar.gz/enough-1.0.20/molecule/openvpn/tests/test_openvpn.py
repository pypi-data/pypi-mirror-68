testinfra_hosts = ['openvpnclient-host']


# development-inventory/group_vars/all/openvpn.yml defines the route 10.11.12.0/24
def test_vpn_route(host):
    cmd = host.run("ip route")
    print(cmd.stdout)
    print(cmd.stderr)
    assert cmd.rc == 0
    assert '10.11.12' in cmd.stdout
