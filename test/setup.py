"""
    License: GPL2
    Author: roberto.polli@babel.it
"""
import logging
from Filepool.FPPool import FPPool
from Filepool.FPLibrary import FPLibrary
from Filepool.util import parse_config

logging.basicConfig()
log = logging.getLogger("centera.test")

CONFIG = parse_config('test.ini')
POOL_ADDRESS = CONFIG['test']['pool_address']
clipid =  CONFIG['test']['clipid']

"""
except FPClientException, c:
  print c
  traceback.print_exc(file=sys.stdout)
except FPServerException, s:
  print s
except FPNetException, n:
  print n
except FPException, e:
  print e
  """


class TestCentera(object):

    def setup(self):

        self.pool = FPPool(POOL_ADDRESS)
        self.pool.setGlobalOption(FPLibrary.FP_OPTION_EMBEDDED_DATA_THRESHOLD,
                                  100 * 1024)
        self.pool.getPoolInfo()
        # the application will be attached to the clip id
        self.pool.registerApplication("python wrapper read example", "1.0")

    def teardown(self):
        self.pool.close()
