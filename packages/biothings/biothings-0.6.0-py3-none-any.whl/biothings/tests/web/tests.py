'''
Nose tests
run as "nosetests tests"
    or "nosetests tests:test_main"
'''
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import quote_plus
import json
import os
import re
import sys
import unittest
from functools import wraps

import requests

from biothings.tests import BiothingsTestCase
from biothings.tests.web.settings import BiothingTestSettings
from biothings.tests.web.helper import parameterized, parameters

try:
    import msgpack
except ImportError:
    sys.stderr.write("Warning: msgpack is not available.")

bts = BiothingTestSettings(config_module='tests.test_config')

_d = json.loads    # shorthand for json decode
_e = json.dumps    # shorthand for json encode
_q = quote_plus     # shorthand for url encoding

try:
    jsonld_context = requests.get(bts.JSONLD_CONTEXT_URL).json()
except BaseException:
    sys.stderr.write("Couldn't load JSON-LD context.\n")
    jsonld_context = {}

PATTR = '%values'


@parameterized
class BiothingGenericTests(BiothingsTestCase):
    __test__ = False  # don't run nosetests on this class directly

    # Make these class variables so that tornadorequesthelper plays nice.
    host = os.getenv(bts.HOST_ENVAR_NAME, '')
    if not host:
        host = bts.NOSETEST_DEFAULT_URL
    host = host.rstrip('/')
    api = '/' + bts.API_VERSION

    # Setup/tear down class for unittest
    @classmethod
    def setUpClass(cls):
        # get host and urls, etc
        sys.stderr.write("Running tests on {}\n".format(cls.host))
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    # setup tear down test for unittest
    def setUp(self):
        pass

    def tearDown(self):
        pass

    #############################################################
    # Test functions                                            #
    #############################################################

    def test_main(self):
        self.request(self.host)

    #############################################################
    # Annotation endpoint GET tests                             #
    #############################################################

    def test_annotation_object(self):
        ''' Test that annotation object contains expected fields. '''
        url = bts.ANNOTATION_ENDPOINT + '/' + bts.ANNOTATION_OBJECT_ID
        res = self.request(url).json()
        for attr in bts.ANNOTATION_OBJECT_EXPECTED_ATTRIBUTE_LIST:
            self.assertIn(
                attr, res, 'Expected field "{}" in returned object of query: {}'.format(
                    attr, url))

    def test_annotation_GET_empty(self):
        ''' Test that the annotation GET endpoint handles empty inputs correctly. '''
        self.request('' + bts.ANNOTATION_ENDPOINT, expect_status=404)
        self.request('' + bts.ANNOTATION_ENDPOINT + '/', expect_status=404)

    def test_annotation_GET_unicode(self):
        ''' Test that the annotation GET endpoint handles unicode string inputs correctly. '''
        self.request(
            ''
            + bts.ANNOTATION_ENDPOINT
            + '/'
            + bts.UNICODE_TEST_STRING,
            expect_status=404)

    @parameters(bts.ANNOTATION_GET_FIELDS)
    def test_annotation_GET_fields(self, bid):
        ''' Test that the fields parameter on the annotation GET endpoint works as expected. '''
        url = bts.ANNOTATION_ENDPOINT + '/' + bid
        # Test setup correctly?
        self.assertRegexpMatches(
            bid, r'fields=.+',
            'Test setup error, "fields" parameter not specified or empty in url: {}'.format(url))
        # get the url with all fields
        total_url = bts.ANNOTATION_ENDPOINT + '/' + _q(bid.split('?')[0])
        # get the user specified fields
        true_fields = [x.strip() for x in self.parse_url(url, 'fields').split(',')]
        # get the original and total request (with specified fields, and all fields, respectively)
        res = self.request(url).json()
        res_total = self.request(total_url).json()
        # check the fields
        self.check_fields(res, res_total, true_fields,
                          bts.CHECK_FIELDS_SUBSET_ADDITIONAL_FIELDS)

    @parameters(bts.ANNOTATION_GET_FILTER)
    def test_annotation_GET_filter(self, bid):
        ''' Test that the filter parameter on the annotation GET endpoint works as expected. '''
        url = bts.ANNOTATION_ENDPOINT + '/' + bid
        # Test setup correctly?
        self.assertRegexpMatches(
            bid, r'filter=.+',
            'Test setup error, "filter" parameter not specified or empty in url: {}'.format(url))
        # get the url with all fields
        total_url = bts.ANNOTATION_ENDPOINT + '/' + _q(bid.split('?')[0])
        # get the user specified fields
        true_filter = [x.strip() for x in self.parse_url(url, 'filter').split(',')]
        # get the original and total request (with specified fields, and all fields, respectively)
        res = self.request(url).json()
        res_total = self.request(total_url).json()
        # check the fields
        self.check_fields(res, res_total, true_filter,
                          bts.CHECK_FIELDS_SUBSET_ADDITIONAL_FIELDS)

    @parameters(bts.ANNOTATION_GET_JSONLD)
    def test_annotation_GET_jsonld(self, bid):
        ''' Test that the annotation GET endpoint correctly returns the JSON-LD context information. '''
        url = bts.ANNOTATION_ENDPOINT + '/' + bid
        self.assertRegexpMatches(
            bid, r'jsonld=((1)|([Tt][Rr][Uu][Ee]))',
            'Test setup error, "jsonld" parameter not specified or false in url: {}'.format(url))
        res = self.request(url).json()
        self.check_jsonld(res, jsonld_context)

    @parameters(bts.ANNOTATION_GET_MSGPACK)
    def test_annotation_GET_msgpack(self, bid):
        ''' Test that the annotation GET endpoint correctly returns msgpack format. '''
        url = bts.ANNOTATION_ENDPOINT + '/' + bid
        # Test must be set up correctly
        self.assertRegexpMatches(
            bid, r'msgpack=((1)|([Tt][Rr][Uu][Ee]))',
            'Test setup error, "msgpack" parameter not specified or false in url: {}\n'.format(url))
        # Get object without msgpack
        total_url = re.sub(r'[?&]msgpack=((1)|([Tt][Rr][Uu][Ee]))', '', url)
        # get the total and msgpack results
        res_t = self.request(total_url).json()
        res_msgpack = self.convert_msgpack(self.msgpack_ok(self.request(url).content))
        # remove took from both (should be different)
        res_t.pop('took', None)
        res_msgpack.pop('took', None)
        self.assertDictEqual(
            res_t,
            res_msgpack,
            "msgpacked results and non-msgpacked results differ for query: {}".format(url))
    """
    def test_annotation_GET(self):
        ''' Function to test GETs to the annotation endpoint.

            Currently supports automatic testing of:
                fields
                filter
                jsonld
                callback
        '''
        # Check some ids to make sure the resulting _id matches

        for (test_number, bid) in enumerate(ns.annotation_GET):
            base_url = ns.annotation_endpoint + '/' + bid
            get_url = ns.annotation_endpoint + '/' + _q(bid.split('?')[0]) + '?' + '?'.join(bid.split('?')[1:])
            # if it specifies a callback function, make sure it works
            if self.parse_url(base_url, 'callback'):
                res = self.extract_results_from_callback(get_url)
            else:
                res = self.request(get_url).json()
            # Check that the returned ID matches
            eq_(res['_id'], bid.split('?')[0])
            # Is this a jsonld query?
            if self.check_boolean_url_option(base_url, 'jsonld') and 'root' in jsonld_context:
                self.check_jsonld(res, '', jsonld_context)
            if 'fields' in bid or 'filter' in bid:
                # This is a filter query, test it appropriately.  First get a list of fields the user specified
                if 'fields' in bid:
                    true_fields = [x.strip() for x in self.parse_url(base_url, 'fields').split(',')]
                elif 'filter' in bid:
                    true_fields = [x.strip() for x in self.parse_url(base_url, 'filter').split(',')]
                # Next get the object with no fields specified
                total_url = ns.annotation_endpoint + '/' + _q(bid.split('?')[0])
                res_total = self.request(total_url).json()
                # Check the fields
                self.check_fields(res, res_total, true_fields, ns.additional_fields_for_check_fields_subset)

            # override to add more tests
            self._extra_annotation_GET(bid, res)

        # insert non ascii characters
        self.request('' + ns.annotation_endpoint + '/' + '\xef\xbf\xbd\xef\xbf\xbd', expect_status=404)

        # test msgpack on first ID
        self.check_msgpack(self.api + '/' + ns.annotation_endpoint + '/' + _q(ns.annotation_GET[0].split('?')[0]))

        # test unicode string handling
        self.request('' + ns.annotation_endpoint + '/' + ns.unicode_test_string, expect_status=404)

        # test empties
        self.request('' + ns.annotation_endpoint, expect_status=404)
        self.request('' + ns.annotation_endpoint + '/', expect_status=404)


        def test_annotation_POST(self):
        ''' Function to test POSTs to the annotation endpoint.

            Currently supports automatic testing of:
                ids
                fields
                filters
                jsonld
        '''
        base_url = ns.annotation_endpoint
        for (test_number, ddict) in enumerate(ns.annotation_POST):
            res = self.json_ok(self.post_ok(base_url, ddict))
            returned_ids = [h['_id'] if '_id' in h else h['query'] for h in res]
            assert set(returned_ids) == set([x.strip() for x in ddict['ids'].split(',')]), "Set of returned ids doesn't match set of requested ids for annotation POST"
            # Check that the number of returned objects matches the number of inputs
            # Probably not needed given the previous test
            eq_(len(res), len(ddict['ids'].split(',')))
            for hit in res:
                # If it's a jsonld query, check that
                if 'jsonld' in ddict and ddict['jsonld'].lower() in ['true', 1]:
                    self.check_jsonld(hit, '', jsonld_context=jsonld_context)
                # If its a filtered query, check the return objects fields
                if 'filter' in ddict or 'fields' in ddict:
                    true_fields = []
                    if 'fields' in ddict:
                        true_fields = [f.strip() for f in ddict.get('fields').split(',')]
                    elif 'filter' in ddict:
                        true_fields = [f.strip() for f in ddict.get('filter').split(',')]
                    total_url = base_url + '/' + _q(hit['_id'])
                    res_total = self.request(total_url).json()
                    self.check_fields(hit, res_total, true_fields, ns.additional_fields_for_check_fields_subset)

                self._extra_annotation_POST(ddict, hit)

        # Check unicode handling on first test
        res_empty = self.json_ok(self.post_ok(base_url, {'ids': ns.unicode_test_string}))
        assert (len(res_empty) == 1) and (res_empty[0]['notfound']), "POST to annotation endpoint failed with unicode test string"
        # Check unicode test string as the second id in the list
        res_second_empty = self.json_ok(self.post_ok(base_url, {'ids': ns.annotation_POST[0]['ids'].split(',')[0] + ',' + ns.unicode_test_string}))
        assert (len(res_second_empty) == 2) and (res_second_empty[1]['notfound']), "POST to annotation endpoint failed with unicode test string"

    def test_query_GET(self):
        ''' Function to test GETs to the query endpoint.

            Automatically tested parameters:

            fields
            filters
            size
            fetch_all/scroll_id
            facets
            callback

            Separately tested:

            from
        '''
        # Test some simple GETs to the query endpoint, first check some queries to make sure they return some hits
        for (test_number, q) in enumerate(ns.query_GET):
            base_url = ns.query_endpoint + '?q=' + q
            # parse callback
            if self.parse_url(base_url, 'callback'):
                res = self.extract_results_from_callback(base_url)
            elif self.check_boolean_url_option(base_url, 'fetch_all'):
                # Is this a fetch all query?
                # TODO:  make this less crappy.
                sres = self.request(base_url).json()
                assert '_scroll_id' in sres, "_scroll_id not found for fetch_all query: {}".format(q)
                scroll_hits = int(sres['total']) if int(sres['total']) <= 1000 else 1000
                res = self.request(self.api + '/' + ns.query_endpoint + '?scroll_id=' + sres['_scroll_id']).json()
                assert 'hits' in res, "No hits found for query: {}\nScroll ID: {}".format(q, sres['_scroll_id'])
                assert len(res['hits']) == scroll_hits, "Expected a scroll size of {}, got a scroll size of {}".format(scroll_hits, len(res['hits']))
            else:
                # does this query have hits?
                res = self.query_has_hits(q, ns.query_endpoint)
            # Test the size/size cap
            total_hits = int(res['total'])
            ret_size = len(res.get('hits', []))
            req_size = int(self.parse_url(base_url, 'size')) if self.parse_url(base_url, 'size') else 10
            if self.check_boolean_url_option(base_url, 'fetch_all'):
                true_size = scroll_hits
            elif total_hits < req_size:
                true_size = total_hits
            else:
                true_size = req_size if req_size <= 1000 else 1000
            assert ret_size == true_size, 'Expected {} hits for query "{}", got {} hits instead'.format(true_size, q, ret_size)
            # Test facets, maybe we should make it a subset test, i.e., set(returned facets) must be a subset of set(requested facets)
            if 'facets' in q:
                facets = [x.strip() for x in self.parse_url(base_url, 'facets').split(',')]
                assert 'facets' in res, "Facets were expected in the response object, but none were found."
                for facet in facets:
                    assert facet in res['facets'], 'Expected facet "{}" in response object, but it was not found'.format(facet)
            # Exhaustively test the first 10?
            for hit in res['hits'][:10]:
                # Make sure correct jsonld is in res
                if self.check_boolean_url_option(base_url, 'jsonld') and 'root' in jsonld_context:
                    hit = self.check_jsonld(hit, '', jsonld_context)
                if self.parse_url(base_url, 'fields') or self.parse_url(base_url, 'filter'):
                    # This is a filter query, test it appropriately
                    if 'fields' in q:
                        true_fields = [x.strip() for x in self.parse_url(base_url, 'fields').split(',')]
                    elif 'filter' in bid:
                        true_fields = [x.strip() for x in self.parse_url(base_url, 'filter').split(',')]
                    total_url = ns.annotation_endpoint + '/' + _q(hit['_id'])
                    res_total = {}
                    res_total = self.request(total_url).json()
                    if res_total:
                        self.check_fields(hit, res_total, true_fields, ns.additional_fields_for_check_fields_subset)
            # extra tests
            self._extra_query_GET(q, res)

        # test non-ascii characters
        res_f = self.request(self.api + '/' + ns.query_endpoint + '?q=' + '\xef\xbf\xbd\xef\xbf\xbd').json()
        assert res_f['hits'] == [], 'Query with non ASCII characters injected failed'

        # test msgpack on first query only
        self.check_msgpack(self.api + '/' + ns.query_endpoint + '?q=' + ns.query_GET[0])

        # test unicode insertion
        res = self.request(self.api + '/' + ns.query_endpoint + '?q=' + ns.unicode_test_string).json()
        assert res['hits'] == [], "GET to query endpoint failed with unicode test string"

        # test empty/error
        res = self.request(self.api + '/' + ns.query_endpoint), checkerror=False)
        assert 'error' in res, "GET to query endpoint failed with empty query"

    def test_query_POST(self):
        '''
            Test POSTS to the query endpoint.

        '''
        #query via post
        base_url = ns.query_endpoint
        for (test_number, ddict) in enumerate(ns.query_POST):
            res = self.json_ok(self.post_ok(base_url, ddict).json()
            returned_queries = [h['query'] for h in res]
            assert set(returned_queries) == set([x.strip() for x in ddict['q'].split(',')]), "Set of returned queries doesn't match set of requested queries for annotation POST"
            # Check that the number of returned objects matches the number of inputs
            # Probably not needed given the previous test
            eq_(len(res), len(ddict['q'].split(',')))
            for hit in res:
                # If it's a jsonld query, check that
                if 'jsonld' in ddict and ddict['jsonld'].lower() in ['true', 1]:
                    self.check_jsonld(hit, '', jsonld_context)
                # If its a filtered query, check the return objects fields
                if 'filter' in ddict or 'fields' in ddict:
                    true_fields = []
                    if 'fields' in ddict:
                        true_fields = [f.strip() for f in ddict.get('fields').split(',')]
                    elif 'filter' in ddict:
                        true_fields = [f.strip() for f in ddict.get('filter').split(',')]
                    total_url = ns.annotation_endpoint + '/' + _q(hit['_id'])
                    res_total = self.request(total_url).json()
                    self.check_fields(hit, res_total, true_fields, ns.additional_fields_for_check_fields_subset)

                self._extra_query_POST(ddict, hit)

        # test unicode insertion, make sure scopes points to a field that is string indexed or else these will fail...
        res = self.json_ok(self.post_ok(base_url, {'q': ns.unicode_test_string, 'scopes': ns.query_POST[0]['scopes']}), checkerror=False)
        assert (len(res) == 1) and (res[0]['notfound']), "POST to query endpoint failed with unicode test string"

        res = self.json_ok(self.post_ok(base_url, {'q': ns.query_POST[0]['q'].split(',')[0] + ',' +
                                ns.unicode_test_string, 'scopes': ns.query_POST[0]['scopes']}), checkerror=False)
        assert (len(res) == 2) and (res[1]['notfound']), "POST to query endpoint failed with unicode test string"

        # test empty post
        res = self.json_ok(self.post_ok(base_url, {'q': ''}), checkerror=False)
        assert 'error' in res, "POST to query endpoint failed with empty query"
    """

    def test_metadata(self):
        self.request('/metadata')
        self.request('metadata')

    def test_get_fields(self):
        res = self.request(self.api + '/metadata/fields').json()
        # Check to see if there are enough keys
        self.assertGreater(len(res), bts.MINIMUM_NUMBER_OF_ACCEPTABLE_FIELDS,
                           'Too few fields returned in the /metadata/fields endpoint')

        for field in bts.TEST_FIELDS_GET_FIELDS_ENDPOINT:
            self.assertIn(
                field,
                res,
                '"{}" expected in response from /metadata/fields, but not found'.format(field))

    def test_status_endpoint(self):
        self.request('/status')
        # (testing failing status would require actually loading tornado app from there
        #  and deal with config params...)

    @classmethod
    def suite(cls):
        tests = unittest.defaultTestLoader.getTestCaseNames(cls)
        return unittest.TestSuite(map(cls, tests))
