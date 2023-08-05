#!/usr/bin/env python
"""
Created on 2020/04/18

@author: yyang
"""
import os
import mmap


class PCIe(object):
    def __init__(self, filename='/sys/bus/pci/devices/0000:01:00.0/resource0'):
        self._file = None
        self._mmap = None

        assert os.path.exists(filename), 'Cannot find filename: {}'.format(filename)

        self._file = open(filename, 'wb+')
        assert self._file, 'Cannot open filename: {}'.format(filename)

        self._mmap = mmap.mmap(self._file.fileno(), 0x0)

    def __del__(self):
        if self._mmap:
            self._mmap.close()
            self._mmap = None

        if self._file:
            self._file.close()
            self._file = None

    def close(self):
        self.__del__()

    def read_uint8(self, offset):
        """
        Read PCIe bar uint8
        :param offset:  Offset address
        :return:        uint8 value that read
        """
        self._mmap.seek(offset)
        return int.from_bytes(self._mmap.read(1), byteorder='little', signed=False)

    def read_uint32(self, offset):
        """
        Read PCIe bar uint32
        :param offset:  Offset address
        :return:        uint32 value that read
        """
        self._mmap.seek(offset)
        print("PCIE READ")
        return int.from_bytes(self._mmap.read(4), byteorder='little', signed=False)

    def write_uint8(self, offset, value):
        """
        Write PCIe bar uint8
        :param offset:  Offset address
        :param value:   uint8 value to write
        :return:
        """
        self._mmap.seek(offset)
        self._mmap.write(value.to_bytes(length=1, byteorder='little', signed=False))

    def write_uint32(self, offset, value):
        """
        Write PCIe bar uint32
        :param offset:  Offset address
        :param value:   uint32 value to write
        :return:
        """
        self._mmap.seek(offset)
        print("PCIE WRITE")
        self._mmap.write(value.to_bytes(length=4, byteorder='little', signed=False))
