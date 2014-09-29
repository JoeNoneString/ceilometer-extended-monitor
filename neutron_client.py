from neutronclient.v2_0 import client as neutron_client

class Client(object):
    def __init__(self):
        self.nets = neutron_client.Client(
                      username='ceilometer',password='password',
                      tenant_name='service',region_name='region_name',
                      auth_url="http://mykeystone:5000/v2.0",)

    def _list_pools(self):
        return self.nets.list_pools().get('pools')

    def _show_pool_stats(self, pool_id):
        return self.nets.retrieve_pool_stats(pool_id)

    def _get_lb_in_bytes(self, pool_id):
        _in_bytes = self._show_pool_stats(pool_id)['stats']['bytes_in']
        return _in_bytes

    def _get_lb_out_bytes(self, pool_id):
        _out_bytes = self._show_pool_stats(pool_id)['stats']['bytes_out']
        return _out_bytes

