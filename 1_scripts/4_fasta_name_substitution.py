from Bio import SeqIO


csv_file = "todo.csv"


new_info = {}
with open(csv_file, "r") as f:
    for line in f:
        line = line.strip().split(";")
        identifier = line[0].split()[0]  
        info = ";".join(line[1:])
        new_info[identifier] = info


fasta_file = "meteora.fasta"
output_file = "meteora_final.fasta"

with open(output_file, "w") as output_handle:
    for record in SeqIO.parse(fasta_file, "fasta"):
        identifier = record.id.split()[0]  
        if identifier in new_info:

            new_name = "{} {}".format(identifier, new_info[identifier])
            sequence = str(record.seq).replace("\n", "")  
            output_handle.write(">{}\n{}\n".format(new_name, sequence))
        else:
            print("No se encontró información para el identificador:", identifier)

print("¡Secuencias modificadas y guardadas en", output_file)
