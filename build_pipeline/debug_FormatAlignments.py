from FormatAlignments import  *

print("\nFormatting alignments\n")
valignments, jalignments = {}, {}
all_valignments, all_jalignments = {}, {}
ccalignments, c1alignments, c2alignments, c3alignments = {}, {}, {}, {}

print("IGs")
for species in all_species:
    for chain_type in "HKL":
        if not os.path.isfile(os.path.join(fasta_path, "%s_%sV.fasta" % (species, chain_type))):
            continue

        valignments[(species, chain_type)] = read_alignment(
            os.path.join(fasta_path, "%s_%sV.fasta" % (species, chain_type)), region_name="V-REGION")
        jalignments[(species, chain_type)] = read_alignment(
            os.path.join(fasta_path, "%s_%sJ.fasta" % (species, chain_type)), region_name="J-REGION")

        ### Comment out if you want constant regions?
        if chain_type == "H":
            c1alignments[(species, chain_type)] = read_alignment(
                os.path.join(fasta_path, "%s_%sC.fasta" % (species, chain_type)), region_name="CH1")
            c2alignments[(species, chain_type)] = read_alignment(
                os.path.join(fasta_path, "%s_%sC.fasta" % (species, chain_type)), region_name="CH2")
            c3alignments[(species, chain_type)] = read_alignment(
                os.path.join(fasta_path, "%s_%sC.fasta" % (species, chain_type)), region_name="CH3")
        else:
            ccalignments[(species, chain_type)] = read_alignment(
                os.path.join(fasta_path, "%s_%sC.fasta" % (species, chain_type)), region_name="C-REGION")

        all_valignments[(species, chain_type)] = read_alignment(
            os.path.join(fasta_path, "%s_%sV.fasta" % (species, chain_type)), region_name="V-REGION", read_all=True)
        all_jalignments[(species, chain_type)] = read_alignment(
            os.path.join(fasta_path, "%s_%sJ.fasta" % (species, chain_type)), region_name="J-REGION", read_all=True)

print("\nTRs")
for species in all_tr_species:
    for chain_type in "ABGD":
        if not os.path.isfile(os.path.join(fasta_path, "%s_%sV.fasta" % (species, chain_type))):
            continue

        print(species, chain_type)
        valignments[(species, chain_type)] = read_alignment(
            os.path.join(fasta_path, "%s_%sV.fasta" % (species, chain_type)))
        jalignments[(species, chain_type)] = read_alignment(
            os.path.join(fasta_path, "%s_%sJ.fasta" % (species, chain_type)))
        all_valignments[(species, chain_type)] = read_alignment(
            os.path.join(fasta_path, "%s_%sV.fasta" % (species, chain_type)), read_all=True)
        all_jalignments[(species, chain_type)] = read_alignment(
            os.path.join(fasta_path, "%s_%sJ.fasta" % (species, chain_type)), read_all=True)

valignments = format_v_genes(valignments)
jalignments = format_j_genes(jalignments)

ccalignments = format_c_genes(ccalignments, 'CC')
c1alignments = format_c_genes(c1alignments, 'C1')
c2alignments = format_c_genes(c2alignments, 'C2')
c3alignments = format_c_genes(c3alignments, 'C3')

all_valignments = format_v_genes(all_valignments)
all_jalignments = format_j_genes(all_jalignments)

all_C_alignments = {"CC": ccalignments, "C1": c1alignments, "C2": c2alignments, "C2": c2alignments}

write_germlines(all_valignments, all_jalignments)

# Combine the alignments to make putative germline alignments (obviously no d gene in there for Hs)
# Write them to a stockholm alignment file.
combined_sequences = make_putative_alignments(valignments, jalignments)

# Write the constant domains each to file.
output_C_alignments(ccalignments, 'CC')
output_C_alignments(c1alignments, 'C1')
output_C_alignments(c2alignments, 'C2')
output_C_alignments(c3alignments, 'C3')