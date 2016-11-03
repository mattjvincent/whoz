-- noinspection SqlNoDataSourceInspectionForFile
-- create chromosome table
DROP TABLE IF EXISTS chromosomes;
CREATE TABLE chromosomes (
   _chromosomes_key INTEGER,
   chromosome_num INTEGER,
   chromosome TEXT,
   species_id TEXT,
   PRIMARY KEY (_chromosomes_key)
);

-- insert chromosome data
INSERT INTO chromosomes VALUES (null, 1, '1', 'Mm');
INSERT INTO chromosomes VALUES (null, 2, '2', 'Mm');
INSERT INTO chromosomes VALUES (null, 3, '3', 'Mm');
INSERT INTO chromosomes VALUES (null, 4, '4', 'Mm');
INSERT INTO chromosomes VALUES (null, 5, '5', 'Mm');
INSERT INTO chromosomes VALUES (null, 6, '6', 'Mm');
INSERT INTO chromosomes VALUES (null, 7, '7', 'Mm');
INSERT INTO chromosomes VALUES (null, 8, '8', 'Mm');
INSERT INTO chromosomes VALUES (null, 9, '9', 'Mm');
INSERT INTO chromosomes VALUES (null, 10, '10', 'Mm');
INSERT INTO chromosomes VALUES (null, 11, '11', 'Mm');
INSERT INTO chromosomes VALUES (null, 12, '12', 'Mm');
INSERT INTO chromosomes VALUES (null, 13, '13', 'Mm');
INSERT INTO chromosomes VALUES (null, 14, '14', 'Mm');
INSERT INTO chromosomes VALUES (null, 15, '15', 'Mm');
INSERT INTO chromosomes VALUES (null, 16, '16', 'Mm');
INSERT INTO chromosomes VALUES (null, 17, '17', 'Mm');
INSERT INTO chromosomes VALUES (null, 18, '18', 'Mm');
INSERT INTO chromosomes VALUES (null, 19, '19', 'Mm');
INSERT INTO chromosomes VALUES (null, 20, 'X', 'Mm');
INSERT INTO chromosomes VALUES (null, 21, 'Y', 'Mm');
INSERT INTO chromosomes VALUES (null, 22, 'MT', 'Mm');
INSERT INTO chromosomes VALUES (null, 1, '1', 'Hs');
INSERT INTO chromosomes VALUES (null, 2, '2', 'Hs');
INSERT INTO chromosomes VALUES (null, 3, '3', 'Hs');
INSERT INTO chromosomes VALUES (null, 4, '4', 'Hs');
INSERT INTO chromosomes VALUES (null, 5, '5', 'Hs');
INSERT INTO chromosomes VALUES (null, 6, '6', 'Hs');
INSERT INTO chromosomes VALUES (null, 7, '7', 'Hs');
INSERT INTO chromosomes VALUES (null, 8, '8', 'Hs');
INSERT INTO chromosomes VALUES (null, 9, '9', 'Hs');
INSERT INTO chromosomes VALUES (null, 10, '10', 'Hs');
INSERT INTO chromosomes VALUES (null, 11, '11', 'Hs');
INSERT INTO chromosomes VALUES (null, 12, '12', 'Hs');
INSERT INTO chromosomes VALUES (null, 13, '13', 'Hs');
INSERT INTO chromosomes VALUES (null, 14, '14', 'Hs');
INSERT INTO chromosomes VALUES (null, 15, '15', 'Hs');
INSERT INTO chromosomes VALUES (null, 16, '16', 'Hs');
INSERT INTO chromosomes VALUES (null, 17, '17', 'Hs');
INSERT INTO chromosomes VALUES (null, 18, '18', 'Hs');
INSERT INTO chromosomes VALUES (null, 19, '19', 'Hs');
INSERT INTO chromosomes VALUES (null, 20, '20', 'Hs');
INSERT INTO chromosomes VALUES (null, 21, '21', 'Hs');
INSERT INTO chromosomes VALUES (null, 22, '22', 'Hs');
INSERT INTO chromosomes VALUES (null, 23, 'X', 'Hs');
INSERT INTO chromosomes VALUES (null, 24, 'Y', 'Hs');
INSERT INTO chromosomes VALUES (null, 25, 'MT', 'Hs');

