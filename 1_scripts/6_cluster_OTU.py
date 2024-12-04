from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import os
import csv


def calculate_distance(seq1, seq2):
    return sum(1 for a, b in zip(seq1, seq2) if a != b) / len(seq1)


def group_sequences(fasta_file, similarity_threshold):

    sequences = []
    sequence_names = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequences.append(record.seq)
        sequence_names.append(record.id)
    

    groups = []
    grouped_indices = []


    for i in range(len(sequences)):
        if i not in grouped_indices:
            group_indices = [i]
            for j in range(i+1, len(sequences)):
                if j not in grouped_indices:
                    dist = calculate_distance(sequences[i], sequences[j])
                    if dist <= similarity_threshold:
                        group_indices.append(j)
                        grouped_indices.append(j)
            groups.append(group_indices)
    
    return sequences, sequence_names, groups


def write_fasta(output_filename, sequences, sequence_names):
    with open(output_filename, "w") as output_file:
        for seq, name in zip(sequences, sequence_names):
          
            output_file.write(f">{name}\n{seq}\n")


def write_csv(output_filename, sequence_names, groups, fasta_name):
    with open(output_filename, "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Sequence Name', 'Group', 'Fasta Name'])
        for i, group in enumerate(groups):
            for idx in group:
                writer.writerow([sequence_names[idx], i+1, fasta_name])


output_folder = "final"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


input_fasta = "input.fasta"

similarity_threshold = 0.03


sequences, sequence_names, groups = group_sequences(input_fasta, similarity_threshold)


if groups:

    for i, group in enumerate(groups):
        output_filename = os.path.join(output_folder, f"group_{i+1}.fasta")
        write_fasta(output_filename, [sequences[idx] for idx in group], [sequence_names[idx] for idx in group])


    representative_sequences = [sequences[group[0]] for group in groups]
    representative_sequence_names = [f"{os.path.basename(input_fasta)}_representative_{i+1}" for i in range(len(groups))]
    output_representative_filename = os.path.join(output_folder, "representative_sequences.fasta")
    write_fasta(output_representative_filename, representative_sequences, representative_sequence_names)


    output_csv_filename = os.path.join(output_folder, "classification_results.csv")
    write_csv(output_csv_filename, sequence_names, groups, os.path.basename(input_fasta))
else:
    print("No se encontraron grupos de secuencias similares.")
