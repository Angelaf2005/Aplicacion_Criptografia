from cryptography.fernet import Fernet
import os


def fernet_encrypt(message, file_name):

    # Verificar existencia de carpetas
    path = 'Data/Fernet/Keys'

    #Leer la clave del archivo
    with open(f"{path}/{file_name}.key", 'rb') as key_file:
        key = key_file.read()

    cipher_suite = Fernet(key)
    bytes_message = message.encode('utf-8')
    encrypted_message = cipher_suite.encrypt(bytes_message)

    return encrypted_message



def fernet_key_generator(file_name):
    
    path = 'Data/Fernet/Keys'

    os.makedirs(f"{path}", exist_ok=True)

    if not os.path.exists(f"{path}/{file_name}.key"):
        # Generar la clave
        key = Fernet.generate_key()

        # Guardar la clave generada en un archivo.
        with open(f"{path}/{file_name}.key", 'wb') as key_file:
            key_file.write(key)


