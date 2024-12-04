from Bio import AlignIO
import numpy as np
import matplotlib.pyplot as plt


alignment = AlignIO.read("filasteria.fasta", "fasta")


alignment_length = alignment.get_alignment_length()
identities = []
for pos in range(alignment_length):
    column = alignment[:, pos]
    num_matches = sum(column.count(base) for base in set(column) if base != '-')
    identity = num_matches / len(column) * 100
    identities.append(identity)



introns = [pos for pos in range(alignment_length) if "-" in alignment[:, pos]]


plt.figure(figsize=(10, 5)) 
plt.plot(range(1, alignment_length + 1), identities, color='purple', linewidth=6)  
plt.bar(range(1, alignment_length + 1), identities, color='violet', alpha=0.4)  
plt.scatter(introns, [0] * len(introns), color='orange', marker='|', s=100, label='Intrones')
plt.xlabel('Posición')
plt.ylabel('Porcentaje de Identidad')
plt.title('Porcentaje de Identidad en cada Posición del Alineamiento')
plt.legend()
plt.grid(True)


plt.savefig('porcentaje_identidad.pdf', format='pdf', dpi=300)
plt.show()
