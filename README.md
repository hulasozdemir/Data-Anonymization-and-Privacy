# Data Anonymization and Privacy Framework

## Overview
This project demonstrates the implementation of various data anonymization techniques to protect sensitive information while preserving data utility. The techniques used include data masking, tokenization, generalization, and differential privacy.

## Data Flow
This document outlines the flow of data through the anonymization pipeline, detailing each transformation step from raw data to the final anonymized state.

## 1. Data Generation
- **Source**: Fake data generated using the `faker` library.
- **Data Fields**: 
  - `name`
  - `ssn`
  - `email`
  - `phone_number`
  - `address`
  - `birthdate`
  - `credit_card_number`

## 2. Data Preprocessing
- **Steps**:
  - Load data into a DataFrame.
  - Handle missing values (none expected in generated data).
  - Normalize data formats (e.g., phone numbers, dates).

## 3. Data Anonymization
- **Techniques**:
  - **Data Masking**: Applied to `name` and `credit_card_number`.
  - **Tokenization**: Applied to `ssn` and `email` using `cryptography.fernet`.
  - **Generalization**: Applied to `birthdate` to create age ranges.
  - **Differential Privacy**: Added noise to `phone_number` (for demonstration).

## 4. Data Validation
- **Validation Steps**:
  - Verify masking length and consistency.
  - Check tokenization decryption correctness.
  - Ensure generalized age ranges are accurate.
  - Confirm noise added by differential privacy is within acceptable bounds.

## 5. Data Storage
- **Files**:
  - `preprocessed_fake_data.csv`: Contains the final anonymized dataset.
  - `key.key`: Stores the encryption key used for tokenization.

## 6. Data Utility
- **Validation**:
  - Ensure aggregate statistics (e.g., mean, std) for numeric columns are preserved.
  - Verify count and uniqueness for non-numeric columns.


## Project Structure
- `main.py`: Main script to generate and preprocess fake data, and apply anonymization techniques.
- `test_anonymization.py`: Script to validate the anonymization techniques.
- `key.key`: File storing the encryption key for tokenization.
- `preprocessed_fake_data.csv`: Sample dataset with preprocessed and anonymized data.

## Setup Instructions
1. Clone the repository:
2. Install requirements: `pip install -r requirements.txt`
3. Generate fake data: `python generate_fake_data.py`
4. Process fake data: `python process_fake_data.py`
5. Anonymize data: `python anonymization.py`
6. Run the test script to validate anonymization techniques: `python validate_and_test.py`