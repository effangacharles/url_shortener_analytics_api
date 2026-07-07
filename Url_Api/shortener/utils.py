# shortener/utils.py
import secrets
import string

def generate_short_code(length=6):
    characters = string.digits + string.ascii_lowercase + string.ascii_uppercase
    short_code = ''.join(secrets.choice(characters) for _ in range(length))
    return short_code



def create_unique_slug(model_instance):
    ModelClass = model_instance.__class__
    
    while True:
     new_code = generate_short_code()
     if not ModelClass.objects.filter(short_code=new_code).exists():
            return new_code