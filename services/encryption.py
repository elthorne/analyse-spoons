import json
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a key from the password using Scrypt."""
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2 ** 14,
        r=8,
        p=1,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt_json_file(json_file: str, password: str, encrypted_file: str):
    """Encrypts a JSON file using the provided password."""
    # Read the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Convert the encrypted_data to a JSON string
    json_data = json.dumps(data).encode()

    # Generate a random salt
    salt = os.urandom(16)

    # Derive a key from the password
    key = derive_key(password, salt)

    # Generate a random nonce
    nonce = os.urandom(12)

    # Encrypt the encrypted_data
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, json_data, None)

    # Save the salt, nonce, and ciphertext to the encrypted file
    with open(encrypted_file, 'wb') as f:
        f.write(salt + nonce + ciphertext)


def decrypt_json_file(encrypted_file: str, password: str, decrypted_file: str):
    """Decrypts a JSON file using the provided password."""
    # Read the encrypted file
    with open(encrypted_file, 'rb') as f:
        file_data = f.read()

    # Extract the salt, nonce, and ciphertext
    salt = file_data[:16]
    nonce = file_data[16:28]
    ciphertext = file_data[28:]

    # Derive the key from the password
    key = derive_key(password, salt)

    # Decrypt the encrypted_data
    aesgcm = AESGCM(key)
    json_data = aesgcm.decrypt(nonce, ciphertext, None)

    # Convert the JSON string back to a dictionary
    data = json.loads(json_data.decode())

    # Write the decrypted encrypted_data to the output file
    with open(decrypted_file, 'w') as f:
        json.dump(data, f, indent=4)


def encrypt_all_files_in_directory(directory: str, password: str):
    """Encrypts all JSON files in the given directory."""
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = os.path.join(directory, filename)
            encrypted_file = os.path.join(directory, filename.replace(".json", ".enc"))
            encrypt_json_file(json_file, password, encrypted_file)
            print(f"Encrypted {json_file} to {encrypted_file}")


def decrypt_all_files_in_directory(input_directory: str, output_directory: str, password: str):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.endswith(".enc"):
            encrypted_file = os.path.join(input_directory, filename)
            decrypted_filename = filename.replace(".enc", ".json")
            decrypted_file = os.path.join(output_directory, decrypted_filename)

            decrypt_json_file(encrypted_file, password, decrypted_file)
            print(f"Decrypted {encrypted_file} to {decrypted_file}")
