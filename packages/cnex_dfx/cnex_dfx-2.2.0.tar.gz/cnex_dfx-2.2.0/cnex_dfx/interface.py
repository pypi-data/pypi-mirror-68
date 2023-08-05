import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from lib.executor import Executor



def run(rout, dfx_file, log_path):
    executor = Executor(rout)
    result, pass_count, fail_count = executor.execute(dfx_file, log_path)
    return result, pass_count, fail_count
