from app.extensions import db


class FuzzySearchRaw(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(140))
    pageIndex = db.Column(db.Integer)
    totalPage = db.Column(db.Integer)
    storage = db.Column(db.String(10000))

    def __init__(self, keyword):
        self.keyword = keyword

    def set_storage(self, storage):
        self.storage = storage

    def get_storage(self):
        return self.storage

    def __repr__(self):
        return '<MerchantRaw {}>'.format(self.keyword)


class MerchantQueryRaw(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(140))
    storage = db.Column(db.String(20000))

    def __init__(self, keyword):
        self.keyword = keyword

    def set_storage(self, storage):
        self.storage = storage

    def get_storage(self):
        return self.storage

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<MerchantRaw {}>'.format(self.keyword)
