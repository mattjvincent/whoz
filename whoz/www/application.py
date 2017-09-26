# -*- coding: utf-8 -*-

# TODO: The REST API's need to be implemented.

from __future__ import print_function


from collections import OrderedDict
import glob
import os
import sys
import time


from flask import Flask, render_template, request, Response, make_response, g, redirect, url_for, jsonify
from flask_restful import reqparse, Resource, Api, fields, marshal_with, marshal_with_field, abort
from flask_cors import CORS

from whoz.search import search_database
from whoz.search import batch_database
import whoz.utils as utils

LOG = utils.get_logger()

app = Flask(__name__)
CORS(app)
api = Api(app)
"""
Get a list of all files in ``directory``.

:param str directory: a directory
:param list file_extensions: a list of file extensions to match, None means all

:return: a list of all files
"""

def support_jsonp(api_instance, callback_name_source='callback'):
    """Let API instance respond to jsonp requesta automatically.

    :param str callback_name_source: can be a string or a callback
        If it is a string, the system will find the argument that named by this string in `query string`.
         If found, determine this request to be a jsonp request, and use the argument's value as the js callback name.
        If `callback_name_source` is a callback, this callback should return js callback name when request
         is a jsonp request, and return False when request is not jsonp request.
         And system will handle request according to its return value.
    default support format：url?callback=js_callback_name
    """
    output_json = api_instance.representations['application/json']

    @api_instance.representation('application/json')
    def handle_jsonp(data, code, headers=None):
        resp = output_json(data, code, headers)

        if code == 200:
            callback = request.args.get(callback_name_source, False) if not callable(callback_name_source) else callback_name_source()
            if callback:
                resp.set_data(str(callback) + '(' + resp.get_data().decode("utf-8") + ')')

        return resp

support_jsonp(api)

app.config['BUNDLE_ERRORS'] = True

class Config:
    pass

CONF = Config()

MATCH_FIELDS = {
    'ensembl_gene_id': fields.Raw,
    'external_id': fields.String,
    'species_id': fields.String,
    'symbol': fields.String,
    'name': fields.String,
    'description': fields.String,
    'synonyms': fields.List(fields.String),
    'chromosome': fields.String,
    'position_start': fields.Integer,
    'position_end': fields.Integer,
    'strand': fields.String,
    'match_reason': fields.String,
    'match_value': fields.String
}

RESULT_FIELDS = {
    'num_results': fields.Integer,
    'num_matches': fields.Integer,
    'matches': fields.List(fields.Nested(MATCH_FIELDS))
}

REQUEST_FIELDS = {
    'term': fields.String,
    'species': fields.String,
    'exact': fields.Boolean,
    'limit': fields.Integer,
    'callback': fields.String
}

RETURN_FIELDS = {
    'request': fields.Nested(REQUEST_FIELDS),
    'result': fields.Nested(RESULT_FIELDS)
}


def get_all_whoz_dbs(dir):
    file_str = os.path.join(dir, 'whoz.*.db3')
    dbs = glob.glob(file_str)

    db_vers = []
    db_temp = {}

    # get the versions
    for db in dbs:
        version = int(db.split(".")[-2])
        db_vers.append(version)
        db_temp[version] = db

    db_vers.sort()

    all_sorted_dbs = OrderedDict()

    default = None
    for version in db_vers:
        all_sorted_dbs[version] = db_temp[version]
        default = db_temp[version]

    return default, all_sorted_dbs


def get_whoz_db(version=None):
    try:
        if version:
            return CONF.ALL_WHOZ_DB[int(version)]

        return CONF.DEFAULT_WHOZ_DB
    except:
        return None


def str2bool(val):
    return str(val).lower() in ['true', '1', 't', 'y', 'yes']


@app.before_request
def before_request():
    g.URL_BASE = request.url_root

    if 'HTTP_X_FORWARDED_PATH' in request.environ:
        if 'wsgi.url_scheme' in request.environ:
            protocol = request.environ['wsgi.url_scheme'] + ':'
        g.URL_BASE = "{}//{}{}".format(protocol, request.environ['HTTP_X_FORWARDED_HOST'], request.environ['HTTP_X_FORWARDED_PATH'])

    if g.URL_BASE[-1] == '/':
        g.URL_BASE = g.URL_BASE[:-1]


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


# Genes
# Transcripts
# Exons
# Proteins
# Search

