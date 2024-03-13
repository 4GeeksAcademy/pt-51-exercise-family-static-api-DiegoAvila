"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }

    return jsonify(response_body), 200
#obtener un solo miembro
@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):

    member = jackson_family.get_member(member_id)
    response_body = {
        "member": member
    }

    return jsonify(response_body), 200
#añadir un miembro
@app.route('/member', methods=['POST'])
def add_new_member():

    request_body = request.json

    new_member={
        "first_name":request_body["first_name"],
        "age":request_body["age"],
        "lucky_numbers":request_body["lucky_numbers"],
        "id":jackson_family._generateId()
    }

    jackson_family.add_member(new_member)

    return jsonify(new_member), 200
# eliminar un miembro
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_one_member(member_id):

    delete_member = jackson_family.delete_member(member_id)
    if delete_member is not None:
        response_body = {"message": "Member deleted successfully", "family": delete_member}
        return jsonify(response_body), 200
    else:
        response_body = {"message": "Member not found"}
        return jsonify(response_body), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
