import os
import zipfile
import re
from urllib.request import urlopen, HTTPError, URLError
import transform
import createDB
import createTables
import csv_builder_single_file

def functionManager():
	initDownload()
	transform.TSVtoCSV()
	deleteFile()
	createDB.createDB()
	createTables.createTables()
	csv_builder_single_file.createCSVInput()

def initDownload():

	#scarica i file
	furl = [["normal_tissue.zip", "https://www.proteinatlas.org/download/normal_tissue.tsv.zip"],
			["pathology.zip", "https://www.proteinatlas.org/download/pathology.tsv.zip"],
			["subcellular_location.zip", "https://www.proteinatlas.org/download/subcellular_location.tsv.zip"],
			["rna_tissue_consensus.zip", "https://www.proteinatlas.org/download/rna_tissue_consensus.tsv.zip"],
			["rna_tissue_hpa.zip", "https://www.proteinatlas.org/download/rna_tissue_hpa.tsv.zip"],
			["rna_tissue_gtex.zip", "https://www.proteinatlas.org/download/rna_tissue_gtex.tsv.zip"],
			["rna_tissue_fantom.zip", "https://www.proteinatlas.org/download/rna_tissue_fantom.tsv.zip"],
			["rna_single_cell_type.zip", "https://www.proteinatlas.org/download/rna_single_cell_type.tsv.zip"],
			["rna_single_cell_type_tissue.zip", "https://www.proteinatlas.org/download/rna_single_cell_type_tissue.tsv.zip"],
			["rna_brain_gtex.zip", "https://www.proteinatlas.org/download/rna_brain_gtex.tsv.zip"],
			["rna_brain_fantom.zip", "https://www.proteinatlas.org/download/rna_brain_fantom.tsv.zip"],
			["rna_blood_cell.zip", "https://www.proteinatlas.org/download/rna_blood_cell.tsv.zip"],
			["rna_blood_cell_sample.zip", "https://www.proteinatlas.org/download/rna_blood_cell_sample.tsv.zip"],
			["rna_blood_cell_sample_tpm_m.zip", "https://www.proteinatlas.org/download/rna_blood_cell_sample_tpm_m.tsv.zip"],
			["rna_blood_cell_monaco.zip", "https://www.proteinatlas.org/download/rna_blood_cell_monaco.tsv.zip"],
			["rna_blood_cell_schmiedel.zip", "https://www.proteinatlas.org/download/rna_blood_cell_schmiedel.tsv.zip"],
			["rna_cell_line.zip", "https://www.proteinatlas.org/download/rna_celline.tsv.zip"],
			["rna_cancer_sample.zip", "https://www.proteinatlas.org/download/rna_cancer_sample.tsv.zip"],
			["protein_atlas.zip", "https://www.proteinatlas.org/download/proteinatlas.tsv.zip"]]


	for i in range(len(furl)):
		print("Sto scaricando "+furl[i][0]+"...")
		fln = os.path.join(os.getcwd(), furl[i][0])
		target = urlopen(furl[i][1])
		meta = target.info()
		filesize = float(meta['Content-Length'])
		chunks = 1024 * 5
		with open(fln, "wb") as f:
			while True:
				parts = target.read(chunks)
				if not parts:
					break

				f.write(parts)

		#estrazione zip	
		with zipfile.ZipFile(fln, 'r') as zip_ref:
			print("Sto estraendo "+furl[i][0]+"...")
			zip_ref.extractall(os.getcwd())
		f.close()	

