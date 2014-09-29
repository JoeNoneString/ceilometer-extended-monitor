# -*- encoding: utf-8 -*-
from ceilometer.openstack.common import log
from ceilometer.openstack.common import timeutils

from ceilometer.central import plugin
from ceilometer import sample
from ceilometer import neutron_client


class LbaasInBytesPollster(plugin.CentralPollster):
 
    LOG = log.getLogger(__name__ + '.LBaaS')

    def _get_lb_in_bytes(self):
        in_bytes = []
        nt = neutron_client.Client()

        for pool in nt._list_pools():
            bytes = nt._get_lb_in_bytes(pool['id'])
            in_bytes.append({'id': pool['id'],
                             'bytes': bytes})
        return in_bytes

    def _iter_pool_stats(self, cache):
        if 'in_bytes' not in cache:
            cache['in_bytes'] = list(self._get_lb_in_bytes())
        return iter(cache['in_bytes'])

    def get_samples(self, manager, cache):
        for pool in self._iter_pool_stats(cache):
            self.LOG.info("LBAAS POOL: %s" % pool['id'])
            yield sample.Sample(
                name='network.lb.in.bytes',
                type=sample.TYPE_CUMULATIVE,
                unit='byte',
                volume=pool['bytes'],
                user_id=None,
                project_id=None,
                resource_id=pool['id'],
                timestamp=timeutils.utcnow().isoformat(),
                resource_metadata={})


class LbaasOutBytesPollster(plugin.CentralPollster):

    LOG = log.getLogger(__name__ + '.LBaaS')

    def _get_lb_out_bytes(self):
        in_bytes = []
        nt = neutron_client.Client()

        for pool in nt._list_pools():
            bytes = nt._get_lb_out_bytes(pool['id'])
            in_bytes.append({'id': pool['id'],
                             'bytes': bytes})
        return in_bytes

    def _iter_pool_stats(self, cache):
        if 'out_bytes' not in cache:
            cache['out_bytes'] = list(self._get_lb_out_bytes())
        return iter(cache['out_bytes'])

    def get_samples(self, manager, cache):
        for pool in self._iter_pool_stats(cache):
            self.LOG.info("LBAAS POOL: %s" % pool['id'])
            yield sample.Sample(
                name='network.lb.out.bytes',
                type=sample.TYPE_CUMULATIVE,
                unit='byte',
                volume=pool['bytes'],
                user_id=None,
                project_id=None,
                resource_id=pool['id'],
                timestamp=timeutils.utcnow().isoformat(),
                resource_metadata={})

