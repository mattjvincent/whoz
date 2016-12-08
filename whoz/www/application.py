# -*- coding: utf-8 -*-

# TODO: The REST API's need to be implemented.

from __future__ import print_function

import json
import os
import sys
import time

from flask import Flask, render_template, request, Response, make_response, g, redirect, url_for
from flask_restful import reqparse, Resource, Api, fields, marshal_with, marshal_with_field
from flask_cors import CORS

from whoz.search import search_database
import whoz.utils as utils

LOG = utils.get_logger()

app = Flask(__name__)
CORS(app)
api = Api(app)


def support_jsonp(api_instance, callback_name_source='callback'):
    """Let API instance can respond jsonp request automatically.
    `callback_name_source` can be a string or a callback.
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

    def get(self, id):
        start = time.time()

        result, status = search_database.get_id(id)
        LOG.debug("Search time: {}".format(format_time(start, time.time())))

        if status.error:
            LOG.debug("Error occurred: {}".format(status.message))
            return


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


class Search(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(Search, self).__init__()

    @marshal_with(RETURN_FIELDS)
    def get(self):
        LOG.info("Call for: GET /search/")
        start = time.time()

        self.reqparse.add_argument('term', type=str, required=True, location='args')
        self.reqparse.add_argument('species', type=str, required=False, location='args')
        self.reqparse.add_argument('exact', type=str, required=False, location='args')
        self.reqparse.add_argument('limit', type=int, required=False, location='args')
        self.reqparse.add_argument('callback', type=str, required=False, location='args')
        #self.reqparse.add_argument('start', type=str, required=False, location='args')

        data = self.reqparse.parse_args()

        result, status = search_database.search(term=data['term'],
                                                species_id=data.get('species', None),
                                                exact=str2bool(data.get('exact', '0')),
                                                limit=data.get('limit', 1000000),
                                                verbose=True)

        LOG.info("Search time: {}".format(format_time(start, time.time())))

        if status.error:
            LOG.error("Error occurred: {}".format(status.message))
            return

        if len(result.matches) == 0:
            LOG.info("No results found")
            return {'request': data, 'result': result}

        return {'request': data, 'result': result}


@app.route("/js/whoz_api.js")
def whoz_api_js():
    return render_template('whoz_api.js'), 200, {'Content-Type': 'application/javascript'}


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


def run(settings=None):
    settings_dir = os.path.dirname(settings)
    app.config.from_pyfile(settings)

    host = app.config['HOST'] if 'HOST' in app.config else '0.0.0.0'
    port = app.config['PORT'] if 'PORT' in app.config else 80
    threaded = app.config['THREADED'] if 'THREADED' in app.config else True
    debug = app.config['DEBUG'] if 'DEBUG' in app.config else True

    # let's attempt to make sure all files are where they are supposed to be
    if 'WHOZ_DB' not in app.config:
        LOG.error('WHOZ_DB not configured in: {}'.format(settings_dir))
        sys.exit()

    whoz_db = app.config['WHOZ_DB']
    if not os.path.isabs(whoz_db):
        LOG.debug('WHOZ DB specified as relative path: {}'.format(whoz_db))
        whoz_db = os.path.abspath(os.path.join(settings_dir, whoz_db))
    else:
        LOG.debug('WHOZ DB specified as absolute path: {}'.format(whoz_db))
        whoz_db = os.path.abspath(whoz_db)


    if not os.path.exists(whoz_db):
        LOG.error('Specified WHOZ_DB does not exist: {}'.format(whoz_db))
        sys.exit()

    LOG.info('Database: {}'.format(whoz_db))

    LOG.debug('host={}'.format(host))
    LOG.debug('port={}'.format(port))
    LOG.debug('threaded={}'.format(threaded))
    LOG.debug('debug={}'.format(debug))
    LOG.debug('settings directory={}'.format(settings_dir))
    LOG.debug('database={}'.format(whoz_db))

    search_database.DATABASE = whoz_db

    api.add_resource(ID, '/id/<id>', '/id/<id>/')
    api.add_resource(Search, '/search')

    app.run(host=host, port=port, threaded=threaded, debug=debug)




