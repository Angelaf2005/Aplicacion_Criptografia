import random
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def code_generator():
    # Generar un codigo de 6 digitos (0-9)
    restore_code = ''.join(str(random.randint(0,9)) for _ in range(6))
    
    # Obtener el tiempo actual (inicio)
    start_time = time.time()

    # Devolver el codigo y el tiempo de inicio
    return restore_code, start_time




# Esta funcion se ejecutara una vez el usuario ingrese y envie el codigo.
def code_verify(code, restore_code, start_time):
    
    # Obtener el tiempo actual (final)
    end_time = time.time()

    # Verificar si han pasado mas de 60 segundos
    if end_time - start_time > 60:
        return False, "El codigo ha expirado."
    
    # Verificar si los codigos coinciden
    elif  code != restore_code:
        return False , "El codigo ingresado no es valido."
    
    # Si pasa las verificaciones, el codigo es valido
    else:
        return True, "El codigo es valido"




def send_email(email, restore_code):
    # Configurar los detalles del servidor SMTP (Outlook)
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587
    sender_email = "" # email remitente
    sender_password = "" # contraseña remitente

    # Crear un mensaje de correo electronico
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Codigo de recuperacion de contraseña"

    body = f"""¡Hola!

Has solicitado un código de recuperación de contraseña para tu cuenta:

Código de recuperación: {restore_code}

Por favor, utiliza este código dentro de los próximos 1 minutos para restablecer tu contraseña.

¡Gracias!

Equipo de soporte técnico
"""

    msg.attach(MIMEText(body, 'plain'))


    # Iniciar conexion SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Enviar el correo electronico
    server.send_message(msg)


    # Cerrar la conexión SMTP
    server.quit()

