# -*- coding: utf-8 -*-
from __future__ import print_function
from future.utils import raise_with_traceback

import locale
#import logging
import os
import random
import shutil
import string
import sys
import tempfile
import time
import traceback

import file2db


from .ensembl import biomart_util as ensembl_biomart
from .ensembl import biomart_info as ensembl_biomart_info
from .mgi import itermine_util as mgi_intermine
from .hugo import hugo_util as hugo_util

from whoz import utils

LOG = utils.get_logger()


def get_sys_exec_root_or_drive():
    path = sys.executable
    while os.path.split(path)[1]:
        path = os.path.split(path)[0]
    return path


def delete_dir(dir):
    dir = os.path.abspath(dir)
    if os.path.exists(dir):
        root = get_sys_exec_root_or_drive()
        # bad error checking, but at least it's something
        if root == dir:
            raise_with_traceback(Exception("Will not delete directory: {}".format(dir)))
        try:
            shutil.rmtree(dir)
        except Exception as e:
            raise_with_traceback(Exception("Will not delete directory: {}".format(dir)))


def delete_file(filename):
    try:
        os.remove(filename)
    except:
        pass


def create_random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def file2db_data(input_file, delimiter, table_name, sql_file, output_dir):
    dialect = 'SQLITE'
    null_value = ''

    LOG.debug('Parsing: {}'.format(input_file))

    if not os.path.isfile(input_file):
        print("\nError: " + input_file + " is not a valid file.")
        exit(1)

    locale.setlocale(locale.LC_NUMERIC, "")

    try:
        output_file = "{0}.dat".format(os.path.abspath(os.path.join(output_dir, os.path.basename(input_file))))
        columns = file2db.parse_file(input_file, delimiter, output_file, null_value, False)

        if columns != None:
            table = [["INDEX", "COLUMN", "MAXVALUE", "MINVALUE", "MAXLEN", "MINLEN", "TYPE", "#VALS", "#EMPTY"]]

            for c in columns:
                simple_type = str(c.type).replace("<type '", "")
                simple_type = simple_type.replace("'>", "")
                table.append([str(c.index), str(c.name), str(c.max_value), str(c.min_value), str(c.max_length), str(c.min_length), simple_type.upper(), str(c.not_empty), str(c.empty)])

            sql_ddl = file2db.generate_ddl(dialect, table_name, columns)
            sql_import = file2db.generate_import(dialect, table_name, columns, output_file, delimiter)

            try:
                sql_file_fd = open(sql_file, "w")
                sql_file_fd.write(sql_ddl)
                sql_file_fd.write('\n')
                sql_file_fd.write(sql_import)
                sql_file_fd.close()
            except:
                print('Unable to generate SQL files!')
        else:
            print('Error parsing file!')

        #shutil.move(output_file, input_file)

    except Exception as e:
        print(str(e))


def execute_sql(database, sql_script):
    LOG = utils.get_logger()
    LOG.debug("cat {} | sqlite3 {}".format(sql_script, database))
    os.system("cat {} | sqlite3 {}".format(sql_script, database))


