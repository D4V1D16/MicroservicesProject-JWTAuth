from flask import Blueprint,jsonify,request
from utils.encrypt import encrypt
from flask_jwt_extended import get_jwt_identity,jwt_required, get_jwt
from utils.DBPushQuery import pushQuery
from .jwtRoutes import check_if_token_revoked


crud = Blueprint('crudUsers',__name__)


@crud.post('/api/users')
def create_users():
    usuario = request.get_json()
    username = usuario['username']
    userpass = usuario['password']
    userpass = encrypt(userpass)
    queryTuple = (username, userpass)
    result = pushQuery('INSERT INTO users (username,password) VALUES (%s,%s) RETURNING *;', queryTuple)
    return jsonify(result)


@crud.delete('/api/users/<id>')
@jwt_required()
def delete_users(id):
    tokenRes = check_if_token_revoked(get_jwt())
    if tokenRes == True:
        return jsonify({'message': 'Token Revocado'}), 403
    else:        
        current_user = get_jwt_identity()
        result = pushQuery('SELECT username FROM users WHERE id = %s', (id,))
        print(current_user)
        if result['username'] != current_user:
            return jsonify({'message': 'No puedes borrar este usuario'}), 403
        else:   
            queryTuple = (id,)
            result = pushQuery('DELETE FROM users WHERE id = %s RETURNING *',queryTuple)

            return jsonify({'message': 'Se ha eliminado el usuario correctamente'}),200


@crud.put('/api/users/<id>')
@jwt_required()
def update_users(id): 
    resultToken = check_if_token_revoked(get_jwt())
    if resultToken == True:
        return jsonify({'message': 'Token Revocado'}), 403
    else:
        current_user = get_jwt_identity()
        result = pushQuery('SELECT username FROM users WHERE id = %s', (id,))
        if result['username'] != current_user:
            return jsonify({'message': 'No puedes actualiza a otros usuarios'}), 403
        else:
            usuario = request.get_json()
            username = usuario['username']
            queryTuple = (username,id)
            result = pushQuery('UPDATE users SET username = %s WHERE id = %s RETURNING username',queryTuple)
            return jsonify({'message':'Se han actualizado los datos correctamente'}), 200


@crud.get('/api/users/<id>')
def getOne_user(id):
    queryTuple = (id,)
    result = pushQuery('SELECT username FROM users WHERE id = %s',queryTuple)
    if result is None:
        return jsonify({'Mensaje':'Usuario no encontrado'}),404 
    else:
        return jsonify(result)