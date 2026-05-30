import random
from faker import Faker
from api.v1.src.constants import SYSTEMS_TYPES, SYSTEMS_STATUS

fake = Faker()


class AuthData:
    @property
    def get_auth_payload(self):
        return {
            "client_id": fake.uuid4()[:8],
            "client_secret": fake.password(length=12),
            "name": fake.company()
        }

    @staticmethod
    def make_login_payload(register_payload):
        return {
            "client_id": register_payload["client_id"],
            "client_secret": register_payload["client_secret"]
        }

    @property
    def get_login_wrong_payload(self):
        return {
            "client_id": "nonexistent",
            "client_secret": "wrong"
        }


class SystemsData:
    @property
    def create_system_payload(self):
        return {
          "name": f"{fake.word()} starship",
          "system_type": random.choice(SYSTEMS_TYPES),
          "status": random.choice(SYSTEMS_STATUS)
        }
