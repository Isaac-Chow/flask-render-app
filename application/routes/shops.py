from flask_smorest import Blueprint
from marshmallow import Schema, fields
from flask.views import MethodView
from application.models import Shop


shop_blp = Blueprint('shop', 'shop', url_prefix='/shops')


class ShopSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    price = fields.Float()
    quantity = fields.Integer()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        ordered = True


class ShopNewSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    price = fields.Float(required=True)
    quantity = fields.Integer(required=True)

    class Meta:
        ordered = True


@shop_blp.route('/', methods=['GET', 'POST'])
class Shops(MethodView):
    @shop_blp.response(200, ShopSchema(many=True), description='List of shops')
    def get(self):
        shops = Shop.query.all()
        return shops
    
    # @shop_blp.arguments(ShopNewSchema)
    # @shop_blp.response(201, ShopSchema, description='New shop created')
    # def post(self, new_data):
    #     new_shop = Shop(**new_data)
    #     new_shop.save()
    #     return new_shop, 201
    
    
    @shop_blp.arguments(ShopNewSchema(many=True))
    @shop_blp.response(201, ShopSchema(many=True), description='New shops created')
    def post(self, new_data):
        new_shops = []
        for shop_data in new_data:
            new_shop = Shop(**shop_data)
            new_shop.save()
            new_shops.append(new_shop)
        return new_shops, 201
    

@shop_blp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
class ShopDetail(MethodView):
    @shop_blp.response(200, ShopSchema, description='Shop detail')
    def get(self, id):
        found_shop = Shop.query.get_or_404(id)
        return found_shop
    
    @shop_blp.arguments(ShopNewSchema)
    @shop_blp.response(202, ShopSchema, description='Shop updated')
    def put(self, new_data, id):
        found_shop = Shop.query.get_or_404(id)
        found_shop.update(**new_data)
        return found_shop
    
    @shop_blp.response(204)
    def delete(self, id):
        found_shop = Shop.query.get_or_404(id)
        found_shop.delete()
        return None, 204