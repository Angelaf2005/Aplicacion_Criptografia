from ast import Return
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import os


def rsa_key_generator(file_name, password):
    # Codificar la contraseña a bytes
    password_bytes = password.encode('utf-8')


    # Generar un par de claves RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,          # Exponente público comúnmente utilizado
        key_size=2048,                  # Tamaño de la clave, por defecto 2048 bits
        backend=default_backend()       # Usar el backend por defecto
    )
    
    # Obtener la clave pública a partir de la clave privada
    public_key = private_key.public_key()
    
    # Serializar las claves en formato PEM
    encrypted_private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password_bytes)
    )
    
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Verificar existencia de carpetas
    keys_directory = f"Data/RSA/Keys/{file_name}"
    private_path = f"{keys_directory}/{file_name}_Private-Keys" 
    public_path =  f"{keys_directory}/{file_name}_Public-Keys" 

    os.makedirs(private_path, exist_ok=True)
    os.makedirs(public_path, exist_ok=True)

    # Guardar las claves en archivos
    with open(f"{private_path}/{file_name}_clave_privada.pem", "wb") as f:
        f.write(encrypted_private_key_pem)

    with open(f"{public_path}/{file_name}_clave_publica.pem", "wb") as f:
        f.write(public_key_pem)
        

def rsa_encrypt(message, public_key_pem):

    # Cargar la clave publica del destinatario
    public_key = serialization.load_pem_public_key(
        public_key_pem,
        backend=default_backend()
    )
        
    
    # Convertir el mensaje a bytes
    message_bytes = message.encode('utf-8')

    # Cifrar el mensaje con la clave publica del destinatario
    cipher_message = public_key.encrypt(
        message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return cipher_message.hex()

def rsa_decrypt(file_name, password):
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes
    import os

    # Rutas de la clave privada y el mensaje encriptado
    private_key_file = f"Data/RSA/Keys/{file_name}/{file_name}_Private-Keys/{file_name}_clave_privada.pem"
    encrypted_message_file = f"Data/RSA/Notes/{file_name}/{file_name}_encrypted_note.txt"

    # Verificar si la clave privada y el mensaje encriptado existen
    if not os.path.exists(private_key_file):
        return f"No se encontró la clave privada para el usuario {file_name}."
    if not os.path.exists(encrypted_message_file):
        return f"No se encontró el mensaje encriptado para el usuario {file_name}."

    # Cargar la clave privada del destinatario
    with open(private_key_file, "rb") as key_file:
        private_key_pem = key_file.read()

    # Leer el mensaje encriptado desde el archivo
    with open(encrypted_message_file, "r") as message_file:
        encrypted_message_hex = message_file.read().strip()

    # Convertir el mensaje encriptado de hexadecimal a bytes
    encrypted_message = bytes.fromhex(encrypted_message_hex)

    # Deserializar y desencriptar la clave privada
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=password.encode('utf-8'),
        backend=default_backend()
    )

    # Desencriptar el mensaje con la clave privada
    decrypted_message_bytes = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_message_bytes.decode('utf-8')

def save_notes(message, file_name, password):
    # Verificar y crear el directorio 'RSA/Notes/usuario' si no existe
    notes_directory = f"Data/RSA/Notes/{file_name}"
    os.makedirs(notes_directory, exist_ok=True)

    # Directorio para las claves privadas
    keys_directory = f"Data/RSA/Keys/{file_name}"
    private_path = f"{keys_directory}/{file_name}_Private-Keys"
    public_path = f"{keys_directory}/{file_name}_Public-Keys"
    os.makedirs(private_path, exist_ok=True)
    os.makedirs(public_path, exist_ok=True)

    # Verificar si la clave pública del destinatario existe
    public_key_file = f"{public_path}/{file_name}_clave_publica.pem"
    if not os.path.exists(public_key_file):
        return print(f"La clave pública de {file_name} no existe.")

    # Obtener la clave pública del destinatario
    with open(public_key_file, "rb") as f:
        public_key_pem = f.read()

    # Encriptar el mensaje
    encrypted_message = rsa_encrypt(message, public_key_pem)

    # Guardar el mensaje encriptado en un archivo
    with open(f"{notes_directory}/{file_name}_encrypted_note.txt", "w") as f:
        f.write(encrypted_message)



def read_encrypted_notes(file_name):
    # Directorio donde se almacenan las notas encriptadas
    notes_directory = f"Data/RSA/Notes/{file_name}"
    
    # Verificar si la carpeta de notas del usuario existe
    if not os.path.exists(notes_directory):
        return f"No se encontraron notas encriptadas para el usuario {file_name}."
    # Iterar sobre los archivos en la carpeta de notas
    for filename in os.listdir(notes_directory):
        if filename.endswith('_encrypted_note.txt'):
            encrypted_note_file = os.path.join(notes_directory, filename)

            # Leer el mensaje encriptado de cada archivo
            with open(encrypted_note_file, "r") as f:
                encrypted_message_hex = f.read().strip()
                return encrypted_message_hex
        else:
                new_var = f'No hay notas guardadas para el usuario {file_name}'
                return new_var