-- create chromosome indices
CREATE INDEX idx_chromosomes_cnum ON chromosomes (chromosome_num ASC);
CREATE INDEX idx_chromosomes_chrom ON chromosomes (chromosome ASC);
CREATE INDEX idx_chromosomes_species ON chromosomes (species_id ASC);

-- remove the data for the chromosomes we aren't bothering with
DELETE FROM ensembl_genes_tmp WHERE chromosome_name NOT IN (SELECT chromosome FROM chromosomes);

-- create some indices to speed up updates and lookups
CREATE INDEX idx_crossref ON mgi_ensemblids_tmp (crossReferences_identifier ASC);
CREATE INDEX idx_crossref_externalid ON ensembl_genes_tmp (external_id ASC);
CREATE INDEX idx_species_id_tmp ON ensembl_genes_tmp (species_id ASC);
CREATE INDEX idx_mgi_genes_tmp ON mgi_genes_tmp (primaryIdentifier ASC);

-- update the mgi_ids
UPDATE ensembl_genes_tmp
   SET external_id = (SELECT primaryIdentifier
                        FROM mgi_ensemblids_tmp
                       WHERE crossReferences_identifier = ensembl_genes_tmp.ensembl_gene_id)
WHERE species_id = 'Mm'
  AND external_gene_db != 'MGI Symbol';

/*
-- DEBUGGING
-- ensembl ids with multiple mgi ids
select count(1), ensembl_gene_id
from ensembl_genes_tmp
group by ensembl_gene_id
and species_id = 'Mm'
having count(1) > 1;

-- mgi ids with multiple ensembl ids
select count(1), mgi_id
from ensembl_genes_mm_tmp
group by mgi_id
having count(1) > 1;

select * from ensembl_genes_mm_tmp where ensembl_gene_id in (select ensembl_gene_id from (select count(1), ensembl_gene_id
from ensembl_genes_mm_tmp
group by ensembl_gene_id
having count(1) > 1));
*/

-- there is a primary mgi_id, so let's get it
ALTER TABLE ensembl_genes_tmp ADD COLUMN primary_mgi_id TEXT;

UPDATE ensembl_genes_tmp
   SET primary_mgi_id = external_id
 WHERE ensembl_gene_id IN (SELECT ensembl_gene_id
                             FROM (SELECT count(1), ensembl_gene_id
                                     FROM ensembl_genes_tmp
                                    WHERE species_id = 'Mm'
                                    GROUP BY ensembl_gene_id
                                   HAVING count(1) > 1)
                           )
   AND description like '%'||external_id||']'
   AND species_id ='Mm';

CREATE INDEX idx_primary_mgi_id_tmp ON ensembl_genes_tmp (primary_mgi_id ASC);

DROP TABLE IF EXISTS updater;
CREATE TEMP TABLE updater AS
    SELECT *
      FROM ensembl_genes_tmp
     WHERE ensembl_gene_id in (SELECT ensembl_gene_id
                                 FROM (SELECT count(1), ensembl_gene_id
                                         FROM ensembl_genes_tmp
                                        WHERE species_id = 'Mm'
                                        GROUP BY ensembl_gene_id
                                       HAVING count(1) > 1)
                               )
       AND primary_mgi_id is not null
       AND species_id = 'Mm';

UPDATE ensembl_genes_tmp
   SET primary_mgi_id = (SELECT primary_mgi_id
                           FROM updater
                          WHERE ensembl_gene_id = ensembl_genes_tmp.ensembl_gene_id)
 WHERE ensembl_gene_id in (SELECT ensembl_gene_id
                            FROM updater)
   AND species_id = 'Mm';

UPDATE ensembl_genes_tmp
   SET primary_mgi_id = external_id
 WHERE primary_mgi_id is null
   AND species_id = 'Mm';

-- create the ensembl_genes table
DROP TABLE IF EXISTS ensembl_genes;
CREATE TABLE ensembl_genes (
   _ensembl_genes_key INTEGER,
   ensembl_gene_id TEXT,
   external_id TEXT,
   species_id TEXT,
   symbol TEXT,
   name TEXT,
   description TEXT,
   synonyms TEXT,
   chromosome TEXT,
   start_position INTEGER,
   end_position INTEGER,
   strand INTEGER,
   PRIMARY KEY (_ensembl_genes_key)
);

