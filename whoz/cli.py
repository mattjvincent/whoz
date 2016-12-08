# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import time

import click
import json
from tabulate import tabulate

from whoz import utils
from whoz.create import create_database
from whoz.search import search_database
from whoz.www import application


def format_time(start, end):
    """
    Format length of time between start and end.

    :param start: the start time
    :param end: the end time
    :return: a formatted string of hours, minutes, and seconds
    """
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)


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
    utils.configure_logging(verbose)
    LOG = utils.get_logger()
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
    utils.configure_logging(verbose)
    LOG = utils.get_logger()
    LOG.info("Search database: {}".format(filename))
    LOG.debug("Term: {}".format(term))
    LOG.debug("Exact: {}".format(exact))
    LOG.debug("Format: {}".format(display))
    LOG.debug("Max: {}".format(max))
    LOG.debug("Species: {}".format(species))

    search_database.DATABASE = filename

    maximum = max if max >= 0 else None

    tstart = time.time()
    result, status = search_database.search(term, species, exact, False, maximum)
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

    #click.echo('serving db %s fires to %s,%s' % (ship, x, y))


@cli.command('id', short_help='get by id')
@click.argument('filename', metavar='<filename>', type=click.Path(exists=True, resolve_path=True, dir_okay=False))
@click.argument('ensembl_id', metavar='<ensembl_id>')
@click.option('-v', '--verbose', count=True)
def id(filename, ensembl_id, verbose):
    """
    Get gene information from annotation database <filename> for <term>
    """
    utils.configure_logging(verbose)
    LOG = utils.get_logger()
    LOG.info("Search database: {}".format(filename))
    LOG.debug("Ensembl ID: {}".format(ensembl_id))

    search_database.DATABASE = filename

    tstart = time.time()
    result, status = search_database.get_id(ensembl_id, verbose=verbose)
    tend = time.time()

    if status.error:
        print("Error occurred: {}".format(status.message))
        sys.exit(-1)

    print(json.dumps({'data': result}, indent=4))

    LOG.info("Search time: {}".format(format_time(tstart, tend)))


@cli.command('server', options_metavar='<options>', short_help='start the web server api')
@click.argument('config', metavar='<config>', type=click.Path(exists=True, resolve_path=True, dir_okay=False, writable=False))
@click.option('-v', '--verbose', count=True)
def server(config, verbose):
    """
    Start the web server using configuration specified in <config>.
    """
    utils.configure_logging(verbose)
    LOG = utils.get_logger()
    LOG.info("Starting www server, using configuration: {}".format(config))
    application.run(config)

if __name__ == '__main__':
    cli()

