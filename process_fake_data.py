import pandas as pd

df = pd.read_csv('fake_data.csv')

# Check for missing values
print(df.isnull().sum())

# Fill or remove missing values if any (for this generated data, there shouldn't be any)
df = df.dropna()  # or use df.fillna(method='ffill') for forward fill

# Normalize phone numbers (example: remove special characters)
df['phone_number'] = df['phone_number'].str.replace(r'\D', '', regex=True)

# Ensure birthdates are in 'YYYY-MM-DD' format
df['birthday'] = pd.to_datetime(df['birthday']).dt.strftime('%Y-%m-%d')

df.to_csv('preprocessed_fake_data.csv', index=False)