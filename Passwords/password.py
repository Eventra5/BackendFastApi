import bcrypt

# Función para hashear una contraseña
def hash_password(password: str) -> str:

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()
