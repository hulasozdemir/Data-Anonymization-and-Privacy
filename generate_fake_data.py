import pandas as pd
from faker import Faker


fake = Faker()

def generate_fake_data(num_of_records):
    data = {
        'name': [fake.name() for _ in range(num_of_records)],
        'email': [fake.email() for _ in range(num_of_records)],
        'phone_number': [fake.phone_number() for _ in range(num_of_records)],
        'birthday': [fake.date_of_birth() for _ in range(num_of_records)],
        'ssn': [fake.ssn() for _ in range(num_of_records)],
        'credit_card_number': [fake.credit_card_number() for _ in range(num_of_records)],
    }

    return pd.DataFrame(data)

fake_data_df = generate_fake_data(100)

fake_data_df.to_csv('fake_data.csv', index=False)