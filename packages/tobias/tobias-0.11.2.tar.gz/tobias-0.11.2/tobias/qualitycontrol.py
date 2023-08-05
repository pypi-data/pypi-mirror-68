import sys
import pysam
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal

from tobias.utils.sequences import *
from tobias.utils.ngs import *

#--bam 
#--fasta    #fasta file for quantifying ATAC bias
#--regions   #quantify the number of reads in specific regions



bam_f = sys.argv[1]
print(bam_f)

"""
total reads
deduplicated reads

fragment size distribution
Tn5 bias
mapping quality
"""

class AtacQC():
    def __init__(self):

        #Initialize quality
        self.n_reads = 0
        self.fragment_length = {}
        self.n_duplicates = 0

    def join(): #join from separate AtacQC objects
        pass

    def add_read(self, read):
        """ Add read to QC quantification"""

        self.n_reads += 1

        template_length = abs(read.template_length) - 9
        self.fragment_length[template_length] = self.fragment_length.get(template_length, 0) + 1

        self.n_duplicates += read.is_duplicate

        return(self)

#Open bam
bam = pysam.AlignmentFile(bam_f, "rb")
try:
    bam.check_index()
except ValueError:
    pysam.index(bam_f)
    bam = pysam.AlignmentFile(bam_f, "rb")

bam_chrom_info = dict(zip(bam.references, bam.lengths))
genome_regions = RegionList().from_chrom_lengths(bam_chrom_info)
genome_regions_chunked = genome_regions.apply_method(OneRegion.split_region, 1000000)

#Open fasta obj

# Read all bedfiles to regions
"""
#fetch reads
for read in bam.fetch():
    print(read)
    print(read.flag)
    print(read.is_duplicate)
    print(read.is_paired)
    print(read.is_proper_pair)
    print(read.get_tags())
    print(read.to_dict())
    print(read.template_length - 9)
    print(read.mapping_quality)

    #oneread obj
    oneread = OneRead(read)
    print(oneread)
    break
"""

atac_qc = AtacQC()
atac_bias = SequenceMatrix().create(20, "PWM")
genome_chunks = []

fasta_obj = pysam.FastaFile(args.fasta)

for region in genome_regions_chunked:
    seq_obj = GenomicSequence(region).from_fasta(fasta_obj)

    for i, read in enumerate(sam.fetch()):
        oneread = OneRead(read)
        atac_qc.add_read(read)

        oneread.get_cutsite()
        oneread.get_kmer(seq_obj, 10)

        print(oneread)
    
    if i == 1000000:
        break

print(i)
print(atac_qc.fragment_length)

inserts = sorted(atac_qc.fragment_length.keys())
counts = [atac_qc.fragment_length[key] for key in inserts]

#impute counts between keys

tot_counts = sum(counts)
print(tot_counts)
print(atac_qc.n_reads)
cum_sum = [sum(counts[i:])/tot_counts for i in range(len(counts))]

print(inserts)
#print(cum_sum_perc)

peaks = scipy.signal.find_peaks(counts, distance=5)

peak_insert = np.array(inserts)[peaks[0]]
peak_counts = np.array(counts)[peaks[0]]
print(peak_insert)

mean_insert_size = np.average(inserts, weights=counts)
print(mean_insert_size)

fig, ax1 = plt.subplots()
ax1.plot(inserts, counts)
ax1.set_xlim(0,1000)

ax2 = ax1.twinx()
ax2.plot(inserts, cum_sum)

ax1.scatter(peak_insert, peak_counts, color="red", s=10)

plt.show()

