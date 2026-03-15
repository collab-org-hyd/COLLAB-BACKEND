from passlib.context import CryptContext

# Password hashing context using argon2id (more modern and reliable than bcrypt)
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,  # 64MB
    argon2__parallelism=4,
    argon2__time_cost=2,
)


def hash_password(password: str) -> str:
    """Hash a password using argon2id
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    # Ensure password is a string
    if isinstance(password, bytes):
        password = password.decode('utf-8')
    
    password = str(password)
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    # Ensure passwords are strings
    if isinstance(plain_password, bytes):
        plain_password = plain_password.decode('utf-8')
    
    plain_password = str(plain_password)
    
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False
