import psycopg2

def createTables():
    conn = psycopg2.connect(database="hpatlas", user="postgres", password="root", host="127.0.0.1", port= "5432")
    conn.autocommit = True

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS gene_names 
        (
            ensembl VARCHAR(255),
            name    VARCHAR(255),
            PRIMARY KEY (ensembl, name)
        );
        """)

    f = open("gene_names.csv", 'r')
    cur.copy_from(f, 'gene_names', sep=',')
    f.close()

    print('Tabella gene_names creata correttamente.')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tissue_celltype_cancer 
        (
            tissue      VARCHAR(255),
            cell_type   VARCHAR(255),
            cancer      VARCHAR(255),
            srcURL      VARCHAR(511),
            PRIMARY KEY (tissue, cell_type, cancer)
        );
        """)

    f = open("tissue_celltype.csv", 'r')
    cur.copy_from(f, 'tissue_celltype_cancer', sep=',')
    f.close()

    print('Tabella tissue_celltype_cancer creata correttamente.')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS location_go 
        (
            go_id VARCHAR(255) PRIMARY KEY,
            location_name    VARCHAR(255)
        );
        """)

    f = open("loc_go_nodup.csv", 'r')
    #caso particolare per colpa di un duplicato
    next(f)
    cur.copy_from(f, 'location_go', sep=',')
    f.close()

    print('Tabella location_go creata correttamente.')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS subcellular_location
        (   
            gene                VARCHAR(255)    NOT NULL,
            reliability         VARCHAR(255)    NOT NULL,
            go_id               VARCHAR(255)    NOT NULL,
            main_location       VARCHAR(255)    NOT NULL,
            extracellular_loc   VARCHAR(255)    NOT NULL,
            ehnanced            VARCHAR(255)    NOT NULL,
            supported           VARCHAR(255)    NOT NULL,
            approved            VARCHAR(255)    NOT NULL,
            uncertain           VARCHAR(255)    NOT NULL,
            single_cell_variation_intensity     VARCHAR(255)    NOT NULL,
            single_cell_variation_spatial       VARCHAR(255)    NOT NULL,
            cell_cycle_dependency               VARCHAR(255)    NOT NULL,
            PRIMARY KEY (gene, go_id)
        );
        """)

    f = open("gene_go.csv", 'r')
    cur.copy_from(f, 'subcellular_location', sep=',')
    f.close()

    print('Tabella subcellular_location creata correttamente.')


    cur.execute("""
        CREATE TABLE IF NOT EXISTS normal_tissue
        (   
            gene        VARCHAR(255)    NOT NULL,
            tissue      VARCHAR(255)    NOT NULL,
            cell_type   VARCHAR(255)    NOT NULL,
            level       VARCHAR(255)    NOT NULL,
            reliability VARCHAR(255)    NOT NULL,
            PRIMARY KEY (gene, tissue, cell_type)
        );
        """)

    f = open("normal_tissue.csv", 'r')
    cur.copy_from(f, 'normal_tissue', sep=',')
    f.close()

    print('Tabella normal_tissue creata correttamente.')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pathology
        (   
            gene        VARCHAR(255)    NOT NULL,
            cancer      VARCHAR(255)    NOT NULL,
            high            INT,
            medium          INT,
            low             INT,
            not_detected    INT,
            prognostic_favorable        NUMERIC,
            unprognostic_favorable      NUMERIC,
            prognostic_unfavorable      NUMERIC,
            unprognostic_unfavorable    NUMERIC,
            PRIMARY KEY (gene, cancer)
        );
        ALTER TABLE pathology ALTER COLUMN high TYPE INT USING (high::integer); 
        ALTER TABLE pathology ALTER COLUMN medium TYPE INT USING (medium::integer); 
        ALTER TABLE pathology ALTER COLUMN low TYPE INT USING (low::integer); 
        ALTER TABLE pathology ALTER COLUMN not_detected TYPE INT USING (not_detected::integer); 
        """)

    f = open("pathology.csv", 'r')
    cur.copy_from(f, 'pathology', sep=',', null='')
    f.close()

    print('Tabella pathology creata correttamente.\n')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS protein_atlas_basic
        (
            ensembl             VARCHAR(255)    PRIMARY KEY,
            gene_description    VARCHAR(255),
            uniprot             VARCHAR(255),
            chromosome          VARCHAR(255),
            position            VARCHAR(255),
            protein_class       VARCHAR(511),
            biological_process  VARCHAR(511),
            molecular_function  VARCHAR(255),
            disease_involvement VARCHAR(255)
        );
        """)

    f = open("protein_atlas_basic.csv", 'r')
    cur.copy_from(f, 'protein_atlas_basic', sep=',')
    f.close()

    print('Tabella protein_atlas_basic creata correttamente.\n')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rna_blood_cell
        (   
            gene        VARCHAR(255)    NOT NULL,
            blood_cell  VARCHAR(255)    NOT NULL,
            TPM         VARCHAR(255),
            pTPM        VARCHAR(255),
            nTPM        VARCHAR(255),
            PRIMARY KEY (gene, blood_cell)
        );
        """)

    f = open("rna_blood_cell.csv", 'r')
    cur.copy_from(f, 'rna_blood_cell', sep=',')
    f.close()

    print('Tabella rna_blood_cell creata correttamente.\n')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rna_blood_cell_monaco
        (   
            gene        VARCHAR(255)    NOT NULL,
            blood_cell  VARCHAR(255)    NOT NULL,
            TPM         VARCHAR(255),
            pTPM        VARCHAR(255),
            PRIMARY KEY (gene, blood_cell)
        );
        """)

    f = open("rna_blood_cell_monaco.csv", 'r')
    cur.copy_from(f, 'rna_blood_cell_monaco', sep=',')
    f.close()

    print('Tabella rna_blood_cell_monaco creata correttamente.\n')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rna_blood_cell_sample
        (   
            sample_id   VARCHAR(255)    NOT NULL,
            donor       VARCHAR(255)    NOT NULL,
            immune_cell VARCHAR(255)    NOT NULL,
            gene        VARCHAR(255)    NOT NULL,
            TPM     VARCHAR(255),
            pTPM    VARCHAR(255),
            nTPM    VARCHAR(255),
            PRIMARY KEY (donor, immune_cell, gene)
        );
        """)

    f = open("rna_blood_cell_sample.csv", 'r')
    cur.copy_from(f, 'rna_blood_cell_sample', sep=',')
    f.close()

    print('Tabella rna_blood_cell_sample creata correttamente.\n')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rna_blood_cell_schmiedel
        (   
            gene        VARCHAR(255)    NOT NULL,
            blood_cell  VARCHAR(255)    NOT NULL,
            TPM         VARCHAR(255),
            PRIMARY KEY (gene, blood_cell)
        );
        """)

    f = open("rna_blood_cell_schmiedel.csv", 'r')
    cur.copy_from(f, 'rna_blood_cell_schmiedel', sep=',')
    f.close()

    print('Tabella rna_blood_cell_schmiedel creata correttamente.\n')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rna_brain_fantom
        (   
            gene                VARCHAR(255)    NOT NULL,
            brain_region        VARCHAR(255)    NOT NULL,
            tags_per_million    VARCHAR(255),
            scaled_tags_per_million VARCHAR(255),  
            nTPM                VARCHAR(255),
            PRIMARY KEY (gene, brain_region)
        );
        """)

    f = open("rna_brain_fantom.csv", 'r')
    cur.copy_from(f, 'rna_brain_fantom', sep=',')
    f.close()

    print('Tabella rna_brain_fantom creata correttamente.\n')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rna_brain_gtex
        (   
            gene        VARCHAR(255)    NOT NULL,
            brain_region    VARCHAR(255)    NOT NULL,
            TPM VARCHAR(255),
            pTPM    VARCHAR(255),  
            nTPM    VARCHAR(255),
            PRIMARY KEY (gene, brain_region)
        );
        """)

    f = open("rna_brain_gtex.csv", 'r')
    cur.copy_from(f, 'rna_brain_gtex', sep=',')
    f.close()

    print('Tabella rna_brain_gtex creata correttamente.\n')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rna_cancer_sample
        (   
            gene        VARCHAR(255)    NOT NULL,
            sample      VARCHAR(255)    NOT NULL,
            cancer  VARCHAR(255)    NOT NULL,
            FPKM    VARCHAR(255),
            PRIMARY KEY (gene, sample, cancer)
        );
        """)

    f = open("rna_cancer_sample.csv", 'r')
    cur.copy_from(f, 'rna_cancer_sample', sep=',')
    f.close()

    print('Tabella rna_cancer_sample creata correttamente.\n')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rna_cell_line
        (   
            gene        VARCHAR(255)    NOT NULL,
            cell_line   VARCHAR(255)    NOT NULL,
            TPM VARCHAR(255),
            pTPM    VARCHAR(255),  
            nTPM    VARCHAR(255),
            PRIMARY KEY (gene, cell_line)
        );
        """)

    f = open("rna_cell_line.csv", 'r')
    cur.copy_from(f, 'rna_cell_line', sep=',')
    f.close()

    print('Tabella rna_cell_line creata correttamente.\n')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rna_single_cell_type
        (   
            gene        VARCHAR(255)    NOT NULL,
            cell_type   VARCHAR(255)    NOT NULL,
            nTPM        VARCHAR(255),
            PRIMARY KEY (gene, cell_type)
        );
        """)

    f = open("rna_single_cell_type.csv", 'r')
    cur.copy_from(f, 'rna_single_cell_type', sep=',')
    f.close()

    print('Tabella rna_single_cell_type creata correttamente.\n')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rna_single_cell_type_tissue
        (   
            gene        VARCHAR(255)    NOT NULL,
            tissue      VARCHAR(255)    NOT NULL,
            cluster VARCHAR(255)    NOT NULL,
            cell_type   VARCHAR(255)    NOT NULL,
            read_count  VARCHAR(255)    NOT NULL,
            pTPM    VARCHAR(255),
            PRIMARY KEY (gene, cell_type, tissue, cluster)
        );
        """)

    f = open("rna_single_cell_type_tissue.csv", 'r')
    cur.copy_from(f, 'rna_single_cell_type_tissue', sep=',')
    f.close()

    print('Tabella rna_single_cell_type_tissue creata correttamente.\n')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rna_tissue_consensus
        (   
            gene        VARCHAR(255)    NOT NULL,
            tissue      VARCHAR(255)    NOT NULL,
            nTPM    VARCHAR(255),
            PRIMARY KEY (gene, tissue)
        );
        """)

    f = open("rna_tissue_consensus.csv", 'r')
    cur.copy_from(f, 'rna_tissue_consensus', sep=',')
    f.close()

    print('Tabella rna_tissue_consensus creata correttamente.\n')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rna_tissue_fantom
        (   
            gene        VARCHAR(255)    NOT NULL,
            tissue  VARCHAR(255)    NOT NULL,
            tags_per_million    VARCHAR(255),
            scaled_tags_per_million VARCHAR(255),  
            normalized_tags_per_million VARCHAR(255),
            PRIMARY KEY (gene, tissue)
        );
        """)

    f = open("rna_tissue_fantom.csv", 'r')
    cur.copy_from(f, 'rna_tissue_fantom', sep=',')
    f.close()

    print('Tabella rna_tissue_fantom creata correttamente.\n')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rna_tissue_gtex
        (   
            gene        VARCHAR(255)    NOT NULL,
            tissue  VARCHAR(255)    NOT NULL,
            TPM     VARCHAR(255),
            pTPM    VARCHAR(255),  
            nTPM    VARCHAR(255),
            PRIMARY KEY (gene, tissue)
        );
        """)

    f = open("rna_tissue_gtex.csv", 'r')
    cur.copy_from(f, 'rna_tissue_gtex', sep=',')
    f.close()

    print('Tabella rna_tissue_gtex creata correttamente.\n')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rna_tissue_hpa
        (
            gene        VARCHAR(255)    NOT NULL,
            tissue  VARCHAR(255)    NOT NULL,
            TPM     VARCHAR(255),
            pTPM    VARCHAR(255),  
            nTPM    VARCHAR(255),
            PRIMARY KEY (gene, tissue)
        );
        """)

    f = open("rna_tissue_hpa.csv", 'r')
    cur.copy_from(f, 'rna_tissue_hpa', sep=',')
    f.close()

    print('Tabella rna_tissue_hpa creata correttamente.\n')

    cur.execute("""
        ALTER TABLE gene_names ADD CONSTRAINT fk_gnn FOREIGN KEY (ensembl) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE normal_tissue ADD CONSTRAINT fk_nt FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE pathology ADD CONSTRAINT fk_p FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE rna_blood_cell ADD CONSTRAINT fk_rbc FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE rna_blood_cell_monaco ADD CONSTRAINT fk_rbcm FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE rna_blood_cell_sample ADD CONSTRAINT fk_rbcs FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE rna_blood_cell_schmiedel ADD CONSTRAINT fk_rbcsc FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE rna_brain_fantom ADD CONSTRAINT fk_rbf FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE rna_brain_gtex ADD CONSTRAINT fk_rbg FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE rna_cancer_sample ADD CONSTRAINT fk_rcs FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE rna_cell_line ADD CONSTRAINT fk_rcl FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE rna_single_cell_type ADD CONSTRAINT fk_rsct FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE rna_single_cell_type_tissue ADD CONSTRAINT fk_rsctt FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE rna_tissue_consensus ADD CONSTRAINT fk_rtc FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE rna_tissue_fantom ADD CONSTRAINT fk_rtf FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE rna_tissue_gtex ADD CONSTRAINT fk_rtg FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE rna_tissue_hpa ADD CONSTRAINT fk_rth FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE subcellular_location ADD CONSTRAINT fke_scl FOREIGN KEY (gene) REFERENCES protein_atlas_basic (ensembl);
        ALTER TABLE subcellular_location ADD CONSTRAINT fkg_scl FOREIGN KEY (go_id) REFERENCES location_go (go_id);
    """)

    #chiusura cur
    cur.close()

    #Closing the connection
    conn.close()