from __future__ import print_function

import copy


class Data:
    pass


ENSEMBL={}
ENSEMBL['chromosomes'] = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','X','Y','MT']

version = '54'
ENSEMBL[version] = Data()
ENSEMBL[version].date='May 2009'
ENSEMBL[version].url='http://may2009.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://may2009.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species={'mm':Data(), 'hs':Data()}
ENSEMBL[version].species['mm'].version='NCBI m37'
ENSEMBL[version].species['mm'].major_version='NCBI m37'
ENSEMBL[version].species['mm'].patch_version=''
ENSEMBL[version].species['mm'].external_id_prepend=''
ENSEMBL[version].species['mm'].external_id_column=1
ENSEMBL[version].species['mm'].genes_header='ensembl_gene_id\texternal_id\tchromosome_name\tstart_position\tend_position\tstrand\tdescription\texternal_gene_db\texternal_gene_symbol\tspecies_id'
ENSEMBL[version].species['mm'].genes_xml='''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "default" formatter = "CSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
    <Dataset name = "mmusculus_gene_ensembl" interface = "default" >
        <Attribute name = "ensembl_gene_id" />
        <Attribute name = "mgi_id" />
        <Attribute name = "chromosome_name" />
        <Attribute name = "start_position" />
        <Attribute name = "end_position" />
        <Attribute name = "strand" />
        <Attribute name = "description" />
        <Attribute name = "external_gene_db" />
        <Attribute name = "mgi_symbol" />
    </Dataset>
</Query>
'''
ENSEMBL[version].species['mm'].gte_header='chromosome\tstrand\tgene_id\tgene_start\tgene_end\ttranscript_id\ttranscript_start\ttranscript_end\ttranscript_count\texon_id\texon_start\texon_end\texon_rank\tprotein_id\tspecies_id'
ENSEMBL[version].species['mm'].gte_by_chrom=True
ENSEMBL[version].species['mm'].gte_xml='''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "default" formatter = "CSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
    <Dataset name = "mmusculus_gene_ensembl" interface = "default" >
        <Filter name = "chromosome_name" value = "{{CHROMOSOME}}"/>
        <Attribute name = "chromosome_name" />
        <Attribute name = "strand" />
        <Attribute name = "ensembl_gene_id" />
        <Attribute name = "start_position" />
        <Attribute name = "end_position" />
        <Attribute name = "ensembl_transcript_id" />
        <Attribute name = "transcript_start" />
        <Attribute name = "transcript_end" />
        <Attribute name = "transcript_count" />
        <Attribute name = "ensembl_exon_id" />
        <Attribute name = "exon_chrom_start" />
        <Attribute name = "exon_chrom_end" />
        <Attribute name = "rank" />
        <Attribute name = "ensembl_peptide_id" />
    </Dataset>
</Query>
'''
ENSEMBL[version].species['hs'].version='NCBI 36'
ENSEMBL[version].species['hs'].major_version='NCBI 36'
ENSEMBL[version].species['hs'].patch_version=''
ENSEMBL[version].species['hs'].external_id_prepend='HGNC:'
ENSEMBL[version].species['hs'].external_id_column=1
ENSEMBL[version].species['hs'].genes_header='ensembl_gene_id\texternal_id\tchromosome_name\tstart_position\tend_position\tstrand\tdescription\texternal_gene_db\texternal_gene_symbol\tspecies_id'
ENSEMBL[version].species['hs'].genes_xml='''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "default" formatter = "CSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
    <Dataset name = "hsapiens_gene_ensembl" interface = "default" >
        <Attribute name = "ensembl_gene_id" />
        <Attribute name = "hgnc_id" />
        <Attribute name = "chromosome_name" />
        <Attribute name = "start_position" />
        <Attribute name = "end_position" />
        <Attribute name = "strand" />
        <Attribute name = "description" />
        <Attribute name = "external_gene_db" />
        <Attribute name = "hgnc_symbol" />
    </Dataset>
</Query>
'''
ENSEMBL[version].species['hs'].gte_header='chromosome\tstrand\tgene_id\tgene_start\tgene_end\ttranscript_id\ttranscript_start\ttranscript_end\ttranscript_count\texon_id\texon_start\texon_end\texon_rank\tprotein_id\tspecies_id'
ENSEMBL[version].species['hs'].gte_by_chrom=True
ENSEMBL[version].species['hs'].gte_xml='''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "default" formatter = "CSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
    <Dataset name = "hsapiens_gene_ensembl" interface = "default" >
        <Filter name = "chromosome_name" value = "{{CHROMOSOME}}"/>
        <Attribute name = "chromosome_name" />
        <Attribute name = "strand" />
        <Attribute name = "ensembl_gene_id" />
        <Attribute name = "start_position" />
        <Attribute name = "end_position" />
        <Attribute name = "ensembl_transcript_id" />
        <Attribute name = "transcript_start" />
        <Attribute name = "transcript_end" />
        <Attribute name = "transcript_count" />
        <Attribute name = "ensembl_exon_id" />
        <Attribute name = "exon_chrom_start" />
        <Attribute name = "exon_chrom_end" />
        <Attribute name = "rank" />
        <Attribute name = "ensembl_peptide_id" />
    </Dataset>
</Query>
'''

