from faker import Faker

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
