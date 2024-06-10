from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker
from cryptography.fernet import Fernet

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_anonymization_dag',
    default_args=default_args,
    description='A simple data anonymization DAG',
    schedule_interval=timedelta(days=1),
)

def generate_and_save_data():
    fake = Faker()
    num_records = 1000
    data = {
        'name': [fake.name() for _ in range(num_records)],
        'ssn': [fake.ssn() for _ in range(num_records)],
        'email': [fake.email() for _ in range(num_records)],
        'phone_number': [fake.phone_number() for _ in range(num_records)],
        'address': [fake.address() for _ in range(num_records)],
        'birthdate': [fake.date_of_birth().strftime('%Y-%m-%d') for _ in range(num_records)],
        'credit_card_number': [fake.credit_card_number() for _ in range(num_records)],
    }
    df = pd.DataFrame(data)
    df.to_csv('/tmp/preprocessed_fake_data.csv', index=False)

def anonymize_data():
    with open('/tmp/key.key', 'rb') as key_file:
        key = key_file.read()

    cipher_suite = Fernet(key)

    df = pd.read_csv('/tmp/preprocessed_fake_data.csv')

    def mask_data(column, mask_char='*'):
        return column.apply(lambda x: mask_char * len(x))

    def tokenize_data(column):
        return column.apply(lambda x: cipher_suite.encrypt(x.encode()).decode())

    df['name_masked'] = mask_data(df['name'])
    df['credit_card_number_masked'] = mask_data(df['credit_card_number'])
    df['ssn_tokenized'] = tokenize_data(df['ssn'])
    df['email_tokenized'] = tokenize_data(df['email'])

    df.to_csv('/tmp/anonymized_data.csv', index=False)

generate_data_task = PythonOperator(
    task_id='generate_and_save_data',
    python_callable=generate_and_save_data,
    dag=dag,
)

anonymize_data_task = PythonOperator(
    task_id='anonymize_data',
    python_callable=anonymize_data,
    dag=dag,
)

generate_data_task >> anonymize_data_task

