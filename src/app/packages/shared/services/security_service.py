from passlib.context import CryptContext
from .service import Service

current_user_id: int = 0

class SecurityService(Service):
    crypt_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
    )

    def check_password(self, ci:int, password:str) -> bool:
        encrypted_text = self._get_user_pwd(ci)
        return self.crypt_context.verify(password,  encrypted_text)

    def encrypt(self, text: str) -> str:
        return self.crypt_context.hash(text)

    def _get_user_pwd(self, ci: int) -> str:
        global current_user_id

        query = f'''SELECT id, password FROM users WHERE ci={ci}'''
        
        result = self._read_query_fetchone(query)
        current_user_id = result["id"]
        
        return result["password"]