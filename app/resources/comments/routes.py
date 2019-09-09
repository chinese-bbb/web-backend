import logging

from flask import session
from flask.views import MethodView
from flask_user import login_required

from .schemas import CommentResponseSchema
from .schemas import CreateCommentParameters
from .services import CommentDAO
from flask_rest_api import Blueprint

log = logging.getLogger(__name__)

bp = Blueprint(
    'comments', 'comments', url_prefix='/comments', description='Comments Related API'
)

commentDAO = CommentDAO()


@bp.route('')
class Comment(MethodView):
    @login_required
    @bp.arguments(CreateCommentParameters)
    def post(self, data):
        """
        Create a Comment.
        """

        user_id = session['user_id']
        data['user_id'] = user_id
        res = commentDAO.create(data)
        if res == 'OK':
            return {'state': 'Success'}
        else:
            return {'state': 'failed creating comment'}, 422


@bp.route('/byComplaint/<int:id>')
class CommentsByComplaint(MethodView):
    @login_required
    @bp.response(CommentResponseSchema(many=True))
    def get(self, id):
        """
        get all Comments given one complaint.
        """

        res = commentDAO.fetch_all_by_complaintID(id)
        return res


@bp.route('/<int:id>')
class Comment2(MethodView):
    @login_required
    @bp.response(CommentResponseSchema)
    def get(self, id):
        """
        get a Comment by comment_id.
        """

        res = commentDAO.get(id)
        return res

    @login_required
    def delete(self, id):
        """
        Delete a comment by comment id.
        """

        res = commentDAO.delete(id)
        if res == 'deleted':
            return 'ok', 204
        else:
            return {'state': 'delete unsuccessful'}
