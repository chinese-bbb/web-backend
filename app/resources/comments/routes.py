import logging

from flask import session
from flask_login import login_required
from flask_restplus import Namespace
from flask_restplus import Resource
from marshmallow_jsonschema import JSONSchema

from .models import comment_schema
from .models import CommentDAO
from .models import comments_schema
from app.extensions import api

log = logging.getLogger(__name__)

json_schema = JSONSchema()

ns = Namespace('comments', path='/comments', description='Comment Resources API')
commentDAO = CommentDAO()

comment_marshall_model = api.schema_model(
    'CommentResponse',
    json_schema.dump(comment_schema).data['definitions']['CommentResponse'],
)
comments_marshall_model = api.schema_model(
    'CommentsResponse',
    json_schema.dump(comments_schema).data['definitions']['CommentsResponse'][
        'properties'
    ]['CommentsResponse'],
)

upload_comment_parser = api.parser()
upload_comment_parser.add_argument(
    'text', type=str, required=True, help='comment text body', location='json'
)
upload_comment_parser.add_argument(
    'complaint_id', type=int, required=True, help='complaint_id', location='json'
)


@ns.route('/')
@api.doc(responses={200: 'Success', 400: 'Validation Error'})
class Comment(Resource):
    @login_required
    @ns.expect(upload_comment_parser)
    def post(self):
        """Create a Comment."""
        data = api.payload

        user_id = session['user_id']
        data['user_id'] = user_id
        res = commentDAO.create(data)
        if res == 'OK':
            return {'state': 'Success'}, 200
        else:
            return {'state': 'failed creating comment'}, 401


update_comment_parser = api.parser()
update_comment_parser.add_argument(
    'text', type=str, required=True, help='comment', location='json'
)


@ns.route('/byComplaint/<int:id>')
@api.doc(responses={200: 'Success', 400: 'Validation Error'})
@ns.param('id', 'The complaint identifier')
class CommentsByComplaint(Resource):
    @login_required
    @ns.response(200, 'Success', comments_marshall_model)
    def get(self, id):
        """get all Comments given one complaint."""
        res = commentDAO.fetch_all_by_complaintID(id)
        return res, 200


@ns.route('/<int:id>')
@api.doc(responses={200: 'Success', 400: 'Validation Error'})
@ns.param('id', 'The Comment identifier')
class Comment2(Resource):
    @login_required
    @ns.response(200, 'Success', comment_marshall_model)
    def get(self, id):
        """get a Comment by comment_id."""
        res = commentDAO.get(id)
        return res

    @ns.doc('delete a comment')
    @ns.response(204, 'Comment deleted')
    def delete(self, id):
        """Delete a comment by comment id."""
        res = commentDAO.delete(id)
        if res == 'deleted':
            return '', 204
        else:
            return {'state': 'delete unsuccessful'}, 200

    @ns.doc('update a comment')
    @ns.expect(update_comment_parser)
    @ns.response(200, 'Success', comment_marshall_model)
    def put(self, id):
        """update a comment by comment id and text."""

        args = update_comment_parser.parse_args()
        text = args['text']

        return commentDAO.update(id, text)