DELETE
  FROM ensembl_genes_tmp
 WHERE species_id = 'Mm'
   AND external_id IS NOT NULL
   AND external_id != primary_mgi_id;


-- insert the mouse data
INSERT
  INTO ensembl_genes
SELECT distinct null,
       e.ensembl_gene_id,
       e.primary_mgi_id,
       'Mm',
       m.symbol,
       m.name,
       m.description,
       null,
       e.chromosome_name,
       e.start_position,
       e.end_position,
       e.strand
  FROM ensembl_genes_tmp e, mgi_genes_tmp m
 WHERE e.primary_mgi_id = m.primaryIdentifier
   AND e.species_id = 'Mm';

-- there could be multiple records not yet ported
UPDATE ensembl_genes_tmp
   SET external_id = null,
       primary_mgi_id = null
 WHERE species_id = 'Mm'
   AND ensembl_gene_id NOT IN (SELECT ensembl_gene_id
                                 FROM ensembl_genes
                                WHERE species_id = 'Mm');

INSERT
  INTO ensembl_genes
SELECT distinct null,
       e.ensembl_gene_id,
       e.primary_mgi_id,
       'Mm',
       e.external_gene_symbol,
       null,
       e.description,
       null,
       e.chromosome_name,
       e.start_position,
       e.end_position,
       e.strand
  FROM ensembl_genes_tmp e
 WHERE e.ensembl_gene_id NOT IN (SELECT ensembl_gene_id FROM ensembl_genes WHERE species_id = 'Mm')
   AND e.species_id = 'Mm';


-- should be no rows
SELECT count(1), ensembl_gene_id
  FROM ensembl_genes
 GROUP BY ensembl_gene_id
HAVING count(1) > 1;


-- create some indices on the human data
CREATE INDEX hugo_genes_tmp_idx1 ON hugo_genes_tmp (hugo_id ASC);
CREATE INDEX hugo_genes_tmp_idx2 ON hugo_genes_tmp (ensembl_gene_id ASC);

-- update the external_id
UPDATE ensembl_genes_tmp
   SET external_id = (SELECT hugo_id
                        FROM hugo_genes_tmp
                       WHERE ensembl_gene_id = ensembl_genes_tmp.ensembl_gene_id
                         AND ensembl_genes_tmp.species_id = 'Hs')
 WHERE external_id = 'HGNC:'
   AND species_id = 'Hs';

-- there is a primary hugo_id, so let's get it
ALTER TABLE ensembl_genes_tmp ADD COLUMN primary_hgnc_id TEXT;

UPDATE ensembl_genes_tmp
   SET primary_hgnc_id = external_id
 WHERE species_id = 'Hs'
   AND ensembl_gene_id in (SELECT ensembl_gene_id
                             FROM (SELECT count(1), ensembl_gene_id
                                     FROM ensembl_genes_tmp
                                    WHERE species_id = 'Hs'
                                    GROUP BY ensembl_gene_id
                                   HAVING count(1) > 1)
                           )
   AND description like '%'||substr(external_id,6)||']';

DROP TABLE IF EXISTS updater;
CREATE TEMP TABLE updater AS
   SELECT *
     FROM ensembl_genes_tmp
    WHERE ensembl_gene_id in (SELECT ensembl_gene_id
                                FROM (SELECT count(1), ensembl_gene_id
                                        FROM ensembl_genes_tmp
                                       WHERE species_id = 'Hs'
                                       GROUP BY ensembl_gene_id
                                      HAVING count(1) > 1)
                              )
      AND primary_hgnc_id is not null
      AND species_id = 'Hs';
UPDATE ensembl_genes_tmp
   SET primary_hgnc_id = (SELECT primary_hgnc_id
                            FROM updater
                           WHERE ensembl_gene_id = ensembl_genes_tmp.ensembl_gene_id
                             AND ensembl_genes_tmp.species_id ='Hs')
 WHERE ensembl_gene_id in (SELECT ensembl_gene_id
                             FROM updater)
   AND species_id = 'Hs';

UPDATE ensembl_genes_tmp
   SET primary_hgnc_id = external_id
 WHERE primary_hgnc_id is null
   AND species_id = 'Hs';

CREATE INDEX idx_primary_hgnc_id_tmp ON ensembl_genes_tmp (primary_hgnc_id ASC);

DELETE
  FROM ensembl_genes_tmp
 WHERE species_id = 'Hs'
   AND external_id IS NOT NULL
   AND external_id != primary_hgnc_id;

