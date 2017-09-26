# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import time

import click
import json
from tabulate import tabulate

from whoz.utils import configure_logging, format_time, get_logger
from whoz.create import create_database
from whoz.search import search_database, batch_database
from whoz.www import application

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
def cli():
    """
    WHOZ

    Simple tools for Ensembl annotations.

    """


@cli.command('create', options_metavar='<options>', short_help='create an annotation database')
@click.argument('filename', metavar='<filename>', type=click.Path(resolve_path=True, dir_okay=False, writable=True))
@click.argument('version', metavar='<version>')
@click.option('-v', '--verbose', count=True)
def create(filename, version, verbose):
    """
    Creates a new annotation database <filename> using Ensembl <version>.
    """
    configure_logging(verbose)
    LOG = get_logger()
    LOG.info("Creating database: {}".format(filename))
    LOG.info("Using Ensembl version: {}".format(version))

    tstart = time.time()
    create_database.execute(version, filename)
    tend = time.time()

    LOG.info("Creation time: {}".format(format_time(tstart, tend)))


@cli.command('search', short_help='search for data')
@click.argument('filename', metavar='<filename>', type=click.Path(exists=True, resolve_path=True, dir_okay=False))
@click.argument('term', metavar='<term>')
@click.option('-e', '--exact', is_flag=True)
@click.option('-f', '--format', 'display', default='pretty', type=click.Choice(['tab', 'csv', 'json', 'pretty']))
@click.option('-m', '--max', default=-1)
@click.option('-s', '--species', type=click.Choice(['mm', 'hs']))
@click.option('-v', '--verbose', count=True)
def search(filename, term, exact, display, max, species, verbose):
    """
    Search annotation database <filename> for <term>
    """
    configure_logging(verbose)
    LOG = get_logger()
    LOG.info("Search database: {}".format(filename))
    LOG.debug("Term: {}".format(term))
    LOG.debug("Exact: {}".format(exact))
    LOG.debug("Format: {}".format(display))
    LOG.debug("Max: {}".format(max))
    LOG.debug("Species: {}".format(species))

    search_database.DATABASE = filename

    maximum = max if max >= 0 else None

    tstart = time.time()
    result, status = search_database.search(filename, term, species, exact, False, maximum)
    tend = time.time()

    LOG.debug("Num Results: {}".format(result.num_results))
    count = 0

    if status.error:
        print("Error occurred: {}".format(status.message))
        sys.exit(-1)

    if len(result.matches) == 0:
        print("No results found")
        sys.exit()

    headers = ["ID", "SYMBOL", "POSITION", "MATCH_REASON", "MATCH_VALUE"]

    if display in ('tab', 'csv'):
        delim = '\t' if display == 'tab' else ','
        print(delim.join(headers))
        for match in result.matches:
            line = list()
            line.append(match.ensembl_gene_id)
            line.append(match.symbol)
            line.append("{}:{}-{}".format(match.chromosome, match.position_start, match.position_end))
            line.append(match.match_reason)
            line.append(match.match_value)
            print(delim.join(map(str, line)))
            count += 1
            if count >= max > 0:
                break
    elif display == 'json':
        tbl = []
        for match in result.matches:
            line = list()
            line.append(match.ensembl_gene_id)
            line.append(match.symbol if match.symbol else '')
            line.append("{}:{}-{}".format(match.chromosome, match.position_start, match.position_end))
            line.append(match.match_reason)
            line.append(match.match_value)
            tbl.append(dict(zip(headers, line)))
            count += 1
            if count >= max > 0:
                break
        print(json.dumps({'data': tbl}, indent=4))
    else:
        tbl = []
        for match in result.matches:
            line = list()
            line.append(match.ensembl_gene_id)
            line.append(match.symbol)
            line.append("{}:{}-{}".format(match.chromosome, match.position_start, match.position_end))
            line.append(match.match_reason)
            line.append(match.match_value)
            tbl.append(line)
            count += 1
            if count >= max > 0:
                break
        print(tabulate(tbl, headers))

    LOG.info("Search time: {}".format(format_time(tstart, tend)))