class ID(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(ID, self).__init__()

    def get(self, id, version=None):
        start = time.time()

        db = get_whoz_db(version)

        if not db:
            abort(500, message='Version {} not supported'.format(version))

        result, status = batch_database.get_id(db, id)
        LOG.debug("Search time: {}".format(format_time(start, time.time())))

        if status.error:
            LOG.debug("Error occurred: {}".format(status.message))
            abort(500, message=status.message)

        return result

    def put(self, gene_id):
        LOG.error("Call for: PUT /id/%s [NOT YET IMPLEMENTED]" % gene_id)
        content = {'please move along': 'nothing to see here'}
        return content, 501

    def delete(self, gene_id):
        LOG.error("Call for: DELETE /id/%s [NOT YET IMPLEMENTED]" % gene_id)
        content = {'please move along': 'nothing to see here'}
        return content, 501

    def post(self):
        LOG.error("Call for: POST /id")
        content = {'please move along': 'nothing to see here'}
        return content, 501


class Genes(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(Genes, self).__init__()

    def get(self, species_id=None, version=None):
        start = time.time()

        db = get_whoz_db(version)

        if not db:
            abort(500, message='Version {} not supported'.format(version))

        result, status = batch_database.get_genes(db, species_id, True)
        LOG.debug("Search time: {}".format(format_time(start, time.time())))

        if status.error:
            LOG.debug("Error occurred: {}".format(status.message))
            abort(500, message=status.message)

        return result


class Search(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(Search, self).__init__()

    @marshal_with(RETURN_FIELDS)
    def get(self, version=None):
        LOG.info("Call for: GET /search/")
        start = time.time()

        self.reqparse.add_argument('term', type=str, required=True, location='args')
        self.reqparse.add_argument('species', type=str, required=False, location='args')
        self.reqparse.add_argument('exact', type=str, required=False, location='args')
        self.reqparse.add_argument('limit', type=int, required=False, location='args')
        self.reqparse.add_argument('callback', type=str, required=False, location='args')

        data = self.reqparse.parse_args()

        db = get_whoz_db(version)

        if not db:
            abort(500, message='Version {} not supported. Try calling /versions'.format(version))

        result, status = search_database.search(database=db,
                                                term=data['term'],
                                                species_id=data.get('species', None),
                                                exact=str2bool(data.get('exact', '0')),
                                                limit=data.get('limit', 1000000),
                                                verbose=True)

        LOG.info("Search time: {}".format(format_time(start, time.time())))

        if len(result.matches) == 0:
            LOG.info("No results found")
            return {'request': data, 'result': result}

        return {'request': data, 'result': result}


@app.route("/js/whoz_api.js")
def whoz_api_js():
    return render_template('whoz_api.js'), 200, {'Content-Type': 'application/javascript'}


@app.route("/versions")
def versions():
    versions = [k for k, v in CONF.ALL_WHOZ_DB.items()]
    return jsonify({'versions': versions})


@app.route("/")
def index():
    # POST search_term = request.form.get("search_term")
    # GET  search_term = request.args.get("search_term")
    # BOTH search_term = request.values.get("search_term")
    #print request.path
    #print request.full_path
    #print request.script_root
    #print request.url
    #print request.base_url
    #print request.url_root

    return redirect(url_for('search'))


def run(settings):
    app.config.from_pyfile(settings)

    host = app.config['HOST'] if 'HOST' in app.config else '0.0.0.0'
    port = app.config['PORT'] if 'PORT' in app.config else 80
    threaded = app.config['THREADED'] if 'THREADED' in app.config else True
    debug = app.config['DEBUG'] if 'DEBUG' in app.config else True

    if 'WHOZ_DIR' not in app.config:
        LOG.error('WHOZ_DIR not configured')
        sys.exit()

    whoz_dir = app.config['WHOZ_DIR']

    if not os.path.isabs(whoz_dir):
        LOG.debug('WHOZ DIR specified as relative path: {}'.format(whoz_dir))
        whoz_dir = os.path.abspath(os.path.join(os.getcwd(), whoz_dir))
    else:
        LOG.debug('WHOZ DIR specified as absolute path: {}'.format(whoz_dir))
        whoz_dir = os.path.abspath(whoz_dir)

    if not os.path.exists(whoz_dir):
        LOG.error('Specified WHOZ_DIR does not exist: {}'.format(whoz_dir))
        sys.exit()

    if not os.path.isdir(whoz_dir):
        LOG.error('Specified WHOZ_DIR is not a directory: {}'.format(whoz_dir))
        sys.exit()

    CONF.DEFAULT_WHOZ_DB, CONF.ALL_WHOZ_DB = get_all_whoz_dbs(whoz_dir)

    LOG.debug("All databases...")
    for ver, db in CONF.ALL_WHOZ_DB.items():
        LOG.debug('{}: {}'.format(ver, db))
    LOG.debug('Default database: {}'.format(get_whoz_db()))
    LOG.debug('host={}'.format(host))
    LOG.debug('port={}'.format(port))
    LOG.debug('threaded={}'.format(threaded))
    LOG.debug('debug={}'.format(debug))
    LOG.debug('whoz_dir={}'.format(whoz_dir))

    api.add_resource(ID, '/<version>/gene/<id>', '/<version>/gene/<id>/' )
    api.add_resource(Genes, '/<version>/genes', '/<version>/genes' )
    api.add_resource(Search, '/<version>/search', '/search')

    app.run(host=host, port=port, threaded=threaded, debug=debug)




