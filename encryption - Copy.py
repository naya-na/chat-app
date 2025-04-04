import rsa
import os

KEY_FOLDER = "keys"
PUBLIC_KEY_FILE = os.path.join(KEY_FOLDER, "public.pem")
PRIVATE_KEY_FILE = os.path.join(KEY_FOLDER, "private.pem")

# Function to generate RSA keys
def generate_keys():
    if not os.path.exists(KEY_FOLDER):
        os.makedirs(KEY_FOLDER)

    public_key, private_key = rsa.newkeys(2048)

    with open(PUBLIC_KEY_FILE, "wb") as pub_file:
        pub_file.write(public_key.save_pkcs1("PEM"))

    with open(PRIVATE_KEY_FILE, "wb") as priv_file:
        priv_file.write(private_key.save_pkcs1("PEM"))

    print("RSA Keys Generated!")

# Function to load RSA keys
def load_keys():
    if not os.path.exists(PUBLIC_KEY_FILE) or not os.path.exists(PRIVATE_KEY_FILE):
        generate_keys()

    with open(PUBLIC_KEY_FILE, "rb") as pub_file:
        public_key = rsa.PublicKey.load_pkcs1(pub_file.read())

    with open(PRIVATE_KEY_FILE, "rb") as priv_file:
        private_key = rsa.PrivateKey.load_pkcs1(priv_file.read())

    return public_key, private_key

# Function to encrypt messages
def encrypt_message(message, public_key):
    return rsa.encrypt(message.encode(), public_key)

# Function to decrypt messages
def decrypt_message(encrypted_message, private_key):
    return rsa.decrypt(encrypted_message, private_key).decode()

# Generate keys if not exists
if __name__ == "__main__":
    generate_keys()
