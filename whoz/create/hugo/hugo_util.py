from builtins import int
from past.builtins import long

#import logging
import os
import shutil
import time

import requests

import whoz.utils as utils

LOG = utils.get_logger()

def _fix(val):
    if val is None:
        return ''

    if isinstance(val, (float, long, int)):
        return str(val)

    if isinstance(val, bytes):
        return bytes.decode(val).strip()

    return str(val).strip()


def extract_data(filename_temp, filename_genes, filename_synonyms):
    url = "http://www.genenames.org/cgi-bin/download?col=gd_hgnc_id&col=gd_app_sym&col=gd_app_name&col=gd_status&col=gd_aliases&col=gd_pub_ensembl_id&status=Approved&status_opt=2&chr=1&chr=2&chr=3&chr=4&chr=5&chr=6&chr=7&chr=8&chr=9&chr=10&chr=11&chr=12&chr=13&chr=14&chr=15&chr=16&chr=17&chr=18&chr=19&chr=20&chr=21&chr=22&chr=X&chr=Y&where=&order_by=gd_hgnc_id&format=text&limit=&hgnc_dbtag=on&submit=submit"
    #HGNC ID Approved Symbol Approved Name   Status  Synonyms        Ensembl Gene ID

    LOG.debug("Downloading HUGO data...")

    response = requests.get(url, stream=True)

    with open(filename_temp, 'wb') as out_file:
        out_file.write(response.content)

    fd_data = open(filename_genes, 'w')
    fd_synonyms = open(filename_synonyms, 'w')

    fd_data.write('ensembl_gene_id\tspecies_id\tgene_symbol\tgene_name\tsynonyms\thugo_id\n')
    fd_synonyms.write('ensembl_gene_id\tsynonym_type\tsynonym\n')

    first = True
    with open(filename_temp) as f:
        count = 0

        for line in f:
            count += 1
            if count % 10000 == 0:
                LOG.debug("{} lines parsed".format(count))

            if first:
                first = False
                continue
            line_elems = line.strip().split('\t')
            if line_elems and len(line_elems) > 5:
                # have ensembl id
                #fd_ids.write('"' + _fix(line_elems[5]) + '"\t"' + _fix(line_elems[0]) + '"\n')

                elems = []
                elems.append('"' + _fix(line_elems[5]) + '"')
                elems.append('"Hs"')
                elems.append('"' + _fix(line_elems[1]) + '"')
                elems.append('"' + _fix(line_elems[2]) + '"')
                elems.append('"' + _fix(line_elems[4]) + '"')
                elems.append('"' + _fix(line_elems[0]) + '"')
                fd_data.write('\t'.join(elems) + '\n')

                fd_synonyms.write('"' + _fix(line_elems[5]) + '"\t')
                fd_synonyms.write('"' + _fix(line_elems[1]) + '"\t')
                fd_synonyms.write('"P"\n')

                if len(line_elems[4]) > 1:
                    synonyms = line_elems[4].split(',')
                    for s in synonyms:
                        fd_synonyms.write('"' + _fix(line_elems[5]) + '"\t')
                        fd_synonyms.write('"' + _fix(s.strip()) + '"\t')
                        fd_synonyms.write('"Y"\n')

    fd_data.close()
    fd_synonyms.close()
    os.remove(filename_temp)

if __name__ == '__main__':
    extract_data()



