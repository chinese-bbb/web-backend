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
upload_comment_parser.add_argument('complaint_id', type=int, required=True, help='complaint_id', location='json')

@ns.route('/comment')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class Comment(Resource):

    @login_required
    @ns.expect(upload_comment_parser)
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



update_comment_parser = api.parser()
update_comment_parser.add_argument('text', type=str, required=True, help='comment', location='json')

@ns.route('/comment/<int:id>')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
@ns.param('id', 'The Comment identifier')
class Comment(Resource):

    @login_required
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

    @ns.doc('update a comment')
    @ns.expect(update_comment_parser)
    @ns.response(200, 'Success', comment_marshall_model)
    def put(self, id):
        '''update a comment by comment id and text'''

        args = update_comment_parser.parse_args()
        text = args['text']

        return commentDAO.update(id, text)


@ns.route('/commentsByComplaint/<int:id>')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
@ns.param('id', 'The complaint identifier')
class CommentsByComplaint(Resource):

    @login_required
    @ns.response(200, 'Success', comment_marshall_model)
    def get(self, id):
        '''get Comment by comment_id'''
        res = commentDAO.fetch_all_by_complaintID(id)
        return res
