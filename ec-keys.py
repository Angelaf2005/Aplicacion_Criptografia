#Genera llava publica y privada utilizando la curva eliptica NIST P-256
#para el algoritmo de encriptado asimetrico ECDSA
#El contenido de la clave esta en Base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

# Generar una clave privada
private_key = ec.generate_private_key(ec.SECP256R1())

# Obtener la clave pública correspondiente
public_key = private_key.public_key()

# Serializar las claves en formato PEM
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Imprimir las claves PEM
print("Clave privada:")
print(private_key_pem.decode('utf-8'))

print("\nClave pública:")
print(public_key_pem.decode('utf-8'))
