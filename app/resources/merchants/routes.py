import json
import logging

from flask import abort
from flask.views import MethodView
from flask_login import login_required

from .models import FuzzySearchRaw
from .models import MerchantQueryRaw
from .schemas import FuzzyQueryParameters
from .schemas import MerchantResponseSchema
from .schemas import MerchantSearchParameters
from .schemas import MerchantSearchResponseSchema
from app.extensions import db
from app.services.qichacha.qichacha_api import basic_detail
from app.services.qichacha.qichacha_api import fuzzy_search_pageIndex
from flask_rest_api import Blueprint

log = logging.getLogger(__name__)

bp = Blueprint(
    'merchants',
    'merchants',
    url_prefix='/merchants',
    description='Merchant Resources API',
)


@bp.route('/merchant_search')
class MerchantSearch(MethodView):
    @login_required
    @bp.arguments(MerchantSearchParameters, location='query')
    @bp.response(MerchantSearchResponseSchema)
    def get(self, args):
        """
        Merchant search by merchant keyword and page Index.
        """

        keyword = args['keyword']
        pageIndex = args['pageIndex']

        fuzzy_search_res = FuzzySearchRaw.query.filter_by(
            keyword=keyword, pageIndex=pageIndex
        ).first()

        if fuzzy_search_res is None:
            fuzzy_result_json_dict, total_records = fuzzy_search_pageIndex(
                keyword, pageIndex
            )
            fuzzy_result_json_str = json.dumps(fuzzy_result_json_dict)

            search_content = FuzzySearchRaw(keyword=keyword)
            search_content.set_storage(fuzzy_result_json_str)
            search_content.pageIndex = pageIndex
            search_content.totalPage = int(total_records / 10) + 1
            db.session.add(search_content)
            db.session.commit()

            return {
                'result': json.loads(fuzzy_result_json_str),
                'totalPage': search_content.totalPage,
            }
        else:
            storage = fuzzy_search_res.get_storage()
            obj = json.loads(storage)
            return {'result': obj, 'totalPage': fuzzy_search_res.totalPage}


def getMerchantIdFromDB(keyword):
    merchant_query_res = MerchantQueryRaw.query.filter_by(keyword=keyword).first()

    if merchant_query_res:
        return merchant_query_res.get_id()

    abort(404, "Merchant by keyword {} doesn't exist".format(keyword))


@bp.route('/merchant_query')
class MerchantQuery(MethodView):
    @login_required
    @bp.arguments(FuzzyQueryParameters, location='query')
    @bp.response(MerchantResponseSchema)
    def get(self, args):
        """
        Detailed Merchant_query.
        """

        keyword = args['keyword']

        merchant_query_res = MerchantQueryRaw.query.filter_by(keyword=keyword).first()
        if merchant_query_res is None:
            merchant_json_dict = basic_detail(keyword)
            merchant_json_str = json.dumps(merchant_json_dict)

            search_content = MerchantQueryRaw(keyword=keyword)
            search_content.set_storage(merchant_json_str)
            db.session.add(search_content)
            db.session.commit()

            merchant_query_return = MerchantQueryRaw.query.filter_by(
                keyword=keyword
            ).first()
            obj = json.loads(merchant_query_return.get_storage())
            return {'merchant_id': merchant_query_return.id, 'storage': obj}
        else:
            log.debug('has merchant query storage')
            obj = json.loads(merchant_query_res.get_storage())
            return {'merchant_id': merchant_query_res.id, 'storage': obj}


@bp.route('/<int:id>')
class Merchant(MethodView):
    @bp.response(MerchantResponseSchema)
    def get(self, id):
        """
        get a merchant by merchant_id.
        """

        merchant_query_res = MerchantQueryRaw.query.filter_by(id=id).first()

        if merchant_query_res:
            obj = json.loads(merchant_query_res.get_storage())
            return {'merchant_id': merchant_query_res.id, 'storage': obj}

        return "Merchant by merchant_id {} doesn't exist".format(id), 404

    @login_required
    @bp.doc(description='delete a merchant')
    def delete(self, id):
        """
        Delete a merchant by merchant id.
        """

        return 'This API is not supported yet.', 404
