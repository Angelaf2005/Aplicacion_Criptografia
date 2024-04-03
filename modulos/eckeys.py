from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os


#Genera llave publica y privada utilizando la curva eliptica NIST P-256
def keys_generator(file_name, passw):
    #Generar una clave privada
    private_key = ec.generate_private_key(ec.SECP256R1())

    # Obtener la clave publica correspondiente
    public_key = private_key.public_key()

    #Convertir la contraseña del usuario a bytes
    password = passw.encode('utf-8')

    # Serializar la clave privada en formato PEM con encriptación
    encrypted_private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
    )

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Verificar existencia de carpetas
    os.makedirs('Data/ECDSA/Private-Keys', exist_ok=True)
    os.makedirs('Data/ECDSA/Public-Keys', exist_ok=True)

    # Guardar las claves en archivos .PEM
    private_path = 'Data/ECDSA/Private-Keys'
    public_path = 'Data/ECDSA/Public-Keys'

    with open(f"{private_path}/{file_name}_private_key.pem",'wb') as key_file:
        key_file.write(encrypted_private_key_pem)

    with open(f"{public_path}/{file_name}_public_key.pem", 'wb') as key_file:
        key_file.write(public_key_pem)


# Crea la firma digital
def sign(file_name, passw, msg):
    #Convertir el mensaje a bytes
    message = msg.encode('utf-8')

    # Convertir la contraseña del usuario a bytes
    password = passw.encode('utf-8')

    # Leer la clave privada desde el archivo
    with open(f"Private-Keys/{file_name}_private_key.pem", 'rb') as key_file:
        encrypted_private_key = key_file.read()

    # Desencriptar la clave privada utilizando la contraseña
    private_key = serialization.load_pem_private_key(
        encrypted_private_key,
        password=password,
        backend=default_backend()
    )
    
    # Firmar el mensaje utilizando la clave privada
    signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))

    #Convertir a hexadecimal
    signature_hex = signature.hex()


    # Verificar la firma utilizando la clave pública
    # try:
    #     public_key.verify(signature, mensaje, ec.ECDSA(hashes.SHA256()))
    #     print("La firma es válida.")
    # except:
    #     print("La firma no es válida.")

    return signature_hex

