import bcrypt

password = b"Admin@123"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed.decode())
