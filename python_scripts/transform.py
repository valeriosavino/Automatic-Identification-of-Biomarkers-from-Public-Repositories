import pandas as pd

#trasforma alcuni tsv in csv rimuovendo la prima riga e il nome dei geni di fianco all'ENSG
def transform(infile, outfile):
	next(infile)
	for line in infile:
		riga = line.strip().split('\t')
		outfile.write(riga[0])
		outfile.write(',')	
		for i in range(2, len(riga)):
			outfile.write(riga[i])
			if(i != len(riga)-1):
				outfile.write(',')
		outfile.write('\n')

def TSVtoCSV():
	with open('normal_tissue.tsv') as infile, open('normal_tissue.csv', 'w') as outfile:
		print("Sto convertendo normal_tissue...")
		transform(infile, outfile)
	
	with open('pathology.tsv') as infile, open('pathology.csv', 'w') as outfile:
		print("Sto convertendo pathology...")
		next(infile)
		for line in infile:
			newLine = line.replace('\t', ',')
			riga = newLine.strip().split(',')
			outfile.write(riga[0])
			outfile.write(',')	
			for i in range(2, len(riga)):
				outfile.write(riga[i])
				if(i != len(riga)-1):
					outfile.write(',')
			outfile.write('\n')

	with open('subcellular_location.tsv') as infile, open('gene_go.csv', 'w') as outfile, open('loc_go.csv', 'w') as outfile2:
		print("Sto convertendo subcellular_location...")
		next(infile)
		outfile2.write("Go_ID,Location\n")
		for line in infile:
			#14 colonne, lavorare su 0 (gene),  3 (main) e 13(goid)
			riga = line.strip().split('\t')
			#splitto go-id
			main_loc = riga[3].split(';')
			go_id = riga[13].split(';')
			for i in range(len(go_id)):
				#estrazione loc
				st_loc = 0
				end_loc = go_id[i].find('(')-1
				loc = go_id[i][st_loc:end_loc]

				#estrazione del go_id
				st_go = go_id[i].find('(')+1
				end_go = go_id[i].find(')')
				go = go_id[i][st_go:end_go]

				#scrittura file
                #gene
				outfile.write(riga[0])
				outfile.write(',')
				#rel
				outfile.write(riga[2])
				outfile.write(',')
				#goid
				if(loc == 'Rods & Rings'):
					go = 'NN:1111111'
				if(loc == 'Nucleoli rim'):
					go = go+".1"
				outfile.write(go)
				outfile.write(',')

				outfile2.write(go)
				outfile2.write(',')
				outfile2.write(loc)
				outfile2.write('\n')
				#attributo se main loc o no
				if(loc in main_loc):
					outfile.write("0,")
				else:
					outfile.write("1,")

                #extracellular-loc
				if(riga[5] == "Predicted to be secreted"):
					outfile.write("0,")
				else:
					outfile.write("1,")

                #se la location è presente nelle diverse colonne
                #ehnanced
				if(loc in riga[6]):
					outfile.write("0,")
				else:
					outfile.write("1,")
				#Supported
				if(loc in riga[7]):
					outfile.write("0,")
				else:
					outfile.write("1,")
				#Approved
				if(loc in riga[8]):
					outfile.write("0,")
				else:
					outfile.write("1,")
				#Uncertain
				if(loc in riga[9]):
					outfile.write("0,")
				else:
					outfile.write("1,")
				#Single-cell variation intensity
				if(loc in riga[10]):
					outfile.write("0,")
				else:
					outfile.write("1,")
				#Single-cell variation spatial
				if(loc in riga[11]):
					outfile.write("0,")
				else:
					outfile.write("1,")
				#Cell cycle dependency
				if(loc in riga[12]):
					outfile.write("0")
				else:
					outfile.write("1")

				outfile.write('\n')

	infile = "loc_go.csv"
	outfile = "loc_go_nodup.csv"

	df = pd.read_csv(infile, sep=",")
	df.drop_duplicates(subset=None, inplace=True)
	df.to_csv(outfile, index=False)   

	with open('rna_blood_cell.tsv') as infile, open('rna_blood_cell.csv', 'w') as outfile:
		print("Sto convertendo rna_blood_cell...")
		transform(infile, outfile)

	with open('rna_blood_cell_sample.tsv') as infile, open('rna_blood_cell_sample.csv', 'w') as outfile:
		print("Sto convertendo rna_blood_cell_sample...")
		next(infile)
		for line in infile:
			riga = line.strip().split('\t')	
			for i in range(4):
				outfile.write(riga[i])
				outfile.write(',')
			for i in range(5, len(riga)):
				outfile.write(riga[i])
				if(i != len(riga)-1):
					outfile.write(',')
			outfile.write('\n')

	with open('rna_blood_cell_monaco.tsv') as infile, open('rna_blood_cell_monaco.csv', 'w') as outfile:
		print("Sto convertendo rna_blood_cell_monaco...")
		transform(infile, outfile)

	with open('rna_blood_cell_schmiedel.tsv') as infile, open('rna_blood_cell_schmiedel.csv', 'w') as outfile:
		print("Sto convertendo rna_blood_cell_schmiedel...")
		transform(infile, outfile)

	with open('rna_brain_fantom.tsv') as infile, open('rna_brain_fantom.csv', 'w') as outfile:
		print("Sto convertendo rna_brain_fantom...")
		transform(infile, outfile)

	with open('rna_brain_gtex.tsv') as infile, open('rna_brain_gtex.csv', 'w') as outfile:
		print("Sto convertendo rna_brain_gtex...")
		transform(infile, outfile)

	with open('rna_celline.tsv') as infile, open('rna_cell_line.csv', 'w') as outfile:
		print("Sto convertendo rna_celline...")
		transform(infile, outfile)

	with open('rna_single_cell_type.tsv') as infile, open('rna_single_cell_type.csv', 'w') as outfile:
		print("Sto convertendo rna_single_cell_type...")
		transform(infile, outfile)

	with open('rna_single_cell_type_tissue.tsv') as infile, open('rna_single_cell_type_tissue.csv', 'w') as outfile:
		print("Sto convertendo rna_single_cell_type_tissue...")
		transform(infile, outfile)

	with open('rna_tissue_consensus.tsv') as infile, open('rna_tissue_consensus.csv', 'w') as outfile:
		print("Sto convertendo rna_tissue_consensus...")
		transform(infile, outfile)

	with open('rna_tissue_hpa.tsv') as infile, open('rna_tissue_hpa.csv', 'w') as outfile:
		print("Sto convertendo rna_tissue_hpa...")
		next(infile)
		for line in infile:
			riga = line.strip().split('\t')
			outfile.write(riga[0])
			outfile.write(',')	
			for i in range(2, len(riga)):
				if(i==2):
					riga[i] = riga[i].replace(',', ';')	
				outfile.write(riga[i])
				if(i != len(riga)-1):
					outfile.write(',')
			outfile.write('\n')

	with open('rna_tissue_fantom.tsv') as infile, open('rna_tissue_fantom.csv', 'w') as outfile:
		print("Sto convertendo rna_tissue_fantom...")
		transform(infile, outfile)

	with open('rna_tissue_gtex.tsv') as infile, open('rna_tissue_gtex.csv', 'w') as outfile:
		print("Sto convertendo rna_tissue_gtex...")
		transform(infile, outfile)

	with open('rna_cancer_sample.tsv') as infile, open('rna_cancer_sample.csv', 'w') as outfile:
		print("Sto convertendo rna_cancer_sample...")
		next(infile)
		for line in infile:
			riga = line.strip().split('\t')
			for i in range(len(riga)):
				outfile.write(riga[i])
				if(i != len(riga)-1):
					outfile.write(',')
			outfile.write('\n')
	
	with open('proteinatlas.tsv') as infile, open('gene_names.csv', 'w') as outfileNames, open('protein_atlas_basic.csv', 'w') as outfileProt:
		print("Sto convertendo proteinatlas...")
		next(infile)
		for line in infile:
			riga = line.strip().split('\t')
			outfileNames.write(riga[2])
			outfileNames.write(',')
			outfileNames.write(riga[0])
			outfileNames.write('\n')

			if(riga[1] != ''):
				if(riga[1][0] == '"'):
					riga[1] = riga[1][1:len(riga[1])-1]
				syn = riga[1].split(',')
				for i in range(len(syn)):
					outfileNames.write(riga[2])
					outfileNames.write(',')
					outfileNames.write(syn[i].strip())
					outfileNames.write('\n')

			for i in range(2,11):
				if(',' in riga[i]):
					riga[i] = riga[i].replace(',', ';')
				outfileProt.write(riga[i].strip('"'))
				if(i != 10):
					outfileProt.write(',')
			outfileProt.write('\n')