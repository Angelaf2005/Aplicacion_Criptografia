from cryptography.fernet import Fernet
import os
from datetime import datetime

def fernet_encrypt(message, file_name):
    user_folder = f'Data/Fernet/Keys/{file_name}'
    key_path = f"{user_folder}/{file_name}.key"

    with open(key_path, 'rb') as key_file:        
        key = key_file.read()

    cipher_suite = Fernet(key)
    bytes_message = message.encode('utf-8')
    encrypted_message = cipher_suite.encrypt(bytes_message)
    print(encrypted_message)
    return encrypted_message

# Genera las clave privada fernet
def fernet_key_generator(file_name):
    # Construir path de la clave del usuario
    path = 'Data/Fernet/Keys/'+ file_name
    # Crear el directorio
    os.makedirs(f"{path}", exist_ok=True)
    # SI no existe una clave, generarla
    if not os.path.exists(f"{path}/{file_name}.key"):
        # Generar la clave
        key = Fernet.generate_key()

        # Guardar la clave generada en un archivo.
        with open(f"{path}/{file_name}.key", 'wb') as key_file:
            key_file.write(key)

def fernet_decrypt(file_name):
    encrypted_file_path = f'Data/Fernet/Notes/{file_name}/'+file_name+'.txt'   
    print(encrypted_file_path)    # Verificar si existe txt
    if not  os.path.exists(encrypted_file_path):
        return "No hay notas guardadas"

    key_path = f'Data/Fernet/Keys/{file_name}/{file_name}.key'                      # Verificar existencia clave 
    if not os.path.exists(key_path):
        return "No existe clave"

    with open(key_path, 'rb') as key_file:                              # Leer la clave del archivo
        key = key_file.read()

    with open(encrypted_file_path, 'rb') as encrypted_file:             # Leer el mensaje encriptado
        encrypted_message = encrypted_file.read()

    cipher_suite = Fernet(key)                                          # Desencriptar el mensaje
    decrypted_message = cipher_suite.decrypt(encrypted_message)
    return decrypted_message.decode('utf-8')
def save_note(message, file_name):                         # Generar clave y encriptar mensaje (formato)
    encrypted_message = fernet_encrypt(message, file_name)

    user_folder = 'Data/Fernet/Notes/'+file_name         # Crear carpeta para el usuario si no existe (almacenar el archivo)
    os.makedirs(user_folder, exist_ok=True)
    file_path = f"{user_folder}/{file_name}.txt"             # Guardar mensaje encriptado en un archivo dentro de la carpeta del usuario
    with open(file_path, 'wb') as message_file:
        message_file.write(encrypted_message)
def read_encrypted_messages(file_name):
    user_folder = f'Data/Fernet/Notes/{file_name}'
    
    # Verificar si la carpeta del usuario existe
    if not os.path.exists(user_folder):
        print(f"No se encontró la carpeta para el usuario {file_name}.")
        return []

    
    # Iterar sobre todos los archivos en la carpeta del usuario
    for filename in os.listdir(user_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(user_folder, filename)
            with open(file_path, 'rb') as file:
                encrypted_message = file.read()
                encrypted_messages = encrypted_message.decode('utf-8')
    
    return encrypted_messages