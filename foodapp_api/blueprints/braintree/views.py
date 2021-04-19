from app import app
from flask import Blueprint, jsonify, request, flash
import braintree

braintree_api_blueprint = Blueprint('braintree_api',
                             __name__,
                             template_folder='templates')

gateway = braintree.BraintreeGateway(
  braintree.Configuration(
    environment=braintree.Environment.Sandbox,
    merchant_id='528rm4hjbzqjv82f',
    public_key='fxthd42ybyysh3x7',
    private_key='d47f5dea1181d878fd308e016fc0bcb2'
  )
)

@braintree_api_blueprint.route('/<id>purchase', methods=['GET'])
def purchase(id):
    client_token = gateway.client_token.generate({})
    return jsonify({
        "client_token": client_token,
        "customer_id": id
    })

@braintree_api_blueprint.route('/<id>purchase/process', methods=['POST'])
def process_purchase(id):
    nonce = request.json.get("nonce_payment")
    service = request.json.get("service")
    result = gateway.transaction.sale({
    "amount": service,
    "payment_method_nonce": nonce,
    "options": {"submit_for_settlement": True}
    })
    if result.is_success:
        flash("Successful Transaction")
        return jsonify({
          "messages": "Successfull",
          "status" : "Success"
        }), 200
    else:
        flash("Unsuccessful Transaction")
        return jsonify({
          "messages": "Unsuccessful",
          "status" : "Fail"
        })