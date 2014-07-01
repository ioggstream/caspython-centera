from Filepool.FPPool import FPPool
from Filepool.FPLibrary import FPLibrary
pool_ip = "192.168.0.1"
clipid = "97PM8IPQE1IQAeFMB3ED6RGLDDHG418DHCIKO90P1GND50REQ4J0S"
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

        self.pool = FPPool(pool_ip)
        self.pool.setGlobalOption(FPLibrary.FP_OPTION_EMBEDDED_DATA_THRESHOLD,
                                  100 * 1024)
        self.pool.getPoolInfo()
        # the application will be attached to the clip id
        self.pool.registerApplication("python wrapper read example", "1.0")

    def teardown(self):
        self.pool.close()
