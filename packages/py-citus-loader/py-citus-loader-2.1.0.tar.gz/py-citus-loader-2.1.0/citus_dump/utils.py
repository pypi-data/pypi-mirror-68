import os
import datetime

from multiprocessing.pool import ThreadPool

from itertools import cycle, islice


def run(cmd):
    print('%s: run statement %s' % (datetime.datetime.now(), cmd))
    return cmd, os.system(cmd)


def run_statements_in_parallel(configuration, statements):
    pool = ThreadPool(configuration.parallel_tasks)
    for cmd, rc in pool.imap_unordered(run, statements):
        print('%s: %s' % (
            datetime.datetime.now(),
            '{cmd} return code: {rc}'.format(**vars())))

    pool.close()
    pool.join()
