import pandas as pd
import os


script_directory = os.path.dirname(os.path.abspath(__file__))


excel_files = [file for file in os.listdir(script_directory) if file.endswith('.xlsx')]


combined_data = pd.DataFrame()


for file in excel_files:
    file_path = os.path.join(script_directory, file)
    df = pd.read_excel(file_path, engine='openpyxl')
    combined_data = pd.concat([combined_data, df])


filo_counts = combined_data['Secuencia Asignada'].str.split(';', expand=True)[4].value_counts()


promedio_filo = filo_counts / len(combined_data)


promedio_filo.to_csv(os.path.join(script_directory, 'promedio_filo.csv'))

print("Promedio de proporción de secuencias asignadas a cada filo:")
print(promedio_filo)
print("Se ha generado el archivo 'promedio_filo.csv' con la información.")
