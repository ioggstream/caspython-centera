"""
    License: GPL2
    Author: roberto.polli@par-tec.it
"""

from nose.tools import *
from nose import *

import sys
import traceback
import time

from Filepool.FPLibrary import FPLibrary

from setup import TestCentera, log
from Filepool.FPQueryExpression import FPQueryExpression
from Filepool.FPQuery import FPQuery
from Filepool.FPQueryResult import FPQueryResult

sec_in_day = 86400
from contextlib import closing


class TestCenteraQuery(TestCentera):
    # TestCentera opens and closes the pool

    def test_query_last_10day(self):
        ts = int(time.time() - 10 * sec_in_day)  #

        log.info("Preparing query")
        with closing(FPQueryExpression()) as querySinceTs:
            querySinceTs.setType(FPLibrary.FP_QUERY_TYPE_EXISTING)
            querySinceTs.setStartTime(ts)

            log.info("Starting query")
            query = FPQuery(self.pool)
            query.open(querySinceTs)

        status = 0
        while True:
            log.info("Starting query")

            res = FPQueryResult(query.fetchResult(0))
            status = res.getResultCode()

            if status in (
                    FPLibrary.FP_QUERY_RESULT_CODE_END,
                    FPLibrary.FP_QUERY_RESULT_CODE_ABORT,
                    FPLibrary.FP_QUERY_RESULT_CODE_ERROR,
                    FPLibrary.FP_QUERY_RESULT_CODE_INCOMPLETE,
                    FPLibrary.FP_QUERY_RESULT_CODE_COMPLETE
            ):
                break
            elif status == FPLibrary.FP_QUERY_RESULT_CODE_PROGRESS:
                continue
            elif status == FPLibrary.FP_QUERY_RESULT_CODE_OK:
                print(res.getClipId())

        query.close()


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
