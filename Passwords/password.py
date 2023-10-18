import bcrypt

def hashed_password(contraseña):
    # Genera un salt aleatorio
    salt = bcrypt.gensalt()
    # Hashea la contraseña con el salt
    hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), salt)
    # Devuelve el hash y el salt como cadena
    return hashed_password, salt