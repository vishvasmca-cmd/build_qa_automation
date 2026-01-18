import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

class DataGenerator:
    """
    Generates dynamic test data based on placeholders.
    """
    
    GENERATORS = {
        "{{random_name}}": lambda: fake.name(),
        "{{random_email}}": lambda: fake.email(),
        "{{random_phone}}": lambda: fake.phone_number(),
        "{{random_username}}": lambda: f"user_{random.randint(1000, 9999)}",
        "{{random_password}}": lambda: f"Pass{random.randint(1000, 9999)}!",
        "{{random_address}}": lambda: fake.address(),
        "{{random_city}}": lambda: fake.city(),
        "{{random_zip}}": lambda: fake.zipcode(),
        "{{today}}": lambda: datetime.now().strftime("%Y-%m-%d"),
        "{{timestamp}}": lambda: str(int(datetime.now().timestamp())),
        "{{uuid}}": lambda: fake.uuid4(),
    }

    @classmethod
    def resolve(cls, value: str) -> str:
        if not isinstance(value, str):
            return value
            
        for placeholder, generator in cls.GENERATORS.items():
            if placeholder in value:
                value = value.replace(placeholder, generator())
        return value