-- insert the human data
INSERT
  INTO ensembl_genes
SELECT distinct null,
       e.ensembl_gene_id,
       e.primary_hgnc_id,
       'Hs',
       h.gene_symbol,
       h.gene_name,
       null,
       null,
       e.chromosome_name,
       e.start_position,
       e.end_position,
       e.strand
  FROM ensembl_genes_tmp e, hugo_genes_tmp h
 WHERE e.primary_hgnc_id = h.hugo_id
   AND e.species_id = 'Hs'
 UNION
SELECT distinct null,
       e.ensembl_gene_id,
       e.primary_hgnc_id,
       'Hs',
       e.external_id,
       null,
       e.description,
       null,
       e.chromosome_name,
       e.start_position,
       e.end_position,
       e.strand
  FROM ensembl_genes_tmp e
 WHERE (length(e.external_id) = 0 or e.external_id is null)
   AND e.species_id = 'Hs';


UPDATE ensembl_genes_tmp
   SET external_id = null,
       primary_hgnc_id = null
 WHERE species_id = 'Hs'
   AND ensembl_gene_id NOT IN (SELECT ensembl_gene_id
                                 FROM ensembl_genes
                                 WHERE species_id = 'Hs');

INSERT
  INTO ensembl_genes
SELECT distinct null,
       e.ensembl_gene_id,
       e.primary_hgnc_id,
       'Hs',
       e.external_gene_symbol,
       null,
       e.description,
       null,
       e.chromosome_name,
       e.start_position,
       e.end_position,
       e.strand
  FROM ensembl_genes_tmp e
 WHERE e.ensembl_gene_id NOT IN (SELECT ensembl_gene_id FROM ensembl_genes WHERE species_id = 'Hs')
   AND e.species_id = 'Hs';

-- should be no rows
SELECT count(1), ensembl_gene_id
  FROM ensembl_genes
 GROUP BY ensembl_gene_id
HAVING count(1) > 1;


UPDATE ensembl_genes
   SET description = null
 WHERE description = ''
    OR description = '\N';

UPDATE ensembl_genes
   SET synonyms = null
 WHERE synonyms = ''
    OR synonyms = '\N';

UPDATE ensembl_genes
   SET external_id = null
 WHERE length(external_id) = 0;

UPDATE ensembl_genes
   SET symbol = null
 WHERE length(symbol) = 0;

UPDATE ensembl_genes
   SET name = null
 WHERE length(name) = 0;

UPDATE ensembl_genes
   SET description = null
 WHERE length(description) = 0;

UPDATE ensembl_genes
   SET synonyms = null
 WHERE length(synonyms) = 0;


--update the gtep table with blank protein ids
UPDATE ensembl_gtep_tmp
   SET protein_id = null
 WHERE protein_id = '';

-- create the lookup table
DROP TABLE IF EXISTS ensembl_genes_lookup;
CREATE TABLE ensembl_genes_lookup (
   _ensembl_genes_lookup_key INTEGER,
   ensembl_gene_id TEXT,
   lookup_value TEXT COLLATE NOCASE,
   ranking_id TEXT,
   species_id TEXT,
   PRIMARY KEY (_ensembl_genes_lookup_key)
);
DROP TABLE IF EXISTS ensembl_genes_lookup_tmp;
CREATE TABLE ensembl_genes_lookup_tmp (
   ensembl_gene_id TEXT,
   lookup_value TEXT,
   ranking_id TEXT,
   species_id TEXT
);

-- insert ensembl genes
INSERT
  INTO ensembl_genes_lookup_tmp
SELECT distinct
       e.ensembl_gene_id,
       e.ensembl_gene_id,
       'EG',
       e.species_id
  FROM ensembl_genes e;

-- insert gene symbols
INSERT
  INTO ensembl_genes_lookup_tmp
SELECT distinct
       e.ensembl_gene_id,
       e.symbol,
       'GS',
       e.species_id
  FROM ensembl_genes e
 WHERE e.symbol is not null;

-- insert gene names
INSERT
  INTO ensembl_genes_lookup_tmp
SELECT distinct
       e.ensembl_gene_id,
       e.name,
       'GN',
       e.species_id
  FROM ensembl_genes e
 WHERE e.name is not null;