def execute(ensembl_version, database_file):
    try:
        final_db_abs_path = os.path.abspath(database_file)
        final_dir, final_db_file = os.path.split(final_db_abs_path)

        if os.path.exists(final_db_abs_path):
            LOG.info("{} exists, please delete first".format(final_db_abs_path))
            raise_with_traceback(Exception('File exists'))

        t = time.strftime("%Y-%m-%d.%H_%M_%S")
        prefix = ".{}_{}_".format(ensembl_version, t)
        #temp_dir = os.path.abspath(tempfile.mkdtemp(dir='.', prefix=prefix))
        temp_dir = '/Users/mvincent/work_new/for_prod/whoz/datawork'


        LOG.info('Using temporary directory: {}'.format(temp_dir))

        ensembl_genes = os.path.join(temp_dir, 'ensembl.genes.txt')
        ensembl_gtep = os.path.join(temp_dir, 'ensembl.gtep.txt')
        mgi_genes = os.path.join(temp_dir, 'mgi.genes.txt')
        mgi_synonyms = os.path.join(temp_dir, 'mgi.synonyms.txt')
        mgi_synonyms_oneline = os.path.join(temp_dir, 'mgi.synonyms.oneline.txt')
        mgi_ensemblids = os.path.join(temp_dir, 'mgi.ensemblids.txt')
        hugo_temp = os.path.join(temp_dir, 'hugo.temp.txt')
        hugo_genes = os.path.join(temp_dir, 'hugo.genes.txt')
        hugo_synonyms = os.path.join(temp_dir, 'hugo.synonyms.txt')

        #delete_file(ensembl_genes)
        #delete_file(ensembl_gtep)
        #delete_file(mgi_genes)
        #delete_file(mgi_synonyms)
        #delete_file(mgi_synonyms_oneline)
        #delete_file(mgi_ensemblids)
        #delete_file(hugo_genes)
        #delete_file(hugo_synonyms)

        LOG.info('Downloading data...')

        LOG.info('Extracting Ensembl data...')

        #ensembl_biomart.extract_genes(ensembl_version, 'Mm', ensembl_genes)
        #ensembl_biomart.extract_genes(ensembl_version, 'Hs', ensembl_genes, append=True)
        #ensembl_biomart.extract_gtep(ensembl_version, 'Mm', ensembl_gtep)
        #ensembl_biomart.extract_gtep(ensembl_version, 'Hs', ensembl_gtep, append=True)

        LOG.info('Extracting MGI data...')

        #mgi_intermine.extract_genes(mgi_genes)
        #mgi_intermine.extract_synonyms(mgi_synonyms)
        #mgi_intermine.extract_synonyms_one_line(mgi_synonyms_oneline)
        #mgi_intermine.extract_ensembl_ids(mgi_ensemblids)

        LOG.info('Extracting HUGO data...')

        #hugo_util.extract_data(hugo_temp, hugo_genes, hugo_synonyms)

        ensembl_genes_sql = os.path.join(temp_dir, 'ensembl.genes.sql')
        ensembl_gtep_sql = os.path.join(temp_dir, 'ensembl.gtep.sql')
        mgi_genes_sql = os.path.join(temp_dir, 'mgi.genes.sql')
        mgi_synonyms_sql = os.path.join(temp_dir, 'mgi.synonyms.sql')
        mgi_synonyms_oneline_sql = os.path.join(temp_dir, 'mgi.synonyms.oneline.sql')
        mgi_ensemblids_sql = os.path.join(temp_dir, 'mgi.ensemblids.sql')
        hugo_genes_sql = os.path.join(temp_dir, 'hugo.genes.sql')
        hugo_synonyms_sql = os.path.join(temp_dir, 'hugo.synonyms.sql')

        delete_file(ensembl_genes_sql)
        delete_file(ensembl_gtep_sql)
        delete_file(mgi_genes_sql)
        delete_file(mgi_synonyms_sql)
        delete_file(mgi_synonyms_oneline_sql)
        delete_file(mgi_ensemblids_sql)
        delete_file(hugo_genes_sql)
        delete_file(hugo_synonyms_sql)

        LOG.info('Parsing all files...')

        file2db_data(ensembl_genes, '\t', 'ensembl_genes_tmp', ensembl_genes_sql, temp_dir)
        file2db_data(ensembl_gtep, '\t', 'ensembl_gtep_tmp', ensembl_gtep_sql, temp_dir)
        file2db_data(mgi_genes, '\t', 'mgi_genes_tmp', mgi_genes_sql, temp_dir)
        file2db_data(mgi_synonyms, '\t', 'mgi_synonyms_tmp', mgi_synonyms_sql, temp_dir)
        file2db_data(mgi_synonyms_oneline, '\t', 'mgi_synonyms_oneline_tmp', mgi_synonyms_oneline_sql, temp_dir)
        file2db_data(mgi_ensemblids, '\t', 'mgi_ensemblids_tmp', mgi_ensemblids_sql, temp_dir)
        file2db_data(hugo_genes, '\t', 'hugo_genes_tmp', hugo_genes_sql, temp_dir)
        file2db_data(hugo_synonyms, '\t', 'hugo_synonyms_tmp', hugo_synonyms_sql, temp_dir)

        LOG.info('Loading data...')

        temp_db_file = os.path.join(temp_dir, final_db_file)

        execute_sql(temp_db_file, ensembl_genes_sql)
        execute_sql(temp_db_file, ensembl_gtep_sql)
        execute_sql(temp_db_file, mgi_genes_sql)
        execute_sql(temp_db_file, mgi_synonyms_sql)
        execute_sql(temp_db_file, mgi_synonyms_oneline_sql)
        execute_sql(temp_db_file, mgi_ensemblids_sql)
        execute_sql(temp_db_file, hugo_genes_sql)
        execute_sql(temp_db_file, hugo_synonyms_sql)

        LOG.info("Finalize database")

        sql_finalize_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sqlite.sql')

        execute_sql(temp_db_file, sql_finalize_file)

        # move into final spot
        LOG.debug("Moving {} to {}".format(temp_db_file, final_db_abs_path))
        shutil.move(temp_db_file, final_db_abs_path)

    except Exception as e:
        LOG.error("Error {}".format(e))
        try:
            if os.path.exists(final_db_abs_path):
                delete_dir(temp_dir)
            raise_with_traceback(e)
        except Exception as catastrophe:
            pass

    #if os.path.exists(final_db_abs_path):
    #    delete_dir(temp_dir)

