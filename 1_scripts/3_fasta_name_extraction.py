def limpiar_nombre(nombre):

    nombre_limpio = nombre.replace("_COX1_CDS", "")

    nombre_limpio = nombre_limpio.replace(" ", ";")
    return nombre_limpio

def leer_archivo_fasta(archivo_entrada):
    secuencias = {}
    with open(archivo_entrada, 'r') as fasta:
        nombre = ''
        secuencia = ''
        for linea in fasta:
            if linea.startswith('>'):
                if nombre:
                    secuencias[limpiar_nombre(nombre)] = secuencia
                nombre = linea.strip()[1:]
                secuencia = ''
            else:
                secuencia += linea.strip()

        if nombre:
            secuencias[limpiar_nombre(nombre)] = secuencia
    return secuencias

def escribir_csv(secuencias, archivo_salida):
    with open(archivo_salida, 'w') as csv_file:
        csv_file.write("Nombre de la secuencia\n")
        for nombre_secuencia in secuencias:
            csv_file.write(f"{nombre_secuencia}\n")

if __name__ == "__main__":
    archivo_entrada = "KOI_taxonomy.fasta"
    archivo_salida = "KOI_taxonomy.csv"

    secuencias = leer_archivo_fasta(archivo_entrada)
    escribir_csv(secuencias, archivo_salida)

    print("CSV generado correctamente.")
