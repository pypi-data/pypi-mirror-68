#!/usr/bin/env python
"""
Created on 2020/04/17

@author: yyang
"""
import os
import math
import fcntl
from ctypes import c_uint8, c_uint16, c_uint32, c_uint64, Structure, Union, sizeof, addressof


class OPCODE(object):
    # Opcodes for Admin Commands
    DELETE_IO_SQ = 0x00
    CREATE_IO_SQ = 0x01
    GET_LOG_PAGE = 0x02
    DELETE_IO_CQ = 0x04
    CREATE_IO_CQ = 0x05
    IDENTIFY = 0x06
    ABORT = 0x08
    SET_FEATURE = 0x09
    GET_FEATURE = 0x0A
    ASYNC_EVENT = 0x0C
    NAMESPACE_MGT = 0x0D
    FIRMWARE_COMMIT = 0x10
    FIRMWARE_DOWNLOAD = 0x11
    NAMESPACE_ATTACH = 0x15
    FORMAT_NVM = 0x80
    SECURITY_SEND = 0x81
    SECURITY_RECV = 0x82
    # Opcodes for NVM Commands
    FLUSH = 0x00
    WRITE = 0x01
    READ = 0x02
    WRITE_UNCORRECTABLE = 0x04
    COMPARE = 0x05
    WRITE_ZEROS = 0x08
    DATASET_MGT = 0x09
    RESERVATION_REGISTER = 0x0D
    RESERVATION_REPORT = 0x0E
    RESERVATION_ACQUIRE = 0x11
    RESERVATION_RELEASE = 0x12
    # Opcodes for CNEX Commands
    CNEX_WRITE_MEM = 0x99
    CNEX_READ_MEM = 0x9A


class NVMePassthruCmd(Union):
    """
    Take Care: different with SQE!
    cdw8 is metadata_len and cdw9 is data_len
    Add cdw16: timeout
    Add cdw17: dword0 of CQE
    """

    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('opcode', c_uint8),
            ('flags', c_uint8),
            ('rsvd1', c_uint16),
            ('nsid', c_uint32),
            ('cdw2', c_uint32),
            ('cdw3', c_uint32),
            ('metadata', c_uint64),
            ('addr', c_uint64),
            ('metadata_len', c_uint32),
            ('data_len', c_uint32),
            ('lba', c_uint64),
            ('cdw12', c_uint32),
            ('cdw13', c_uint32),
            ('cdw14', c_uint32),
            ('cdw15', c_uint32),
            ('timeout_ms', c_uint32),
            ('result', c_uint32),
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword0', c_uint32),
            ('dword1', c_uint32),
            ('dword2', c_uint32),
            ('dword3', c_uint32),
            ('dword4', c_uint32),
            ('dword5', c_uint32),
            ('dword6', c_uint32),
            ('dword7', c_uint32),
            ('dword8', c_uint32),
            ('dword9', c_uint32),
            ('dword10', c_uint32),
            ('dword11', c_uint32),
            ('dword12', c_uint32),
            ('dword13', c_uint32),
            ('dword14', c_uint32),
            ('dword15', c_uint32),
            ('dword16', c_uint32),
            ('dword17', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


def _IOWR(_tp, _nr, _sz):
    return (3 << 30) + (sizeof(_sz) << 16) + (ord(_tp) << 8) + _nr


NVME_IOCTL_ADMIN_CMD = _IOWR('N', 0x41, NVMePassthruCmd)
NVME_IOCTL_IO_CMD = _IOWR('N', 0x43, NVMePassthruCmd)


class NVMe(object):
    def __init__(self, device='/dev/nvme0', nsid=1):
        self._fd = -1
        self.nsid = nsid
        assert os.path.exists(device), 'Cannot find device: {}'.format(device)

        self._fd = os.open(device, os.O_RDWR)
        assert self._fd != -1, 'Cannot open device: {}'.format(device)

    def __del__(self):
        if self._fd != -1:
            os.close(self._fd)
            self._fd = -1

    def close(self):
        self.__del__()

    def _ioctl(self, req, cmd):
        return fcntl.ioctl(self._fd, req, cmd)

    def io_passthru(self, cmd):
        """
        Send a user-defined IO command to the specified device via IOCTL passthrough
        :param cmd:
        :return:
        """
        return self._ioctl(NVME_IOCTL_IO_CMD, cmd)

    def admin_passthru(self, cmd):
        """
        Send a user-defined Admin command to the specified device via IOCTL passthrough
        :param cmd:
        :return:
        """
        return self._ioctl(NVME_IOCTL_ADMIN_CMD, cmd)

    def rdma_read_list(self, offset, ndw=1, nsid=1):
        """
        RDMA read, return list of uint32
        :param offset:  Offset address
        :param ndw:     Number of dword
        :param nsid:    Namespace ID
        :return:        List of uint32 from RDMA read
        """
        length = math.ceil(ndw / 1024) * 1024
        data = (c_uint32 * length)()

        cmd = NVMePassthruCmd()
        cmd.opcode = OPCODE.CNEX_READ_MEM
        cmd.lba = offset
        cmd.nsid = nsid
        cmd.dword12 = ndw - 1
        cmd.addr = addressof(data)
        cmd.data_len = length * 4

        status = self.io_passthru(cmd)
        assert status == 0, 'RDMA read failed! Offset: {:#x} Status: {:#x}'.format(offset, status)

        return data[0:ndw]

    def rdma_write_list(self, offset, array, nsid=1):
        """
        RDMA write list of uint32 to offset
        :param offset:  Offset address
        :param array:   List of uint32 to RDMA write
        :param nsid:    Namespace ID
        :return:
        """
        ndw = len(array)
        length = math.ceil(ndw / 1024) * 1024
        data = (c_uint32 * length)(*array)

        cmd = NVMePassthruCmd()
        cmd.opcode = OPCODE.CNEX_WRITE_MEM
        cmd.lba = offset
        cmd.nsid = nsid
        cmd.dword12 = ndw - 1
        cmd.addr = addressof(data)
        cmd.data_len = length * 4

        status = self.io_passthru(cmd)
        assert status == 0, 'RDMA write failed! Offset: {:#x} Status: {:#x}'.format(offset, status)

    def read_uint32(self, offset):
        """
        RDMA read, return uint32
        :param offset:  Offset address
        :param nsid:    Namespace ID
        :return:        uint32
        """
        print("RDMA WRITE")
        return self.rdma_read_list(offset, ndw=1, nsid=self.nsid)[0]

    def write_uint32(self, offset, value):
        """
        RDMA write uint32 to offset
        :param offset:  Offset address
        :param value:   uint32 value to RDMA write
        :param nsid:    Namespace ID
        :return:
        """
        print("RDMA READ")
        self.rdma_write_list(offset, [value], nsid=self.nsid)
