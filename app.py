import os
import json
from flask import Flask
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from flask import Flask, request # change
 
app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'root'),
    os.getenv('DB_PASSWORD', '1q2w3e4r'),
    os.getenv('DB_HOST', '127.0.0.1'),
    os.getenv('DB_NAME', 'warehouse')
)

db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))
    price = db.Column(db.Integer)
    count = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Product %r>' % self.name
 
# create the DB on demand
@app.before_first_request
def create_tables():
    db.create_all()


@api.route('/products')
class ProductIndex(Resource):
    def get(self):
        ret = []
        res = Product.query.all()
        for product in res:
            ret.append(
                {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'price': product.price,
                    'count': product.count
                }
            )
        return ret, 200

@api.route('/product')
@api.response(404, "Could not put product")
class ProductPost(Resource):
    def post(self):
        data = request.get_json(force=True)
        product = Product(
            name = data['name'],
            description = data['description'],
            price = data['price'],
            count = data['count']
        )
        db.session.add(product)
        db.session.commit()
        return {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'count': product.count
            }, 200


@api.route('/product/<int:id>')
@api.response(404, "Could not find product")
@api.param('id', 'The task identifier')
class ProductItem(Resource):
    def get(self, id):
        product = Product.query.get_or_404(id)
        return  {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'price': product.price,
                    'count': product.count
                }, 200
    def patch(self, id):  
        product = Product.query.get_or_404(id)
        data = request.get_json(force=True)

        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = data['price']
        if 'count' in data:
            product.count = data['count']

        db.session.commit()

        return  {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'price': product.price,
                    'count': product.count
                }, 200

    def delete(self, id):  
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return '', 204

@api.route('/')
class Main(Resource):
    def get(self):
        return {'status': Product.__tablename__}

#api.add_resource(Index, '/products')
#api.add_resource(Main, '/')
#api.add_resource(Main, '/product')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
