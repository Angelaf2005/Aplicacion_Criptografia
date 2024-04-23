from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
from datetime import datetime
import os


# Genera llave publica y privada utilizando la curva eliptica NIST P-256
# Genera el certificado y la clave privada encriptada para los archivos
def keys_generator(name, username, password, email):
    #Generar una clave privada
    private_key = ec.generate_private_key(ec.SECP256R1())

    # Obtener la clave publica correspondiente
    public_key = private_key.public_key()

    #Convertir la contraseña del usuario a bytes
    password_bytes = password.encode('utf-8')

    # Serializar la clave privada en formato DER con encriptación
    encrypted_private_key_der = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password_bytes)
    )

    public_key_der = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Verificar existencia de carpetas
    os.makedirs('Data/ECDSA/Private-Keys', exist_ok=True)
    os.makedirs('Data/ECDSA/Public-Keys', exist_ok=True)
    os.makedirs('Data/ECDSA/Certificates', exist_ok=True)

    # Guardar las claves en archivos .key
    private_path = 'Data/ECDSA/Private-Keys'
    public_path = 'Data/ECDSA/Public-Keys'
    certificate_path = 'Data/ECDSA/Certificates'

    # Guardar los archivos en el servidor
    with open(f"{private_path}/{username}_encrypted_private_key.key",'wb') as key_file:
        key_file.write(encrypted_private_key_der)

    with open(f"{public_path}/{username}_public_key.key", 'wb') as key_file:
        key_file.write(public_key_der)


    # Crear el certificado
    issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, 'PIA-CRIPTOGRAFIA')
    ])
    # Construir el sujeto del certificado
    subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, name),
        x509.NameAttribute(NameOID.SURNAME, username),
        x509.NameAttribute(NameOID.EMAIL_ADDRESS, email)

    ])

    #Crear objeto de validez para el certificado
    valid_from = datetime.now()

    #Establecer la fecha de vencimiento
    # 31/12/9999 23:59:59
    valid_to = datetime(9999, 12, 31, 23, 59, 59)

    # Construir el certificado sin fecha de vencimiento
    builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(public_key)
        .serial_number(x509.random_serial_number())
        .not_valid_before(valid_from)
        .not_valid_after(valid_to)

    )

    #Firmar los datos del usuario
    certificate = builder.sign(
        private_key,
        hashes.SHA256()
    )

    certificate_bytes = certificate.public_bytes(encoding=serialization.Encoding.DER)

    with open(f"{certificate_path}/{username}_Certificate.cer", 'wb') as cer_file:
        cer_file.write(certificate_bytes)

