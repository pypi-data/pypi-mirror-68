# header = { 'HD': {'VN': '1.0'},
#            'SQ': [{'LN': 1575, 'SN': 'chr1'},
#                   {'LN': 1584, 'SN': 'chr2'}] }

# with pysam.AlignmentFile(tmpfilename, "wb", header=header) as outf:
#     a = pysam.AlignedSegment()
#     a.query_name = "read_28833_29006_6945"
#     a.query_sequence="AGCTTAGCTAGCTACCTATATCTTGGTCTTGGCCG"
#     a.flag = 99
#     a.reference_id = 0
#     a.reference_start = 32
#     a.mapping_quality = 20
#     a.cigar = ((0,10), (2,1), (0,25))
#     a.next_reference_id = 0
#     a.next_reference_start=199
#     a.template_length=167
#     a.query_qualities = pysam.qualitystring_to_array("<<<<<<<<<<<<<<<<<<<<<:<9/,&,22;;<<<")
#     a.tags = (("NM", 1),
#               ("RG", "L1"))
#     outf.write(a)

import numpy as np
import cython

import pysam

from libc.stdint cimport int32_t, uint32_t, uint64_t, int8_t, int16_t, uint16_t

# from pysam.libcalignedsegment cimport AlignedSegment

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
cpdef _bamwrite(filename, uint32_t mapq=0, uint64_t required_flag=0, uint64_t filter_flag=1540):

    cdef:
        uint16_t flag
        int32_t start
        int32_t end
        uint32_t count = 0
        uint32_t nfound = 0
        long [::1] starts
        long [::1] ends
        int16_t [::1] chromosomes
        int8_t [::1] strands
        uint16_t [::1] flags
        # cdef AlignedSegment a


    samfile = pysam.AlignmentFile(filename, "rb")

    for _ in samfile:
        count += 1

    samfile.close()
    samfile = pysam.AlignmentFile(filename, "rb")

    flags_arr = np.zeros(count, dtype=np.uint16)
    flags = flags_arr

    starts_arr = np.zeros(count, dtype=long)
    starts = starts_arr

    ends_arr = np.zeros(count, dtype=long)
    ends = ends_arr

    chromosomes_arr = np.zeros(count, dtype=np.int16)
    chromosomes = chromosomes_arr

    strands_arr = np.zeros(count, dtype=np.int8)
    strands = strands_arr
