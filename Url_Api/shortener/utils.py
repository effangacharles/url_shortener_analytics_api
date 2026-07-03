# shortener/utils.py
import secrets
import string

def generate_short_code(length=6):
    """
    Generates a secure, random alphanumeric short code using Base62.
    Using 'secrets' instead of 'random' ensures cryptographically 
    secure tokens that are harder to predict.
    """
    # 0-9 + a-z + A-Z (Total 62 characters)
    characters = string.digits + string.ascii_lowercase + string.ascii_uppercase
    
    # Securely pick random characters and join them
    short_code = ''.join(secrets.choice(characters) for _ in range(length))
    return short_code

# shortener/utils.py (Continued)

def create_unique_slug(model_instance):
    """
    Loops to find a completely unique short code if a collision occurs.
    """
    # Get the model class dynamically (avoids circular import issues)
    ModelClass = model_instance.__class__
    
    while True:
        # 1. Generate a candidate code
        new_code = generate_short_code()
        
        # 2. Check if it already exists in the database
        if not ModelClass.objects.filter(short_code=new_code).exists():
            return new_code