version = '67'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['54'])
ENSEMBL[version].date='May 2012'
ENSEMBL[version].url='http://may2012.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://may2012.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='NCBIm37'
ENSEMBL[version].species['mm'].major_version='NCBIm37'
ENSEMBL[version].species['mm'].patch_version=''
ENSEMBL[version].species['hs'].version='GRCh37.p7'
ENSEMBL[version].species['hs'].major_version='GRCh37'
ENSEMBL[version].species['hs'].patch_version='p7'

version = '68'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['67'])
ENSEMBL[version].date='Jul 2012'
ENSEMBL[version].url='http://jul2012.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://jul2012.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version=''
ENSEMBL[version].species['hs'].version='GRCh37.p8'
ENSEMBL[version].species['hs'].major_version='GRCh37'
ENSEMBL[version].species['hs'].patch_version='p8'

version = '69'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['68'])
ENSEMBL[version].date='Oct 2012'
ENSEMBL[version].url='http://oct2012.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://oct2012.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version=''
ENSEMBL[version].species['hs'].version='GRCh37.p8'
ENSEMBL[version].species['hs'].major_version='GRCh37'
ENSEMBL[version].species['hs'].patch_version='p8'

version = '70'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['69'])
ENSEMBL[version].date='Jan 2013'
ENSEMBL[version].url='http://jan2013.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://jan2013.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p1'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p1'
ENSEMBL[version].species['hs'].version='GRCh37.p8'
ENSEMBL[version].species['hs'].major_version='GRCh37'
ENSEMBL[version].species['hs'].patch_version='p8'

version = '71'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['70'])
ENSEMBL[version].date='Apr 2013'
ENSEMBL[version].url='http://apr2013.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://apr2013.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p1'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p1'
ENSEMBL[version].species['hs'].version='GRCh37.p10'
ENSEMBL[version].species['hs'].major_version='GRCh37'
ENSEMBL[version].species['hs'].patch_version='p10'

version = '72'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['71'])
ENSEMBL[version].date='Jun 2013'
ENSEMBL[version].url='http://jun2013.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://jun2013.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p1'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p1'
ENSEMBL[version].species['hs'].version='GRCh37.p11'
ENSEMBL[version].species['hs'].major_version='GRCh37'
ENSEMBL[version].species['hs'].patch_version='p11'

version = '73'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['72'])
ENSEMBL[version].date='Sep 2013'
ENSEMBL[version].url='http://sep2013.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://sep2013.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p1'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p1'
ENSEMBL[version].species['hs'].version='GRCh37.p12'
ENSEMBL[version].species['hs'].major_version='GRCh37'
ENSEMBL[version].species['hs'].patch_version='p12'

version = '74'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['73'])
ENSEMBL[version].date='Dec 2013'
ENSEMBL[version].url='http://dec2013.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://dec2013.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p2'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p2'
ENSEMBL[version].species['hs'].version='GRCh37.p13'
ENSEMBL[version].species['hs'].major_version='GRCh37'
ENSEMBL[version].species['hs'].patch_version='p13'

version = '75'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['74'])
ENSEMBL[version].date='Feb 2014'
ENSEMBL[version].url='http://feb2014.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://feb2014.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p2'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p2'
ENSEMBL[version].species['hs'].version='GRCh37.p13'
ENSEMBL[version].species['hs'].major_version='GRCh37'
ENSEMBL[version].species['hs'].patch_version='p13'

version = '76'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['75'])
ENSEMBL[version].date='Aug 2014'
ENSEMBL[version].url='http://aug2014.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://aug2014.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p2'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p2'
ENSEMBL[version].species['mm'].external_id_prepend=''
ENSEMBL[version].species['mm'].genes_header='ensembl_gene_id\texternal_id\tchromosome_name\tstart_position\tend_position\tstrand\tdescription\texternal_gene_db\texternal_gene_symbol\tspecies_id'
ENSEMBL[version].species['mm'].genes_xml='''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "default" formatter = "CSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
    <Dataset name = "mmusculus_gene_ensembl" interface = "default" >
        <Attribute name = "ensembl_gene_id" />
        <Attribute name = "mgi_id" />
        <Attribute name = "chromosome_name" />
        <Attribute name = "start_position" />
        <Attribute name = "end_position" />
        <Attribute name = "strand" />
        <Attribute name = "description" />
        <Attribute name = "external_gene_source" />
        <Attribute name = "mgi_symbol" />
    </Dataset>
</Query>
'''
ENSEMBL[version].species['hs'].version='GRCh38'
ENSEMBL[version].species['hs'].major_version='GRCh38'
ENSEMBL[version].species['hs'].patch_version=''
ENSEMBL[version].species['hs'].external_id_prepend=''
ENSEMBL[version].species['hs'].genes_header='ensembl_gene_id\texternal_id\tchromosome_name\tstart_position\tend_position\tstrand\tdescription\texternal_gene_db\texternal_gene_symbol\tspecies_id'
ENSEMBL[version].species['hs'].genes_xml='''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "default" formatter = "CSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
    <Dataset name = "hsapiens_gene_ensembl" interface = "default" >
    <Attribute name = "ensembl_gene_id" />
    <Attribute name = "hgnc_id" />
    <Attribute name = "chromosome_name" />
    <Attribute name = "start_position" />
    <Attribute name = "end_position" />
    <Attribute name = "strand" />
    <Attribute name = "description" />
    <Attribute name = "external_gene_source" />
    <Attribute name = "hgnc_symbol" />
    </Dataset>
</Query>
'''

