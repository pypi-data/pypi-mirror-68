import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
import argparse
from .lib.executor import Executor
from .lib.driver.nvme import NVMe
from .lib.driver.pcie import PCIe


def create_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    add_rdma_argument(subparsers)
    add_pcie_argument(subparsers)
    add_list_argument(subparsers)
    return parser


def add_list_argument(subparsers):
    regression_parser = subparsers.add_parser("list", help='list all dfx files')
    regression_parser.set_defaults(executor_function=list_handler)


def add_pcie_argument(subparsers):
    regression_parser = subparsers.add_parser("pcie", help='read and write register with PCIE')
    regression_required_arguments = regression_parser.add_argument_group('required arguments')
    regression_required_arguments.add_argument('--dfx_file', '-f', type=str, help='dfx file', required=False)
    regression_required_arguments.add_argument('--pcie', '-p', type=str, default="0000:01:00.0",
                                               help='pcie address', required=False)
    regression_parser.set_defaults(executor_function=pcie_handler)


def add_rdma_argument(subparsers):
    regression_parser = subparsers.add_parser("rdma", help='read and write register with RDMA')
    regression_required_arguments = regression_parser.add_argument_group('required arguments')
    regression_required_arguments.add_argument('--dfx_file', '-f', type=str, help='dfx file', required=False)
    regression_required_arguments.add_argument('--device', '-d', type=str,  default="nvme0",
                                               help='nvme device name', required=False)
    regression_required_arguments.add_argument('--nsid', '-n', type=int, default=1,
                                               help='nvme namespace id', required=False)
    regression_parser.set_defaults(executor_function=rdma_handler)


def rdma_handler(args):
    device = "/dev/{}".format(args.device)
    rout = NVMe(device, args.nsid)
    executor = Executor(rout)
    executor.execute(args.dfx_file)
    return 0


def pcie_handler(args):
    filename = '/sys/bus/pci/devices/{}/resource0'.format(args.pcie)
    rout = PCIe(filename)
    executor = Executor(rout)
    executor.execute(args.dfx_file)
    return 0


def list_handler(args):
    dfx_folder = os.path.join(os.path.dirname(__file__), "configuration")
    all_files = os.listdir(dfx_folder)
    for item in all_files:
        if "dfx" in item:
            print(item)


def main():
    parser = create_parser()
    args = parser.parse_args()
    try:
        args.executor_function(args)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
