import csv
#import logging
import sys

from .biomart_info import ENSEMBL

import whoz.utils as utils
LOG = utils.get_logger()

#LOG = logging.getLogger('simple_annotations')

import requests

def extract_genes(ensembl_version, species_id, filename, append=False):
    if ensembl_version not in ENSEMBL:
        raise ValueError("Ensembl Version {} is not configured".format(ensembl_version))

    ensembl_data = ENSEMBL[ensembl_version]

    if species_id.lower() not in ensembl_data.species:
        raise ValueError("Species '{}' is not configured for Ensembl Version {}".format(species_id, ensembl_version))

    rwa = 'a' # if append else 'w'
    fd = sys.stdout if not filename else open(filename, rwa)

    url = ensembl_data.url_biomart
    xml = ensembl_data.species[species_id.lower()].genes_xml
    values = {'query': xml.strip()}

    LOG.debug("Downloading Ensembl gene data from: {}".format(url))

    response = requests.get(url, values)

    external_id_prepend = ensembl_data.species[species_id.lower()].external_id_prepend
    external_id_column = ensembl_data.species[species_id.lower()].external_id_column

    species = species_id[0].upper() + species_id[1].lower()

    if not append:
        fd.write(ensembl_data.species[species_id.lower()].genes_header)
        fd.write('\n')

    LOG.debug("Parsing Ensembl gene data...")

    text = response.content.decode('utf-8')
    cr = csv.reader(text.splitlines())
    count = 0

    for row in cr:
        count += 1
        if count % 10000 == 0:
            LOG.debug("{} lines parsed".format(count))

        if external_id_prepend and row[external_id_column]:
            row[external_id_column] = "{}{}".format(external_id_prepend, row[external_id_column])
        row.append(species)

        fd.write('\t'.join(row))
        fd.write('\n')

    fd.close()


def extract_gtep(ensembl_version, species_id, filename=None, append=False):
    if ensembl_version not in ENSEMBL:
        raise ValueError("Ensembl Version {} is not configured".format(ensembl_version))

    ensembl_data = ENSEMBL[ensembl_version]

    if species_id.lower() not in ensembl_data.species:
        raise ValueError("Species '{}' is not configured for Ensembl Version {}".format(species_id, ensembl_version))

    rwa = 'a' #if append else 'w'
    fd = sys.stdout if not filename else open(filename, rwa)

    url = ensembl_data.url_biomart

    if not append:
        fd.write(ensembl_data.species[species_id.lower()].gte_header)
        fd.write('\n')

    if ensembl_data.species[species_id.lower()].gte_by_chrom:
        for i, chrom in enumerate(ENSEMBL['chromosomes']):

            LOG.debug("Downloading Ensembl gtep data for chromosome {} from: {}".format(chrom, url))

            xml = ensembl_data.species[species_id.lower()].gte_xml
            xml = xml.replace('{{CHROMOSOME}}', chrom)
            LOG.debug(xml)
            values = {'query': xml.strip()}

            response = requests.get(url, values)

            species = species_id[0].upper() + species_id[1].lower()

            LOG.debug("Parsing Ensembl gtep data...")

            text = response.content.decode('utf-8')
            cr = csv.reader(text.splitlines())

            count = 0

            for row in cr:
                count += 1
                if count % 10000 == 0:
                    LOG.debug("{} lines parsed".format(count))

                row.append(species)
                fd.write('\t'.join(row))
                fd.write('\n')
    else:
        LOG.debug("Downloading Ensembl gtep data from: {}".format(url))

        xml = ensembl_data.species[species_id.lower()].gte_xml
        values = {'query': xml.strip()}

        response = requests.get(url, values)

        species = species_id[0].upper() + species_id[1].lower()

        if not append:
            fd.write(ensembl_data.species[species_id.lower()].gte_header)
            fd.write('\n')

        LOG.debug("Parsing Ensembl gtep data...")

        text = response.content.decode('utf-8')
        cr = csv.reader(text)
        count = 0

        for row in cr:
            count += 1
            if count % 10000 == 0:
                LOG.debug("{} lines parsed".format(count))

            row.append(species)
            fd.write('\t'.join(row))
            fd.write('\n')

