from flask import session
from flask_login import login_required
from app import api
from flask_restplus import Resource, fields, marshal_with
from app.db_models.comment_model import CommentDAO, comment_schema
from marshmallow_jsonschema import JSONSchema

json_schema = JSONSchema()

ns = api.namespace('api', description='All API descriptions')
commentDAO = CommentDAO()

comment_marshall_model = api.schema_model('Comment',
                                          json_schema.dump(comment_schema).data['definitions']['CommentSchema'])

upload_comment_parser = api.parser()
upload_comment_parser.add_argument('text', type=str, required=True, help='comment text body', location='json')

get_comment_parser = api.parser()
get_comment_parser.add_argument('comment_id', type=str, required=True, help='comment', location='values')

@ns.route('/comment')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class Comment(Resource):

    @login_required
    @api.expect(upload_comment_parser)
    def post(self):
        '''Create a Comment'''
        data = api.payload

        user_id = session["user_id"]
        data['user_id'] = user_id
        res = commentDAO.create(data)
        if res == "OK":
            return {"state": "Success"}, 200
        else:
            return {"state": "failed creating comment"}, 401

@ns.route('/comment/<int:id>')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
@ns.param('id', 'The Comment identifier')
class Comment(Resource):

    @login_required
    @api.expect(get_comment_parser)
    @ns.response(200, 'Success', comment_marshall_model)
    def get(self, id):
        '''get Comment by comment_id'''
        res = commentDAO.get(id)
        return res

    @ns.doc('delete a comment')
    @ns.response(204, 'Comment deleted')
    def delete(self, id):
        '''Delete a comment by comment id'''
        res = commentDAO.delete(id)
        if res == "deleted":
            return '', 204
        else:
            return {"state": "delete unsuccessful"}, 200