-- insert mgi ids
INSERT
  INTO ensembl_genes_lookup_tmp
SELECT distinct e.ensembl_gene_id,
       e.external_id,
       'MI',
       'Mm'
  FROM ensembl_genes_tmp e
  WHERE e.species_id = 'Mm';

-- insert hugo/hgnc ids
INSERT
  INTO ensembl_genes_lookup_tmp
SELECT distinct
       e.ensembl_gene_id,
       e.external_id,
       'HI',
       'Hs'
  FROM ensembl_genes_tmp e
  WHERE e.species_id = 'Hs';

-- insert mouse synonyms
INSERT
  INTO ensembl_genes_lookup_tmp
SELECT distinct
       e.ensembl_gene_id,
       m.synonyms_value,
       'GY',
       e.species_id
  FROM ensembl_genes e,
       mgi_synonyms_tmp m
 WHERE m.primaryIdentifier = e.external_id
   AND m.symbol != m.synonyms_value;

-- insert human synonyms
INSERT
  INTO ensembl_genes_lookup_tmp
SELECT distinct
       e.ensembl_gene_id,
       h.synonym_type,
       'GY',
       e.species_id
  FROM ensembl_genes e,
       hugo_synonyms_tmp h
 WHERE e.ensembl_gene_id = h.ensembl_gene_id
   AND h.synonym = 'Y';

-- insert exon_ids
INSERT
  INTO ensembl_genes_lookup_tmp
SELECT distinct
       e.ensembl_gene_id,
       m.exon_id,
       'EE',
       e.species_id
  FROM ensembl_genes e,
       ensembl_gtep_tmp m
 WHERE e.ensembl_gene_id = m.gene_id;

-- insert transcript ids
INSERT
  INTO ensembl_genes_lookup_tmp
SELECT distinct
       e.ensembl_gene_id,
       m.transcript_id,
       'ET',
       e.species_id
  FROM ensembl_genes e,
       ensembl_gtep_tmp m
 WHERE e.ensembl_gene_id = m.gene_id;

-- insert protein ids
INSERT
  INTO ensembl_genes_lookup_tmp
SELECT distinct
       e.ensembl_gene_id,
       m.protein_id,
       'EP',
       e.species_id
  FROM ensembl_genes e,
       ensembl_gtep_tmp m
 WHERE e.ensembl_gene_id = m.gene_id;

-- insert all the data
INSERT
  INTO ensembl_genes_lookup
SELECT distinct null,
       ensembl_gene_id,
       lookup_value,
       ranking_id,
       species_id TEXT
  FROM ensembl_genes_lookup_tmp
 WHERE lookup_value is not null
 ORDER BY ensembl_gene_id, lookup_value, ranking_id;

-- create some indices
CREATE INDEX idx_lookup_ensembl_gene_id ON ensembl_genes_lookup (ensembl_gene_id ASC);
CREATE INDEX idx_lookup_value ON ensembl_genes_lookup (lookup_value ASC);
CREATE INDEX idx_lookup_id ON ensembl_genes_lookup (ranking_id ASC);
CREATE INDEX idx_lookup_species_id ON ensembl_genes_lookup (species_id ASC);

-- see how much data we have
SELECT count(1), ranking_id
  FROM ensembl_genes_lookup
 GROUP BY ranking_id;

-- EP Ensembl Protein ID
-- EE Ensembl Exon ID
-- EG Ensembl Gene ID
-- ET Ensembl Transcript ID
-- GN Gene Name
-- GS Gene Symbol
-- GY Gene Synonym
-- HI Hugo ID
-- MI MGI ID


-- create the scoring/ranking table
DROP TABLE IF EXISTS search_ranking;
CREATE TABLE search_ranking (
   _search_ranking_key INTEGER,
   ranking_id TEXT,
   score INTEGER,
   description TEXT,
   PRIMARY KEY (_search_ranking_key)
);

-- insert the rankings
INSERT INTO search_ranking VALUES (null, 'EE',7000,'Ensembl Exon ID');
INSERT INTO search_ranking VALUES (null, 'EP',6500,'Ensembl Protein ID');
INSERT INTO search_ranking VALUES (null, 'EG',10000,'Ensembl Gene ID');
INSERT INTO search_ranking VALUES (null, 'ET',7500,'Ensembl Transcript ID');
INSERT INTO search_ranking VALUES (null, 'GN',5000,'Gene Name');
INSERT INTO search_ranking VALUES (null, 'GS',6000,'Gene Symbol');
INSERT INTO search_ranking VALUES (null, 'GY',2500,'Gene Synonym');
INSERT INTO search_ranking VALUES (null, 'HI',8000,'HGNC ID');
INSERT INTO search_ranking VALUES (null, 'MI',9000,'MGI ID');

