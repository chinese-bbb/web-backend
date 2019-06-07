import flask
from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from app import application, db, api
from app.models import User, FuzzySearchRaw, MerchantQueryRaw
from app.sms.send_sms import send_message
from app.qichacha.qichacha_api import fuzzy_search, basic_detail
from flask_restplus import Resource, fields
import datetime
import json

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


@ns.route('/merchant_query')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class MerchantQuery(Resource):

    @login_required
    @api.doc(parser=qichacha_parser)
    def post(self):
        '''fuzzy_query'''

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

            return {"return": json.loads(merchant_json_str)}
        else:
            storage = merchant_query_res.get_storage()
            print("has merchant query storage")
            return {"return": json.loads(storage)}
