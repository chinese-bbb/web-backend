import json

from flask_login import login_required
from flask_restplus import Resource

from app import db, api
from app.models import FuzzySearchRaw, MerchantQueryRaw
from app.qichacha.qichacha_api import fuzzy_search, basic_detail

ns = api.namespace('api', description='All API descriptions')

qichacha_parser = api.parser()
qichacha_parser.add_argument('keyword', type=str, required=True, help='keyword', location='json')

@ns.route('/fuzzy_query')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class FuzzyQuery(Resource):

    @login_required
    @api.doc(parser=qichacha_parser)
    def post(self):
        '''fuzzy_query'''

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
    def post(self):
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

            merchant_id = getMerchantIdFromDB(keyword)
            return {"return": json.loads(merchant_json_str), "merchant_id": merchant_id}, 200
        else:
            storage = merchant_query_res.get_storage()
            print("has merchant query storage")

            merchant_id = getMerchantIdFromDB(keyword)
            return {"return": json.loads(storage), "merchant_id": merchant_id}, 200
