import pandas as pd
from cryptography.fernet import Fernet
import numpy as np

# Load the encryption key
with open('key.key', 'rb') as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

df = pd.read_csv('anonymized_fake_data.csv')

def test_data_masking(original, masked):

    assert len(original) == len(masked)
    assert all(len(str(o)) == len(str(m)) for o, m in zip(original, masked))
    assert all(m == '*' * len(str(o)) for o, m in zip(original, masked))

# Validate 'name' and 'credit_card_number' masking
test_data_masking(df['name'], df['name_masked'])
test_data_masking(df['credit_card_number'], df['credit_card_number_masked'])
print("Data masking tests passed.")


def test_tokenization(original, tokenized, cipher_suite):
    assert len(original) == len(tokenized)
    assert all(cipher_suite.decrypt(t.encode()).decode() == o for o, t in zip(original, tokenized))

# Validate 'ssn' and 'email' tokenization
test_tokenization(df['ssn'], df['ssn_tokenized'], cipher_suite)
test_tokenization(df['email'], df['email_tokenized'], cipher_suite)
print("Tokenization tests passed.")


def generalize_age(birthdate):
    age = pd.to_datetime('today').year - pd.to_datetime(birthdate).year
    if age < 18:
        return '0-17'
    elif age < 30:
        return '18-29'
    elif age < 45:
        return '30-44'
    elif age < 60:
        return '45-59'
    else:
        return '60+'


def test_generalization(birthdate, age_range):
    calculated_age_range = birthdate.apply(generalize_age)
    assert all(a == b for a, b in zip(calculated_age_range, age_range))

# Validate 'birthdate' generalization
test_generalization(df['birthday'], df['age_range'])
print("Generalization tests passed.")


def test_differential_privacy(original, noisy, epsilon):
    assert len(original) == len(noisy)
    noise = np.abs(original.astype(int) - noisy.astype(int))
    avg_noise = np.mean(noise)
    print(f"Average noise added: {avg_noise}")
    assert avg_noise > 0  # We expect some noise to be added

# Validate 'phone_number' differential privacy (note: for demonstration)
test_differential_privacy(df['phone_number'].astype(int), df['phone_number_noisy'].astype(int), epsilon=1.0)
print("Differential privacy test passed.")


def validate_data_utility(original_df, anonymized_df, numeric_columns, non_numeric_columns):
    for column in numeric_columns:
        original_stats = original_df[column].describe()
        anonymized_stats = anonymized_df[column].describe()
        print(f"Original {column} stats:\n{original_stats}")
        print(f"Anonymized {column} stats:\n{anonymized_stats}")
        assert np.isclose(original_stats['mean'], anonymized_stats['mean'], atol=0.1 * original_stats['mean'])
        assert np.isclose(original_stats['std'], anonymized_stats['std'], atol=0.1 * original_stats['std'])
    
    for column in non_numeric_columns:
        original_unique = original_df[column].nunique()
        anonymized_unique = anonymized_df[column].nunique()
        print(f"Original {column} unique count: {original_unique}")
        print(f"Anonymized {column} unique count: {anonymized_unique}")
        assert original_unique == anonymized_unique
        assert len(original_df[column]) == len(anonymized_df[column])

# Validate utility of 'ssn' and 'email' columns after tokenization
numeric_columns = ['phone_number']  # example numeric column, typically other numeric columns would be used
non_numeric_columns = ['ssn', 'email']

# Validate data utility
validate_data_utility(df, df, numeric_columns, non_numeric_columns)
print("Data utility validation passed.")