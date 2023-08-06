from __future__ import print_function
import subprocess
import sys, os
from sys import stdout
import re 
import shutil
import parasail


def cigar_to_seq(cigar, query, ref):
    cigar_tuples = []
    result = re.split(r'[=DXSMI]+', cigar)
    cig_pos = 0
    for length in result[:-1]:
        cig_pos += len(length)
        type_ = cigar[cig_pos]
        cig_pos += 1
        cigar_tuples.append((int(length), type_ ))

    r_index = 0
    q_index = 0
    q_aln = []
    r_aln = []
    for length_ , type_ in cigar_tuples:
        if type_ == "=" or type_ == "X":
            q_aln.append(query[q_index : q_index + length_])
            r_aln.append(ref[r_index : r_index + length_])

            r_index += length_
            q_index += length_
        
        elif  type_ == "I":
            # insertion w.r.t. reference
            r_aln.append('-' * length_)
            q_aln.append(query[q_index: q_index + length_])
            #  only query index change
            q_index += length_

        elif type_ == 'D':
            # deletion w.r.t. reference
            r_aln.append(ref[r_index: r_index + length_])
            q_aln.append('-' * length_)
            #  only ref index change
            r_index += length_
        
        else:
            print("error")
            print(cigar)
            sys.exit()

    return  "".join([s for s in q_aln]), "".join([s for s in r_aln]), cigar_tuples


def parasail_alignment(s1, s2, match_score = 2, mismatch_penalty = -2, opening_penalty = 3, gap_ext = 1):
    user_matrix = parasail.matrix_create("ACGT", match_score, mismatch_penalty)
    result = parasail.sg_trace_scan_16(s1, s2, opening_penalty, gap_ext, user_matrix)
    if result.saturated:
        print("SATURATED!",len(s1), len(s2))
        result = parasail.sg_trace_scan_32(s1, s2, opening_penalty, gap_ext, user_matrix)
        print("computed 32 bit instead")

    # difference in how to obtain string from parasail between python v2 and v3... 
    if sys.version_info[0] < 3:
        cigar_string = str(result.cigar.decode).decode('utf-8')
    else:
        cigar_string = str(result.cigar.decode, 'utf-8')
    s1_alignment, s2_alignment, cigar_tuples = cigar_to_seq(cigar_string, s1, s2)
    # print(result.score, len(s1), len(s2))
    # print(s1_alignment)
    # print(s2_alignment)
    # print(cigar_string)
    # sys.exit()

    return s1_alignment, s2_alignment, cigar_string, cigar_tuples, result.score

def reverse_complement(string):
    #rev_nuc = {'A':'T', 'C':'G', 'G':'C', 'T':'A', 'N':'N', 'X':'X'}
    # Modified for Abyss output
    rev_nuc = {'A':'T', 'C':'G', 'G':'C', 'T':'A', 'a':'t', 'c':'g', 'g':'c', 't':'a', 'N':'N', 'X':'X', 'n':'n', 'Y':'R', 'R':'Y', 'K':'M', 'M':'K', 'S':'S', 'W':'W', 'B':'V', 'V':'B', 'H':'D', 'D':'H', 'y':'r', 'r':'y', 'k':'m', 'm':'k', 's':'s', 'w':'w', 'b':'v', 'v':'b', 'h':'d', 'd':'h'}

    rev_comp = ''.join([rev_nuc[nucl] for nucl in reversed(string)])
    return(rev_comp)

def run_spoa(reads, spoa_out_file, spoa_path):
    with open(spoa_out_file, "w") as output_file:
        # print('Running spoa...', end=' ')
        stdout.flush()
        null = open("/dev/null", "w")
        subprocess.check_call([ spoa_path, reads, "-l", "0", "-r", "0", "-g", "-2"], stdout=output_file, stderr=null)
        # print('Done.')
        stdout.flush()
    output_file.close()
    l = open(spoa_out_file, "r").readlines()
    consensus = l[1].strip()
    return consensus

