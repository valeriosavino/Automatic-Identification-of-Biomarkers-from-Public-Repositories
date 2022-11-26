import psycopg2

def createCSVInput():
	conn = psycopg2.connect(database="hpatlas", user="postgres", password="root", host="127.0.0.1", port= "5432")
	conn.autocommit = True

	cur = conn.cursor()

	#soglia di probabilità
	p = 0.2

	#preparazione script per "file unico"
	#t, c, gene1,...., genen, cancer
	#metto inizialmente tessuto cellula, da gene1 a genen COMUNE metto le concentrazioni
	#colonna finale sarà cancer da prevedere

	#associazione gene -> nome del gene
	cur.execute(""" SELECT * 
					FROM gene_names
					WHERE ensembl IN (SELECT DISTINCT gene FROM pathology
									  INTERSECT
					  				  SELECT DISTINCT gene FROM normal_tissue)
					ORDER BY ensembl""")
	rs_gene_names = cur.fetchall()
	genes = {}
	[genes.setdefault(row[0], None) for row in rs_gene_names]
	for row in rs_gene_names:
		if(genes[row[0]]) == None:
			genes[row[0]] = row[1]

	#faccio intersezione di "gene", poichè ogni COLONNA sarà il "gene" comune a normal e pathology
	cur.execute("""SELECT DISTINCT gene FROM pathology
					INTERSECT
					SELECT DISTINCT gene FROM normal_tissue
					ORDER BY gene""")
	rs_gene = cur.fetchall()

	#assegnazione ad ogni tessuto un indice
	cur.execute("""SELECT DISTINCT tissue FROM tissue_celltype_cancer""")
	rs_tissue = cur.fetchall()
	tissues = {}
	i=1
	for row in rs_tissue:
		tissue = row[0]
		if '\'' in row[0]:
			tissue = row[0].replace('\'', '\'\'')
		tissues[tissue] = i
		i+=1

	#assegnazione ad ogni tipo di cellula un indice
	cur.execute("""SELECT DISTINCT cell_type FROM tissue_celltype_cancer""")
	rs_cell_type = cur.fetchall()
	cell_types = {}
	i=1
	for row in rs_cell_type:
		cell_type = row[0]
		if '\'' in row[0]:
			cell_type = row[0].replace('\'', '\'\'')
		cell_types[cell_type] = i
		i+=1

	#assegnazione ad ogni tumore un indice
	cur.execute("""SELECT DISTINCT cancer FROM pathology ORDER BY cancer""")
	rs_cancer = cur.fetchall()
	cancers = {}
	i=1
	for row in rs_cancer:
		cancers[row[0]] = i
		i+=1

	with open('csv_input.csv', 'w') as outfile:
		outfile.write("Tissue,Cell type,")
		for gene in genes:
			outfile.write(genes[gene])
			outfile.write(',')
		outfile.write('Cancer\n')

		#creo il dizionario per i vari geni
		file_matrix = {}
		file_matrix['0'] = ['', '', '']
		file_matrix['1'] = ['', '', ''] 

		for row in rs_gene:
			#preparo un array per ogni gene
			file_matrix[row[0]] = [0,0,0]

		#seleziono tutti i tessuti e cell_types
		cur.execute("""SELECT tissue, cell_type, cancer
						FROM tissue_celltype_cancer
					""")
		rs_tc = cur.fetchall()

		for row in rs_tc:
			#risoluzione problema con stringhe che contengono il carattere ' al loro interno
			tissue = row[0]
			if '\'' in row[0]:
				tissue = row[0].replace('\'', '\'\'')
			cell_type = row[1]
			if '\'' in row[1]:
				cell_type = row[1].replace('\'', '\'\'')
			
			#matrice per la stampa sul file, le prime 2 colonne contengono l'accoppiata tissue - cell_type
			file_matrix['0'][0] = file_matrix['0'][1] = file_matrix['0'][2] = tissues[tissue]
			file_matrix['1'][0] = file_matrix['1'][1] = file_matrix['1'][2] = cell_types[cell_type]

			cur.execute("""SELECT p.gene, p.high, p.medium, p.low
							FROM tissue_celltype_cancer AS t, pathology AS p
							WHERE t.tissue = \'"""+tissue+"""\' AND t.cell_type = \'"""+cell_type+"""\' 
							AND p.cancer = t.cancer AND p.gene IN (SELECT DISTINCT gene FROM pathology
																	INTERSECT
																	SELECT DISTINCT gene FROM normal_tissue)
							ORDER BY p.gene
						""")
			rs = cur.fetchall()
			if(len(rs) != 0):
				for result in rs:
					nv_h = 0
					nv_m = 0
					nv_l = 0
					#livello high
					if(result[1] is not None):
						nv_h = result[1]
					#livello medium
					if(result[2] is not None):
						nv_m = result[2]
					#livello low
					if(result[3] is not None):
						nv_l = result[3]

					n = nv_h+nv_m+nv_l

					prop_h = 0
					prop_m = 0
					prop_l = 0
					
					if(n!=0):	
						#Prob(t, c, g, v)
						prop_h = round(nv_h/n, 3)
						prop_m = round(nv_m/n, 3)
						prop_l = round(nv_l/n, 3)

					#Controllo per le proprietà che superano la soglia p
					if(prop_h >= p):
						file_matrix[result[0]][0] = prop_h
					else:
						file_matrix[result[0]][0] = 0
					if(prop_m >= p):
						file_matrix[result[0]][1] = prop_m
					else:
						file_matrix[result[0]][1] = 0
					if(prop_l >= p):
						file_matrix[result[0]][2] = prop_l
					else:
						file_matrix[result[0]][2] = 0
			
				#stampa su file
				#oss: prime 2 colonne della matrice sono tissue e cell_type, poi le concentrazioni per i vari geni, infine il cancer da prevedere
				for c in range(3):
					for r in file_matrix.keys():
						outfile.write(str(file_matrix[r][c]))
						outfile.write(',')
					#stampa del cancer da prevedere
					outfile.write(str(cancers[row[2]]))
					outfile.write('\n')	

			file_matrix['0'] = ['', '', '']
			file_matrix['1'] = ['', '', ''] 
		
		for row in rs_gene:
			#preparo un array per ogni gene
			file_matrix[row[0]] = [0,0,0]

		for row in rs_tc:
			#risoluzione problema con stringhe che contengono il carattere ' al loro interno
			tissue = row[0]
			if '\'' in row[0]:
				tissue = row[0].replace('\'', '\'\'')
			cell_type = row[1]
			if '\'' in row[1]:
				cell_type = row[1].replace('\'', '\'\'')
			
			#matrice per la stampa sul file, le prime 2 colonne contengono l'accoppiata tissue - cell_type
			file_matrix['0'][0] = file_matrix['0'][1] = file_matrix['0'][2] = tissues[tissue]
			file_matrix['1'][0] = file_matrix['1'][1] = file_matrix['1'][2] = cell_types[cell_type]

			cur.execute("""SELECT n.gene, n.level
							FROM normal_tissue as n
							WHERE n.tissue = \'"""+tissue+"""\' AND n.cell_type = \'"""+cell_type+"""\' 
							AND n.gene IN (SELECT DISTINCT gene FROM pathology
											INTERSECT
											SELECT DISTINCT gene FROM normal_tissue)
							ORDER BY n.gene
						""")
			rs = cur.fetchall()

			if(len(rs) != 0):
				for result in rs:
					if(result[0] in file_matrix.keys()):
						#livello high
						if(result[1] == "High"):
							file_matrix[result[0]][0] = 1-p
						else:
							file_matrix[result[0]][0] = 0
						#livello medium
						if(result[1] == "Medium"):
							file_matrix[result[0]][1] = 1-p
						else:
							file_matrix[result[0]][1] = 0
						#livello low
						if(result[1] == "Low"):
							file_matrix[result[0]][2] = 1-p
						else:
							file_matrix[result[0]][2] = 0
						#livello not detected
						if(result[1] == "Not detected"):
							file_matrix[result[0]][0] = file_matrix[result[0]][1] = file_matrix[result[0]][2] = 0

				#stampa su file
				#oss: prime 2 colonne della matrice sono tissue e cell_type, poi le concentrazioni per i vari geni, infine il cancer da prevedere
				for c in range(3):
					for r in file_matrix.keys():
						outfile.write(str(file_matrix[r][c]))
						outfile.write(',')
					#stampa del cancer da prevedere (paziente sano, metto 0)
					outfile.write('0')
					outfile.write('\n')	

			file_matrix['0'] = ['', '', '']
			file_matrix['1'] = ['', '', '']
		outfile.close()