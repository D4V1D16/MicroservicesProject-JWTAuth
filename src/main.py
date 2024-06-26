from datetime import timedelta

from flask import Flask
from routes.CRUDUsers import crud
from routes.jwtRoutes import jwtRoutesBluePrint
from flask_jwt_extended import JWTManager

ACCESS_EXPIRES = timedelta(hours=1)


appFlask = Flask(__name__)
appFlask.config["JWT_SECRET_KEY"] = "SecretKEYdfhdjkfhdjkfdsh"  
appFlask.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(appFlask)

# Configuración de la aplicación Flask y registro de blueprints
appFlask.register_blueprint(crud)
appFlask.register_blueprint(jwtRoutesBluePrint)

if __name__ == '__main__':
    appFlask.run(debug=True)


