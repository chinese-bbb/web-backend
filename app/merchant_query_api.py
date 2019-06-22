import json

from flask_login import login_required
from flask_restplus import Resource

from app import db, api
from app.models import FuzzySearchRaw, MerchantQueryRaw
from app.qichacha.qichacha_api import fuzzy_search, basic_detail, fuzzy_search_pageIndex
from app.db_models.merchant_model import merchant_resp, merchant_search_resp
from marshmallow_jsonschema import JSONSchema

ns = api.namespace('api', description='All API descriptions')

json_schema = JSONSchema()
merchant_marshall_model = api.schema_model('MerchantResponse',
                                          json_schema.dump(merchant_resp).data['definitions']['MerchantResponse'])

merchant_search_marshall_model = api.schema_model('MerchantSearchResponse',
                                          json_schema.dump(merchant_search_resp).data['definitions']['MerchantSearchResponse'])

qichacha_parser = api.parser()
qichacha_parser.add_argument('keyword', type=str, required=True, help='keyword', location='args')

@ns.route('/fuzzy_query')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class FuzzyQuery(Resource):

    @login_required
    @api.doc(parser=qichacha_parser)
    def get(self):
        '''fuzzy_query with paging support'''

        args = qichacha_parser.parse_args()
        keyword = args['keyword']

        fuzzy_search_res = FuzzySearchRaw.query.filter_by(keyword=keyword).first()
        if fuzzy_search_res is None:
            fuzzy_result_json_dict = fuzzy_search(keyword)
            fuzzy_result_json_str = json.dumps(fuzzy_result_json_dict)

            search_content = FuzzySearchRaw(keyword=keyword)
            search_content.set_storage(fuzzy_result_json_str)
            db.session.add(search_content)
            db.session.commit()

            return {"return": json.loads(fuzzy_result_json_str)}
        else:
            storage = fuzzy_search_res.get_storage()
            obj = json.loads(storage)
            return {"return": obj}

qichacha_page_parser = api.parser()
qichacha_page_parser.add_argument('keyword',   type=str, required=True, help='keyword', location='args')
qichacha_page_parser.add_argument('pageIndex', type=int, required=True, help='pageIndex', location='args')

@ns.route('/merchant_search')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class MerchantSearch(Resource):

    @login_required
    @api.doc(parser=qichacha_page_parser)
    @ns.response(200, 'Success', merchant_search_marshall_model)
    def get(self):
        '''Merchant search by merchant keyword and page Index'''

        args = qichacha_page_parser.parse_args()
        keyword = args['keyword']
        pageIndex = args['pageIndex']

        fuzzy_search_res = FuzzySearchRaw.query.filter_by(keyword = keyword,
                                                          pageIndex = pageIndex).first()
        if fuzzy_search_res is None:
            fuzzy_result_json_dict, total_records = fuzzy_search_pageIndex(keyword, pageIndex)
            fuzzy_result_json_str = json.dumps(fuzzy_result_json_dict)

            search_content = FuzzySearchRaw(keyword=keyword)
            search_content.set_storage(fuzzy_result_json_str)
            search_content.pageIndex = pageIndex
            search_content.totalPage = int(total_records/10) + 1
            db.session.add(search_content)
            db.session.commit()

            return {"result": json.loads(fuzzy_result_json_str),
                    "totalPage": search_content.totalPage}
        else:
            storage = fuzzy_search_res.get_storage()
            obj = json.loads(storage)
            return {"result": obj,
                    "totalPage:": fuzzy_search_res.totalPage}


def getMerchantIdFromDB(keyword):
    merchant_query_res = MerchantQueryRaw.query.filter_by(keyword=keyword).first()

    if merchant_query_res:
        return merchant_query_res.get_id()

    api.abort(404, "Merchant by keyword {} doesn't exist".format(keyword))

@ns.route('/merchant_query')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class MerchantQuery(Resource):

    @login_required
    @api.doc(parser=qichacha_parser)
    @ns.response(200, 'Success', merchant_search_marshall_model)
    def get(self):
        '''Detailed Merchant_query'''

        args = qichacha_parser.parse_args()
        keyword = args['keyword']

        merchant_query_res = MerchantQueryRaw.query.filter_by(keyword=keyword).first()
        if merchant_query_res is None:
            merchant_json_dict = basic_detail(keyword)
            merchant_json_str = json.dumps(merchant_json_dict)

            search_content = MerchantQueryRaw(keyword=keyword)
            search_content.set_storage(merchant_json_str)
            db.session.add(search_content)
            db.session.commit()

            merchant_query_return = MerchantQueryRaw.query.filter_by(keyword=keyword).first()
            dump_data = merchant_resp.dump(merchant_query_return).data
            ret_storage = json.loads(merchant_query_return.get_storage())
            dump_data['storage'] = ret_storage
            return dump_data
        else:
            print("has merchant query storage")
            dump_data = merchant_resp.dump(merchant_query_res).data
            ret_storage = json.loads(merchant_query_res.get_storage())
            dump_data['storage'] = ret_storage
            return dump_data

@ns.route('/merchant/<int:id>')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
@ns.param('id', 'The Complaint Identifier')
class Merchant(Resource):

    @login_required
    @ns.response(200, 'Success', merchant_marshall_model)
    def get(self, id):
        '''get a merchant by merchant_id'''
        merchant_query_res = MerchantQueryRaw.query.filter_by(id=id).first()

        if merchant_query_res:
            dump_data = merchant_resp.dump(merchant_query_res).data
            ret_storage = json.loads(merchant_query_res.get_storage())
            dump_data['storage'] = ret_storage
            return dump_data
        api.abort(404, "Merchant by merchant_id {} doesn't exist".format(id))

    @ns.doc('delete a merchant')
    @ns.response(204, 'merchant deleted')
    def delete(self, id):
        '''Delete a merchant by merchant id'''

        ns.abort(404, "This API is not supported yet.")