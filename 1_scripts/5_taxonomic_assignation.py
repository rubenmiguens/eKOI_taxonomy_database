import os
import subprocess
import pandas as pd


base_de_datos = "combined_limpio.fasta"


porcentaje_minimo = 84


archivos_fasta = [archivo for archivo in os.listdir() if archivo.endswith('.fasta') and archivo != base_de_datos]


for archivo_fasta in archivos_fasta:

    nombre_carpeta = os.path.splitext(archivo_fasta)[0]
    os.makedirs(nombre_carpeta, exist_ok=True)


    nombre_archivo = os.path.splitext(archivo_fasta)[0]


    comando = f"vsearch --usearch_global {archivo_fasta} --db {base_de_datos} --id 0.84 --blast6out {nombre_carpeta}/{nombre_archivo}_resultados.txt --quiet"
    subprocess.run(comando, shell=True)


    resultados = []


    with open(f"{nombre_carpeta}/{nombre_archivo}_resultados.txt", 'r') as f:
        for linea in f:
            campos = linea.strip().split('\t')
            nombre_secuencia = campos[0]
            porcentaje_similitud = float(campos[2])
            secuencia_asignada = campos[1]
            resultados.append((nombre_secuencia, porcentaje_similitud, secuencia_asignada))


    df = pd.DataFrame(resultados, columns=['Nombre de la Secuencia', 'Porcentaje de Similitud', 'Secuencia Asignada'])

 
    nombre_excel = f"{nombre_carpeta}/{nombre_archivo}_resultados.xlsx"
    df.to_excel(nombre_excel, index=False)


    df_filtrado = df[df['Porcentaje de Similitud'] >= porcentaje_minimo]


    df_filtrado['Secuencia Asignada'] = df_filtrado['Secuencia Asignada'].str.split(';')


    for group_name, group_df in df_filtrado.groupby(df_filtrado['Secuencia Asignada'].str[4]):

        fasta_filename = f"{nombre_carpeta}/{group_name}_{nombre_archivo}.fasta"
        with open(fasta_filename, 'w') as fasta_file:

            secuencias_grupo = group_df['Nombre de la Secuencia'].tolist()

            with open(archivo_fasta, 'r') as original_fasta:
                for linea in original_fasta:
                    if linea.startswith('>'):
                        nombre_secuencia = linea.strip()[1:]
                        if nombre_secuencia in secuencias_grupo:
                            fasta_file.write(linea)
                            fasta_file.write(next(original_fasta))  


    nombre_excel_filtrado = f"{nombre_carpeta}/{nombre_archivo}_resultados_filtrados.xlsx"
    df_filtrado.to_excel(nombre_excel_filtrado, index=False)
