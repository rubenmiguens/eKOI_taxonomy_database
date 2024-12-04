import os
import subprocess
import re
import xml.etree.ElementTree as ET

def parse_fasta(fasta_file):
    data = []
    with open(fasta_file, "r") as fasta:
        current_record = None
        for line in fasta:
            if line.startswith(">"):
                if current_record is not None:
                    data.append(current_record)
                current_record = {"header": line.strip(), "sequence": ""}
            else:
                current_record["sequence"] += line.strip()
        if current_record is not None:
            data.append(current_record)
    return data

def create_output_folder():
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    records = root.findall(".//INSDSeq")

    unique_sequences = set()
    data = []
    for record in records:
        sequence_element = record.find("INSDSeq_sequence")
        if sequence_element is not None and sequence_element.text:
            sequence = sequence_element.text
            if sequence not in unique_sequences:
                unique_sequences.add(sequence)
                locus = record.find("INSDSeq_locus").text
                taxonomy = re.sub(r"\s+", "", record.find("INSDSeq_taxonomy").text)
                organism = re.sub(r"\s+", "_", record.find("INSDSeq_organism").text)
                data.append({"locus": locus, "taxonomy": taxonomy, "organism": organism, "sequence": sequence})

    return data

def write_fasta(data, fasta_output_file):
    with open(fasta_output_file, "w") as fasta_file:
        for record in data:
            header = f">{record['locus']} {record['taxonomy']};{record['organism']}\n"
            sequence = record['sequence'] + "\n"
            fasta_file.write(header)
            fasta_file.write(sequence)

def filter_sequences_by_size(data):
    return [record for record in data if 200 <= len(record['sequence']) <= 2000]

def perform_vsearch_clustering(data, output_folder, identity_threshold):
    temp_input_path = os.path.join(output_folder, "temp_input.fasta")

    with open(temp_input_path, "w") as temp_input_file:
        for record in data:
            temp_input_file.write(f">{record['locus']} {record['taxonomy']};{record['organism']}\n")
            temp_input_file.write(record['sequence'] + "\n")

    print(f"Temp input file created: {temp_input_path}")

    cluster_output_path = os.path.join(output_folder, "clustered_sequences.fasta")

    vsearch_cmd = [
        "vsearch",
        "--cluster_fast", temp_input_path,
        "--id", f"{identity_threshold / 100.0}",
        "--centroids", cluster_output_path
    ]

    print(f"Running VSEARCH command: {' '.join(vsearch_cmd)}")

    subprocess.run(vsearch_cmd)

    return cluster_output_path

def detect_chimeras(data, output_folder):
    temp_input_path = os.path.join(output_folder, "temp_input.fasta")
    
    with open(temp_input_path, "w") as temp_input_file:
        for record in data:
            if 'header' in record:
                temp_input_file.write(f">{record['header'][1:]}\n")
            elif 'locus' in record and 'taxonomy' in record and 'organism' in record:
                temp_input_file.write(f">{record['locus']} {record['taxonomy']};{record['organism']}\n")
            else:
                print(f"Formato de encabezado no reconocido: {record}")
                continue
            
            temp_input_file.write(record['sequence'] + "\n")

    print(f"Temp input file created: {temp_input_path}")

    chimeras_output_path = os.path.join(output_folder, "chimeric_sequences.fasta")

    vsearch_cmd = [
        "vsearch",
        "--uchime_denovo", temp_input_path,
        "--nonchimeras", chimeras_output_path
    ]

    try:
        subprocess.run(vsearch_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running VSEARCH command: {e}")
        return []

    with open(chimeras_output_path, "r") as chimeras_output_file:
        content = chimeras_output_file.read()
        print(f"Content of chimeric_sequences.fasta after VSEARCH:\n{content}")


    chimeric_data = parse_fasta(chimeras_output_path)

    return chimeric_data


def write_clean_fasta(clustered_sequences, original_fasta_file, clean_fasta_output, chimeric_sequences_output):

    taxonomy_info_dict = {}
    with open(original_fasta_file, "r") as original_fasta:
        for line in original_fasta:
            if line.startswith(">"):
                parts = line.strip().split(' ', 1)
                identifier = parts[0][1:]
                taxonomy_info = parts[1] if len(parts) > 1 else ""
                taxonomy_info_dict[identifier] = taxonomy_info


    with open(clean_fasta_output, "w") as clean_fasta_file:
        for record in clustered_sequences:
            identifier = record['header'][1:]
            taxonomy_info = taxonomy_info_dict.get(identifier, "")
            new_header = f">{record['header'][1:]} {taxonomy_info}\n"
            
            sequence = record['sequence'] + "\n"
            clean_fasta_file.write(new_header)
            clean_fasta_file.write(sequence)


    chimeric_data = detect_chimeras(clustered_sequences, output_folder)


    with open(chimeric_sequences_output, "w") as chimeric_file:
        for record in chimeric_data:
            chimeric_file.write(f">{record['header'][1:]}\n")
            chimeric_file.write(record['sequence'] + "\n")


    print(f"Número de secuencias quimeras: {len(chimeric_data)}")

if __name__ == "__main__":
    create_output_folder()

    xml_file = "sequence.gbc.xml"
    fasta_output_file = "archivo7.fasta"

    data = parse_xml(xml_file)
    original_sequence_count = len(data)


    filtered_data = filter_sequences_by_size(data)
    unique_sequence_count = len(filtered_data)


    write_fasta(filtered_data, fasta_output_file)

    output_folder = "output"  
    os.makedirs(output_folder, exist_ok=True)

    identity_threshold = 88.0  

 
    clustered_sequences_path = perform_vsearch_clustering(filtered_data, output_folder, identity_threshold)

 
    clustered_data = parse_fasta(clustered_sequences_path)
    clustered_sequence_count = len(clustered_data)


    for record in clustered_data:
        print(f"Header: {record['header']}")
        print(f"Sequence Length: {len(record['sequence'])}")
        print("-" * 30)


    representatives = {record['header']: record for record in clustered_data}


    clean_fasta_output = "clean.fasta"
    chimeric_sequences_output = "chimeric_sequences.fasta"
    write_clean_fasta(representatives.values(), fasta_output_file, clean_fasta_output, chimeric_sequences_output)

    chimeric_data = detect_chimeras(clustered_data, output_folder)
    chimeric_sequence_count = len(chimeric_data)

    print("\nResumen Final:")
    print(f"Número de secuencias originales: {original_sequence_count}")
    print(f"Número de secuencias después de eliminar duplicadas: {unique_sequence_count}")
    print(f"Número de secuencias después del filtrado de tamaño: {len(filtered_data)}")
    print(f"Número de secuencias después del clustering: {clustered_sequence_count}")




    print(f"Diferencia después del clustering: {clustered_sequence_count - chimeric_sequence_count}")

    print("Clustering and representative selection completed.")
