from utils.encrypt import decryptPassword
from utils.DBPushQuery import pushQuery

def verificarUsuario(usuario, contrasena):
    queryTuple = (usuario,)
    result = pushQuery("SELECT password,id FROM users WHERE username = %s", queryTuple)
    if result is None:
        return None 
    bytesResultPassword = bytes.fromhex(result['password'][2:])
    contrStr = decryptPassword(bytesResultPassword).decode('utf-8')

    if contrStr == contrasena:
        return True
    else:
        return False

