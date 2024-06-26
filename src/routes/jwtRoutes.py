from flask import Blueprint,request,jsonify
from datetime import timedelta

from services.userAuth import verificarUsuario
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity,get_jwt
from utils.DBPushQuery import pushQuery
from datetime import datetime,timezone

jwtRoutesBluePrint = Blueprint('jwtRoutes',__name__)
@jwtRoutesBluePrint.route('/login', methods=['POST'])
def login():
    user = request.get_json()
    username = str(user['username'])
    userpassword = str(user['password'])

    result = verificarUsuario(username,userpassword)

    if result == True:
        return jsonify({'access_token':create_access_token(identity=username),
                        'refresh_token':create_refresh_token(identity=username,expires_delta=False)}),200
    else:
        return jsonify({'message':'Credenciales Incorrectas'}),401



@jwtRoutesBluePrint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

@jwtRoutesBluePrint.route("/logout",methods=["DELETE"])
@jwt_required()
def Logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    queryTuple=(jti,now)
    result = pushQuery('INSERT INTO tokenblocklist (jti,created_at) VALUES (%s,%s)RETURNING id',queryTuple)
    return jsonify({'message':'Se ha cerrado la sesión'}),200


def check_if_token_revoked(jwtPayload:dict) -> bool:
    jti = jwtPayload["jti"]
    queryTuple = (jti,)
    result = pushQuery('SELECT * FROM tokenblocklist WHERE jti = %s',queryTuple)

    return result is not None


@jwtRoutesBluePrint.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
        return response
    except (RuntimeError, KeyError):
        return response