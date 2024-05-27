import os
def cesar_encrypt(message, shift):
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            encrypted_message += chr(shifted)
        else:
            encrypted_message += char
    return encrypted_message


def cesar_decrypt(file_name):
    keys_directory = f"Data/Cesar/Keys/{file_name}"
    key_file_path = f"{keys_directory}/{file_name}_key.txt"
    notes_directory = f"Data/Cesar/Notes/{file_name}"
    note_file_path = f"{notes_directory}/{file_name}_note.txt"


    if not os.path.exists(note_file_path):
        return f"No se encontró una nota guardada para el usuario {file_name}."
    with open(note_file_path, "r") as f:
        encrypted_message = f.read()

    decrypted_message = cesar_encrypt(encrypted_message, -3)
    return decrypted_message

def save_note(message, file_name):
    mensaje = cesar_encrypt(message, 3)
    # Crear directorio si no existe

    # Guardar la clave en un archivo

    # Crear directorio si no existe
    notes_directory = f"Data/Cesar/Notes/{file_name}"
    os.makedirs(notes_directory, exist_ok=True)

    # Guardar el mensaje cifrado en un archivo
    with open(f"{notes_directory}/{file_name}_note.txt", "w") as f:
        f.write(mensaje)
def read_encrypted_cesar_notes(file_name):
    notes_directory = f"Data/Cesar/Notes/{file_name}"
    
    if not os.path.exists(notes_directory):
        return f"No se encontraron notas encriptadas para el usuario {file_name}."
    for filename in os.listdir(notes_directory):
        if filename.endswith('_note.txt'):
            note_file_path = os.path.join(notes_directory, filename)
            with open(note_file_path, "r") as f:
                encrypted_message = f.read().strip()
                return encrypted_message
        else:
            return f"No se encontraron notas encriptadas para el usuario {file_name}"