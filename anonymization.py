import pandas as pd

df = pd.read_csv('preprocessed_fake_data.csv')

def mask_data(column, mask_char='*'):
    return column.apply(lambda x: mask_char * len(str(x)))


# Mask the 'name' and 'credit_card_number' columns
df['name_masked'] = mask_data(df['name'])
df['credit_card_number_masked'] = mask_data(df['credit_card_number'])

# Tokenization

from cryptography.fernet import Fernet

# Generate encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

with open('key.key', 'wb') as key_file:
    key_file.write(key)

# Tokenization function
def tokenize_data(column):
    return column.apply(lambda x: cipher_suite.encrypt(x.encode()).decode())

# Tokenize the 'ssn' and 'email' columns
df['ssn_tokenized'] = tokenize_data(df['ssn'])
df['email_tokenized'] = tokenize_data(df['email'])

# Generalization function for birthday to age range
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

# Apply generalization to 'birthday' column
df['age_range'] = df['birthday'].apply(generalize_age)



from diffprivlib.mechanisms import Laplace

# Differential privacy function for numerical data
def add_noise(column, epsilon):
    mech = Laplace(epsilon=epsilon, sensitivity=1)
    return column.apply(lambda x: mech.randomise(x))

# Add noise to the 'phone_number' column (note: normally you wouldn't add noise to phone numbers; this is just for demonstration)
df['phone_number_noisy'] = add_noise(df['phone_number'].astype(int), epsilon=1.0)


df.to_csv('anonymized_fake_data.csv', index=False)

