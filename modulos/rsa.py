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
        public_exponent=65537,  # Exponente público comúnmente utilizado
        key_size=2048,  # Tamaño de la clave, por defecto 2048 bits
        backend=default_backend()  # Usar el backend por defecto
    )
    
    # Obtener la clave pública a partir de la clave privada
    public_key = private_key.public_key()
    
    # Serializar las claves en formato PEM
    encrypted_private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password_bytes)
    )
    
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Verificar existencia de carpetas
    private_path = 'Data/RSA/Private-Keys'
    public_path = 'Data/RSA/Public-Keys'

    os.makedirs(private_path, exist_ok=True)
    os.makedirs(public_path, exist_ok=True)

    # Guardar las claves en archivos
    with open(f"{private_path}/{file_name}_clave_privada.der", "wb") as f:
        f.write(encrypted_private_key_pem)

    with open(f"{public_path}/{file_name}_clave_publica.der", "wb") as f:
        f.write(public_key_pem)





def rsa_encrypt(message, public_key_der):
    # Cargar la clave publica del destinatario desde DER
    destination_public_key = serialization.load_der_public_key(
        public_key_der,
        backend=default_backend()
        )
    
    # Convertir el mensaje a bytes
    message_bytes = message.encode('utf-8')

    # Cifrar el mensaje con la clave publica del destinatario
    cipher_message = destination_public_key.encrypt(
        message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return cipher_message