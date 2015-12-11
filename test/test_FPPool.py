"""
Test for FPool

"""
from Filepool.FPClientException import FPClientException
from Filepool.FPPool import FPPool
from nose.tools.nontrivial import raises
from setup import log, POOL_ADDRESS

__author__ = 'rpolli'


def test_double_close():
    pool = FPPool(POOL_ADDRESS)
    log.info("Pool opened with handle: %r", pool.handle)
    pool.close()
    log.info("Pool opened with handle: %r", pool.handle)
    pool.close()


@raises(FPClientException)
def test_work_on_closed():
    pool = FPPool(POOL_ADDRESS)
    log.info("Pool opened with handle: %r", pool.handle)
    pool.close()
    log.info("Pool opened with handle: %r", pool.handle)
    pool.getClusterTime()