-- create ranking indices
CREATE INDEX idx_search_ranking_ranking_id ON search_ranking (ranking_id ASC);
CREATE INDEX idx_search_ranking_score ON search_ranking (score ASC);

-- make sure we have the synonyms
CREATE INDEX idx_mgi_synonyms_oneline_tmp ON mgi_synonyms_oneline_tmp (primaryIdentifier ASC);

UPDATE ensembl_genes
   SET synonyms = (SELECT synonyms
                     FROM mgi_synonyms_oneline_tmp
                    WHERE primaryIdentifier = ensembl_genes.external_id)
 WHERE species_id = 'Mm';

UPDATE ensembl_genes
   SET synonyms = (SELECT replace(synonyms, ', ', '||')
                     FROM hugo_genes_tmp
                    WHERE ensembl_gene_id = ensembl_genes.ensembl_gene_id)
 WHERE species_id = 'Hs';

-- qtep
CREATE TABLE ensembl_gtep (
    _ensembl_gtep_key INTEGER,
    chromosome TEXT,
    strand INTEGER,
    gene_id TEXT,
    gene_start INTEGER,
    gene_end INTEGER,
    transcript_id TEXT,
    transcript_start INTEGER,
    transcript_end INTEGER,
    transcript_count INTEGER,
    exon_id TEXT,
    exon_start INTEGER,
    exon_end INTEGER,
    exon_rank INTEGER,
    protein_id TEXT,
    species_id TEXT,
    PRIMARY KEY (_ensembl_gtep_key)
);

INSERT
  INTO ensembl_gtep
SELECT distinct null,
       chromosome,
       strand,
       gene_id,
       gene_start,
       gene_end,
       transcript_id,
       transcript_start,
       transcript_end,
       transcript_count,
       exon_id,
       exon_start,
       exon_end,
       exon_rank,
       protein_id,
       species_id
  FROM ensembl_gtep_tmp
 ORDER BY species_id, chromosome, gene_start, transcript_start, exon_rank, protein_id;

CREATE INDEX idx_chromosome_qtep ON ensembl_gtep (chromosome ASC);
CREATE INDEX idx_species_id_qtep ON ensembl_gtep (species_id ASC);
CREATE INDEX idx_gene_id_qtep ON ensembl_gtep (gene_id ASC);
CREATE INDEX idx_transcript_id_qtep ON ensembl_gtep (transcript_id ASC);
CREATE INDEX idx_exon_id_qtep ON ensembl_gtep (exon_id ASC);
CREATE INDEX idx_protein_id_qtep ON ensembl_gtep (protein_id ASC);
CREATE INDEX idx_gene_start_qtep ON ensembl_gtep (gene_start ASC);
CREATE INDEX idx_transcript_start_qtep ON ensembl_gtep (transcript_start ASC);
CREATE INDEX idx_exon_start_qtep ON ensembl_gtep (exon_start ASC);

-- cleanup
DELETE
  FROM ensembl_genes_lookup
 WHERE length(lookup_value) = 0;

-- create another important index
CREATE INDEX idx_ensembl_gene_id ON ensembl_genes (ensembl_gene_id ASC);

-- create the search table
CREATE VIRTUAL TABLE ensembl_search USING fts4(_ensembl_genes_lookup_key, lookup_value);

INSERT
  INTO ensembl_search
SELECT _ensembl_genes_lookup_key, lookup_value
  FROM ensembl_genes_lookup;

-- drop some tables
DROP TABLE ensembl_genes_tmp;
DROP TABLE mgi_genes_tmp;
DROP TABLE mgi_ensemblids_tmp;
DROP TABLE mgi_synonyms_tmp;
DROP TABLE mgi_synonyms_oneline_tmp;
DROP TABLE hugo_genes_tmp;
DROP TABLE hugo_synonyms_tmp;
DROP TABLE ensembl_gtep_tmp;
DROP TABLE ensembl_genes_lookup_tmp;