@cli.command('id', short_help='get by id')
@click.argument('filename', metavar='<filename>', type=click.Path(exists=True, resolve_path=True, dir_okay=False))
@click.argument('ensembl_id', metavar='<ensembl_id>')
@click.option('-f', '--format', 'display', default='pretty', type=click.Choice(['tab', 'csv', 'json', 'pretty']))
@click.option('-v', '--verbose', count=True)
def id(filename, ensembl_id, display, verbose):
    """
    Get gene information from annotation database <filename> for <term>
    """
    configure_logging(verbose)
    LOG = get_logger()
    LOG.info("Search database: {}".format(filename))
    LOG.debug("Ensembl ID: {}".format(ensembl_id))

    tstart = time.time()
    result, status = batch_database.get_id(filename, ensembl_id, verbose=verbose)
    tend = time.time()

    if status.error:
        print("Error occurred: {}".format(status.message))
        sys.exit(-1)

    headers = ["ID", "SYMBOL", "NAME", "POSITION", "STRAND", "DESCRIPTION", "SYNONYMS"]

    gene = result[0]

    if display in ('tab', 'csv'):
        delim = '\t' if display == 'tab' else ','
        print(delim.join(headers))
        line = list()
        line.append(gene['id'])
        line.append(gene['symbol'] if gene['symbol'] else '')
        line.append(gene['name'] if gene['name'] else '')
        line.append("{}:{}-{}".format(gene['chromosome'], gene['start'], gene['end']))
        line.append(gene['strand'] if gene['strand'] else '')
        line.append(gene['description'] if gene['description'] else '')
        line.append(gene['synonyms'] if gene['synonyms'] else '')
        print(delim.join(map(str, line)))
    elif display == 'json':
        tbl = []
        line = list()
        line.append(gene['id'])
        line.append(gene['symbol'] if gene['symbol'] else '')
        line.append(gene['name'] if gene['name'] else '')
        line.append("{}:{}-{}".format(gene['chromosome'], gene['start'], gene['end']))
        line.append(gene['strand'] if gene['strand'] else '')
        line.append(gene['description'] if gene['description'] else '')
        line.append(gene['synonyms'] if gene['synonyms'] else '')
        tbl.append(dict(zip(headers, line)))
        print(json.dumps({'data': tbl}, indent=4))
    else:
        tbl = []
        line = list()
        line.append(gene['id'])
        line.append(gene['symbol'] if gene['symbol'] else '')
        line.append(gene['name'] if gene['name'] else '')
        line.append("{}:{}-{}".format(gene['chromosome'], gene['start'], gene['end']))
        line.append(gene['strand'] if gene['strand'] else '')
        line.append(gene['description'] if gene['description'] else '')
        line.append(gene['synonyms'] if gene['synonyms'] else '')
        tbl.append(line)
        print(tabulate(tbl, headers))



    LOG.info("Search time: {}".format(format_time(tstart, tend)))


@cli.command('genes', short_help='get all genes')
@click.argument('filename', metavar='<filename>', type=click.Path(exists=True, resolve_path=True, dir_okay=False))
@click.option('-s', '--species', type=click.Choice(['mm', 'hs']))
@click.option('-v', '--verbose', count=True)
def genes(filename, species, verbose):
    """
    Get gene information from annotation database <filename> for <term>
    """
    configure_logging(verbose)
    LOG = get_logger()
    LOG.info("Search database: {}".format(filename))
    LOG.debug("Species: {}".format(species))

    tstart = time.time()
    result, status = batch_database.get_genes(filename, species, verbose=verbose)
    tend = time.time()

    if status.error:
        print("Error occurred: {}".format(status.message))
        sys.exit(-1)

    for r in result:
        print(r)


    LOG.info("Search time: {}".format(format_time(tstart, tend)))


@cli.command('server', options_metavar='<options>', short_help='start the web server api')
@click.argument('config', metavar='<config>', type=click.Path(exists=True, resolve_path=True, dir_okay=False, writable=False))
@click.option('-v', '--verbose', count=True)
def server(config, verbose):
    """
    Start the web server using configuration specified in <config>.
    """
    configure_logging(verbose)
    LOG = get_logger()
    LOG.info("Starting www server, using configuration: {}".format(config))
    application.run(config)


if __name__ == '__main__':
    cli()