def run_medaka(reads_to_center, center_file, outfolder, cores, medaka_model):
    medaka_stdout = os.path.join(outfolder, "stdout.txt")
    with open(medaka_stdout, "w") as output_file:
        # print('Running medaka...', end=' ')
        stdout.flush()
        medaka_stderr = open(os.path.join(outfolder, "stderr.txt"), "w")
        if medaka_model:
            subprocess.check_call(['medaka_consensus', '-i', reads_to_center, "-d", center_file, "-o", outfolder, "-t", cores, "-m", medaka_model], stdout=output_file, stderr=medaka_stderr)
        else:
            subprocess.check_call(['medaka_consensus', '-i', reads_to_center, "-d", center_file, "-o", outfolder, "-t", cores], stdout=output_file, stderr=medaka_stderr)

        # print('Done.')
        stdout.flush()
    output_file.close()

def run_racon(reads_to_center, center_file, outfolder, cores, racon_iter):
    racon_stdout = os.path.join(outfolder, "stdout.txt")
    with open(racon_stdout, "w") as output_file:
        # print('Running medaka...', end=' ')
        stdout.flush()
        for i in range(racon_iter):
            read_alignments = open(os.path.join(outfolder, "read_alignments_it_{0}.paf".format(i)), 'w')
            mm2_stderr = open(os.path.join(outfolder, "mm2_stderr_it_{0}.txt".format(i)), "w")
            racon_stderr = open(os.path.join(outfolder, "racon_stderr_it_{0}.txt".format(i)), "w")
            racon_polished = open(os.path.join(outfolder, "racon_polished_it_{0}.fasta".format(i)), 'w')

            subprocess.check_call(['minimap2', '-x', 'map-ont', center_file, reads_to_center], stdout=read_alignments, stderr=mm2_stderr)
            subprocess.check_call(['racon', reads_to_center, read_alignments.name, center_file], stdout=racon_polished, stderr=racon_stderr)
            center_file = racon_polished.name

        shutil.copyfile(center_file, os.path.join(outfolder, "consensus.fasta"))
        # print('Done.')
        stdout.flush()
    output_file.close()
    # consensus.run_medaka( " medaka_consensus -i ~/tmp/stefan_isonclust/mixed_b1_b3_b4_b5.fastq -d ~/tmp/stefan_isonclust/mixed_b1_b3_b4_b5_isonclust/consensus_references.fasta -o ~/tmp/stefan_isonclust/mixed_b1_b3_b4_b5_medaka/ -t 1 -m r941_min_high_g303")


def detect_reverse_complements(centers, rc_identity_threshold):
    filtered_centers = []
    already_removed = set()
    for i, (nr_reads_in_cl, c_id, seq, reads_path) in enumerate(centers):
        merged_cluster_id = c_id
        merged_nr_reads = nr_reads_in_cl
        if c_id in already_removed:
            print("has already been merged, skipping")
            continue

        elif i == len(centers) - 1: # last sequence and it is not in already removed
            filtered_centers.append( (merged_nr_reads, c_id, seq, [reads_path]) )

        else:
            all_reads = [reads_path]
            for j, (nr_reads_in_cl2, c_id2, seq2, reads_path) in enumerate(centers[i+1:]):
                seq2_rc = reverse_complement(seq2)
                seq_aln, seq2_rc_aln, cigar_string, cigar_tuples, alignment_score = parasail_alignment(seq, seq2_rc)
                # print(i,j)
                # print(seq_aln)
                # print(seq2_rc_aln)
                nr_mismatching_pos = len([1 for n1, n2 in zip(seq_aln, seq2_rc_aln) if n1 != n2])
                total_pos = len(seq_aln)
                aln_identity =  (total_pos - nr_mismatching_pos) / float(total_pos)
                print(aln_identity)

                if aln_identity >= rc_identity_threshold:
                    print("Detected alignment identidy above threchold for reverse complement. Keeping center with the most read support and adding rc reads to supporting reads.")
                    merged_nr_reads += nr_reads_in_cl2
                    already_removed.add(c_id2)
                    all_reads.append(reads_path)
            filtered_centers.append( (merged_nr_reads, c_id, seq, all_reads) )

    print(len(filtered_centers), "consensus formed.")
    return filtered_centers





