# eKOI Taxonomy Database
![logo](https://github.com/user-attachments/assets/880ef2a1-9181-420d-9e84-58d609e84f53)

# Project Overview
This repository contains data and scripts related to the analysis and curation of the eKOI database, which is based on the mitochondrial COI gene. Below is a detailed description of the folders and files included in this repository.

# Folders
- **1_scripts:**
Contains scripts used to generate various files and analyses.

- **2_alignment_eKOI:**
Alignments for each phylum, including sequences that constitute the final eKOI.fasta and eKOI_taxonomy_PR2.fasta files.

- **3_ASV_metabarcoding:**
Alignments and OTUs for each phylum derived from the taxonomically reannotated ASVs from metabarcoding studies using the eKOI database. The metadata file contains information about the samples and studies included.

- **4_alignment_phylogenetic_trees:**
Alignments and phylogenetic trees for each phylum, combining sequences from the eKOI database and taxonomically reannotated ASVs.

- **5_COI_databases_comparison:**
Comparison of the eKOI database with other databases based on the mitochondrial COI gene.

- **Tables:**
Contains supplementary tables with taxonomic information for each FASTA file.

- **Figures:**
Contains figures generated for the publication XXX.

# Files
- [eKOI_ver1.fasta](https://github.com/rubenmiguens/eKOI_taxonomy_database/blob/main/eKOI_ver1.fasta)
Final FASTA file with taxonomically curated sequences in the following format:
ID Domain;supergroup;division;subdivision;phylum;class;order;family;genus;species;accession

- [eKOI_taxonomy_PR2_ver1.fasta](https://github.com/rubenmiguens/eKOI_taxonomy_database/blob/main/eKOI_taxonomy_PR2_ver1.fasta)
Final FASTA file with taxonomically curated sequences formatted according to the PR2 taxonomy convention:
ID Domain;supergroup;division;subdivision;class;order;family;genus;species;accession

# Reference
- A Novel Taxonomic Database for eukaryotic Mitochondrial Cytochrome Oxidase subunit I Gene (eKOI): Enhancing taxonomic resolution at community-level in metabarcoding analyses
Ruben Gonzalez-Miguens, Alex Galvez-Morante, Margarita Skamnelou, Meritxell Anto, Elena Casacuberta, Daniel J. Richter, Daniel Vaulot, Javier del Campo, Inaki Ruiz-Trillo
bioRxiv 2024.12.05.626972; doi: https://doi.org/10.1101/2024.12.05.626972
