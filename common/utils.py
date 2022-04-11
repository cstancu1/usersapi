import random
import string

def gen_random_password(username):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(10))

def send_user_password(username, password):
    #TO BE REFACTORED
    #Will publish to queue
    print(f"sending email for user: {username} with password {password}")