# cython: language_level=3

# SPDX-FileCopyrightText: 2014 The cython-sgio Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Cython bindings for the Linux SGIO ioctl interface.

References:
 + Linux SCSI Generic (sg) Driver: http://sg.danny.cz/sg/
 + Tour the Linux generic SCSI driver:
     http://www.ibm.com/developerworks/library/l-scsi-api/
 + Extending Python with C or C++:
     https://docs.python.org/2/extending/extending.html
 + Python Extension Programming with C:
     http://www.tutorialspoint.com/python/python_further_extensions.htm

See Also:
 + The Linux SCSI Generic (sg) HOWTO:
     (Though out of date, this Linux 2.4 doc provides useful info.)
     http://www.tldp.org/HOWTO/SCSI-Generic-HOWTO/index.html
"""

from cpython.bytearray cimport PyByteArray_FromStringAndSize

from libc.errno cimport errno
from libc.stdlib cimport calloc, free
from posix.ioctl cimport ioctl

cdef extern from "scsi/sg.h":
    cdef enum:
        SG_IO

    cdef enum:
        SG_DXFER_NONE
        SG_DXFER_TO_DEV
        SG_DXFER_FROM_DEV
        SG_DXFER_TO_FROM_DEV

    cdef enum:
        SG_INFO_OK_MASK
        SG_INFO_OK

    ctypedef struct sg_io_hdr_t:
        int interface_id
        int dxfer_direction
        unsigned char cmd_len
        unsigned char mx_sb_len
        unsigned short int iovec_count
        unsigned int dxfer_len
        unsigned char * dxferp
        unsigned char * cmdp
        unsigned char * sbp
        unsigned int timeout
        unsigned int flags
        int pack_id
        void * usr_ptr
        unsigned char status
        unsigned char masked_status
        unsigned char msg_status
        unsigned char sb_len_wr
        unsigned short int host_status
        unsigned short int driver_status
        int resid
        unsigned int duration
        unsigned int info


class CheckConditionError(Exception):
    """The target is reporting an error.

    Send a Request Sense command to retrieve error information.

    See https://en.wikipedia.org/wiki/SCSI_check_condition for details.
    """

    def __init__(self, sense):
        super(CheckConditionError, self).__init__(
            'SCSI Check Condition: %s' % sense.hex()
        )
        self.sense = sense


class UnspecifiedError(Exception):
    """Something went wrong."""


def execute(
        fid,
        cdb,
        data_out,
        bytearray data_in,
        max_sense_data_length = 32,
):
    """Execute a SCSI Generic ioctl on the provided file object.

    This function wraps the call to the C-level ioctl() method for the
    Linux SCSI Generic interface. While Python provides a wrapper for
    ioctl() as part of the standard library, the SG interface requires
    providing output pointers as well as an input structure.

    Args:
      fid: The file object to execute the ioctl() on.
      cdb: A bytes, bytearray or compatible object with the Command
        Buffer to send.
      data_out: A bytes, bytearray or compatible object with the data
        to send together with the CDB.
      data_in: A bytearray allocated to the length of the expected
        data to receive in the CDB response.
      max_sense_data_length: An optional maximum number of bytes to
        allocate to receive Sense Data in case of Check Condition
        failures.

    Returns:
      The number of bytes written or received from a successful
      ioctl().

    Raises:

      MemoryError: if the allocation of the sense data failed.
      OSError: if the ioctl() call failed.
      CheckConditionError: if a SCSI Check Condition was received from
        the device.
      UnspecifiedError: if the ioctl() succeded, an error occurred,
        but no Check Condition was received.
    """
    cdef sg_io_hdr_t io_hdr
    cdef unsigned char[:] input_view = data_in

    cdef unsigned char *sense = <unsigned char *> calloc(
        max_sense_data_length, sizeof(unsigned char))
    if not sense:
        raise MemoryError()

    try:
        # Prepare the sg device I/O header structure.
        io_hdr.interface_id = b'S'
        io_hdr.cmd_len = len(cdb)
        io_hdr.iovec_count = 0
        io_hdr.cmdp = cdb
        io_hdr.sbp = sense
        io_hdr.timeout = 1800000
        io_hdr.flags = 0
        io_hdr.mx_sb_len = max_sense_data_length

        if data_out is not None:
            data_out_len = len(data_out)
        else:
            data_out_len = 0

        if data_in is not None:
            data_in_len = len(data_in)
        else:
            data_in_len = 0

        if data_out_len and data_in_len:
            raise NotImplemented('Indirect IO is not supported.')
        elif data_out_len:
            io_hdr.dxfer_direction = SG_DXFER_TO_DEV
            io_hdr.dxfer_len = data_out_len
            io_hdr.dxferp = data_out
        elif data_in_len:
            io_hdr.dxfer_direction = SG_DXFER_FROM_DEV
            io_hdr.dxfer_len = data_in_len
            io_hdr.dxferp = &input_view[0]
        else:
            io_hdr.dxfer_len = 0
            io_hdr.dxferp = NULL
            io_hdr.dxfer_direction = SG_DXFER_NONE

        result = ioctl(fid.fileno(), SG_IO, &io_hdr)
        if result < 0:
            raise OSError(errno, 'ioctl failed')

        if io_hdr.info & SG_INFO_OK_MASK != SG_INFO_OK:
            if io_hdr.sb_len_wr > 0:
                raise CheckConditionError(bytes(sense[:io_hdr.sb_len_wr]))
            else:
                raise UnspecifiedError()

        # Return the actual transfer written.
        return io_hdr.resid
    finally:
        free(sense)
