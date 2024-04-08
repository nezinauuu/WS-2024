from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json
import graphene
import requests
from flask_restful import reqparse
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.objectid import ObjectId

app = Flask(__name__)
api = Api(app)

class GetProducts(Resource):
    def get(self):
        client = MongoClient("mongodb://root:example@localhost:27017/")
        db = client.sales
        collection = db.sales_data
        results = dumps(collection.find())
        return json.loads(results)

api.add_resource(GetProducts, '/getProducts')

class Product(graphene.ObjectType):
    title = graphene.String()
    
class Query(graphene.ObjectType):
    product = graphene.List(Product)
    def resolve_product(root,info):
        data = requests.get('http://127.0.0.1:5000/getProducts')
        json_content = json.loads(data.text)
        pName = [item.get('P-name') for item in json_content]
        products = [Product(title=pName) for pName in pName]
        return products

class GetTitles(Resource):
    def get(self):
        schema = graphene.Schema(query=Query)
        query = """
                {
                product {
                title
                }
                }
            """
        result = schema.execute(query)
        return result.data
    
api.add_resource(GetTitles, '/getTitles')

class insertProduct(Resource):
    # Define your custom API key
    CUSTOM_API_KEY = "custom_api_key"
    
    def post(self):
        # Check if the API key has been provided
        api_key = request.args.get('api_key')
        if api_key != self.CUSTOM_API_KEY:
            return{"Error": "Please provide a valid API key."},
        401
        
        # Parse the request data
        data = request.get_json()
        
        #Extract data from the request
        product_id = data.get('ProductId')
        title = data.get('P-name')
        cost = data.get('cost')
        # quantity = data.get('Quantity')
        
        # Validate the request data
        if not all([product_id, title, cost]):
            return {"Error": "Missing required data"}, 400
        
        # Connect to MongoDB and insert the product data
        client = MongoClient("mongodb://root:example@localhost:27017/")
        db = client.sales
        collection = db.sales_data
        
        new_record = {"ProductId": product_id, "P-name": title, "cost": cost}
        collection.insert_one(new_record)
        
        return {"status": "inserted"}, 201

api.add_resource(insertProduct, '/insertProduct')

class APIDescription(Resource):
    def get(self):
        description = { 
            "/getProducts": "in the getProducts page, the GET request retrieves a list of all products from the mongo database.", 
            "/getTitles": "In the getTitles page, the GET request retrieves titles of all products using GraphQL query.", 
            "/insertProduct?api_key=<YOUR_API_KEY>": "This is how you add a new product to the database, but you need an API key to do it.", 
            "/": "This is a page that shows you all the different things you can do with the API and explains how they work" 
        } 
        return jsonify(description)
    
api.add_resource(APIDescription, '/')

if __name__ == '__main__':
    app.run(debug=True)
    
  