version = '77'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['76'])
ENSEMBL[version].date='Oct 2014'
ENSEMBL[version].url='http://oct2014.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://oct2014.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p2'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p2'
ENSEMBL[version].species['hs'].version='GRCh38'
ENSEMBL[version].species['hs'].major_version='GRCh38'
ENSEMBL[version].species['hs'].patch_version=''

version = '78'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['77'])
ENSEMBL[version].date='Dec 2014'
ENSEMBL[version].url='http://dec2014.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://dec2014.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p3'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p3'
ENSEMBL[version].species['hs'].version='GRCh38'
ENSEMBL[version].species['hs'].major_version='GRCh38'
ENSEMBL[version].species['hs'].patch_version=''

version = '79'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['78'])
ENSEMBL[version].date='Mar 2015'
ENSEMBL[version].url='http://mar2015.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://mar2015.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p3'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p3'
ENSEMBL[version].species['hs'].version='GRCh38.p2'
ENSEMBL[version].species['hs'].major_version='GRCh38'
ENSEMBL[version].species['hs'].patch_version='p2'

version = '80'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['79'])
ENSEMBL[version].date='May 2015'
ENSEMBL[version].url='http://may2015.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://may2015.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p3'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p3'
ENSEMBL[version].species['hs'].version='GRCh38.p2'
ENSEMBL[version].species['hs'].major_version='GRCh38'
ENSEMBL[version].species['hs'].patch_version='p2'

version = '81'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['80'])
ENSEMBL[version].date='Jul 2015'
ENSEMBL[version].url='http://jul2015.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://jul2015.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p4'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p4'
ENSEMBL[version].species['hs'].version='GRCh38.p3'
ENSEMBL[version].species['hs'].major_version='GRCh38'
ENSEMBL[version].species['hs'].patch_version='p3'

version = '82'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['81'])
ENSEMBL[version].date='Sep 2015'
ENSEMBL[version].url='http://sep2015.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://sep2015.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p4'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p4'
ENSEMBL[version].species['hs'].version='GRCh38.p3'
ENSEMBL[version].species['hs'].major_version='GRCh38'
ENSEMBL[version].species['hs'].patch_version='p3'

version = '83'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['82'])
ENSEMBL[version].date='Dec 2015'
ENSEMBL[version].url='http://dec2015.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://dec2015.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p4'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p4'
ENSEMBL[version].species['hs'].version='GRCh38.p5'
ENSEMBL[version].species['hs'].major_version='GRCh38'
ENSEMBL[version].species['hs'].patch_version='p5'

version = '84'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['83'])
ENSEMBL[version].date='Mar 2016'
ENSEMBL[version].url='http://mar2016.archive.ensembl.org'
ENSEMBL[version].url_biomart='http://mar2016.archive.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p4'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p4'
ENSEMBL[version].species['hs'].version='GRCh38.p5'
ENSEMBL[version].species['hs'].major_version='GRCh38'
ENSEMBL[version].species['hs'].patch_version='p5'

version = '85'
ENSEMBL[version]=copy.deepcopy(ENSEMBL['84'])
ENSEMBL[version].date='Jul 2016'
ENSEMBL[version].url='http://useast.ensembl.org'
ENSEMBL[version].url_biomart='http://useast.ensembl.org/biomart/martservice'
ENSEMBL[version].species['mm'].version='GRCm38.p4'
ENSEMBL[version].species['mm'].major_version='GRCm38'
ENSEMBL[version].species['mm'].patch_version='p4'
ENSEMBL[version].species['hs'].version='GRCh38.p5'
ENSEMBL[version].species['hs'].major_version='GRCh38'
ENSEMBL[version].species['hs'].patch_version='p5'

def print_ensembl_info():
    for version in sorted(map(int, (k for k in ENSEMBL.keys() if k != 'chromosomes'))):
        ensembl_info = ENSEMBL[str(version)]
        print('{}\t{}\t{}\t{}'.format(version, ensembl_info.date, ensembl_info.species['hs'].version, ensembl_info.species['mm'].version))

if __name__ == '__main__':
    print_ensembl_info()
