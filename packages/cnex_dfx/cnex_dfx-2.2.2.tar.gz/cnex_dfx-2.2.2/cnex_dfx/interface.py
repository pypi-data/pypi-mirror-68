import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from .lib.executor import Executor


def run(rout, dfx_file, log_path):
    """

    :param rout: read, write register rout
    :param dfx_file: dfx file path
    :param log_path: where save log faile
    :return:
    result: result file
    pass_count: count of passed test
    fail_count: count of failed test
    """
    executor = Executor(rout)
    result, pass_count, fail_count = executor.execute(dfx_file, log_path)
    return result, pass_count, fail_count