def deleteFile():
	#Cancella i file superflui
	if os.path.exists("normal_tissue.zip"):
		os.remove("normal_tissue.zip")
	if os.path.exists("normal_tissue.tsv"):
		os.remove("normal_tissue.tsv")

	if os.path.exists("pathology.zip"):
		os.remove("pathology.zip")
	if os.path.exists("pathology.tsv"):
		os.remove("pathology.tsv")

	if os.path.exists("subcellular_location.zip"):
		os.remove("subcellular_location.zip")
	if os.path.exists("subcellular_location.tsv"):
		os.remove("subcellular_location.tsv")
	if os.path.exists("loc_go.csv"):
		os.remove("loc_go.csv")

	if os.path.exists("rna_tissue_consensus.zip"):
		os.remove("rna_tissue_consensus.zip")
	if os.path.exists("rna_tissue_consensus.tsv"):
		os.remove("rna_tissue_consensus.tsv")

	if os.path.exists("rna_tissue_hpa.zip"):
		os.remove("rna_tissue_hpa.zip")
	if os.path.exists("rna_tissue_hpa.tsv"):
		os.remove("rna_tissue_hpa.tsv")

	if os.path.exists("rna_tissue_gtex.zip"):
		os.remove("rna_tissue_gtex.zip")
	if os.path.exists("rna_tissue_gtex.tsv"):
		os.remove("rna_tissue_gtex.tsv")

	if os.path.exists("rna_tissue_fantom.zip"):
		os.remove("rna_tissue_fantom.zip")
	if os.path.exists("rna_tissue_fantom.tsv"):
		os.remove("rna_tissue_fantom.tsv")

	if os.path.exists("rna_single_cell_type.zip"):
		os.remove("rna_single_cell_type.zip")
	if os.path.exists("rna_single_cell_type.tsv"):
		os.remove("rna_single_cell_type.tsv")

	if os.path.exists("rna_single_cell_type_tissue.zip"):
		os.remove("rna_single_cell_type_tissue.zip")
	if os.path.exists("rna_single_cell_type_tissue.tsv"):
		os.remove("rna_single_cell_type_tissue.tsv")

	if os.path.exists("rna_brain_gtex.zip"):
		os.remove("rna_brain_gtex.zip")
	if os.path.exists("rna_brain_gtex.tsv"):
		os.remove("rna_brain_gtex.tsv")
	
	if os.path.exists("rna_brain_fantom.zip"):
		os.remove("rna_brain_fantom.zip")
	if os.path.exists("rna_brain_fantom.tsv"):
		os.remove("rna_brain_fantom.tsv")
	
	if os.path.exists("rna_blood_cell.zip"):
		os.remove("rna_blood_cell.zip")
	if os.path.exists("rna_blood_cell.tsv"):
		os.remove("rna_blood_cell.tsv")

	if os.path.exists("rna_blood_cell_sample.zip"):
		os.remove("rna_blood_cell_sample.zip")
	if os.path.exists("rna_blood_cell_sample.tsv"):
		os.remove("rna_blood_cell_sample.tsv")

	if os.path.exists("rna_blood_cell_sample_tpm_m.zip"):
		os.remove("rna_blood_cell_sample_tpm_m.zip")
	if os.path.exists("rna_blood_cell_sample_tpm_m.tsv"):
		os.remove("rna_blood_cell_sample_tpm_m.tsv")

	if os.path.exists("rna_blood_cell_monaco.zip"):
		os.remove("rna_blood_cell_monaco.zip")
	if os.path.exists("rna_blood_cell_monaco.tsv"):
		os.remove("rna_blood_cell_monaco.tsv")

	if os.path.exists("rna_blood_cell_schmiedel.zip"):
		os.remove("rna_blood_cell_schmiedel.zip")
	if os.path.exists("rna_blood_cell_schmiedel.tsv"):
		os.remove("rna_blood_cell_schmiedel.tsv")

	if os.path.exists("rna_cell_line.zip"):
		os.remove("rna_cell_line.zip")
	if os.path.exists("rna_celline.tsv"):
		os.remove("rna_celline.tsv")

	if os.path.exists("rna_cancer_sample.zip"):
		os.remove("rna_cancer_sample.zip")
	if os.path.exists("rna_cancer_sample.tsv"):
		os.remove("rna_cancer_sample.tsv")

	if os.path.exists("protein_atlas.zip"):
		os.remove("protein_atlas.zip")
	if os.path.exists("proteinatlas.tsv"):
		os.remove("proteinatlas.tsv")

functionManager()