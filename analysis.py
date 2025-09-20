import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the compressed dataset
file_path = 'accepted_2007_to_2018Q4.csv.gz'
try:
    df = pd.read_csv(file_path, compression='gzip', low_memory=False)
    print("Data loaded successfully.")
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found. Please check the file path.")

# List of columns to keep for analysis
columns_to_keep = [
    'loan_amnt', 'int_rate', 'term', 'installment', 'grade', 'sub_grade',
    'emp_title', 'emp_length', 'home_ownership', 'annual_inc', 'issue_d',
    'loan_status', 'purpose', 'title', 'zip_code', 'addr_state', 'dti',
    'earliest_cr_line', 'fico_range_low', 'fico_range_high',
    'inq_last_6mths', 'pub_rec', 'revol_util', 'total_acc', 'initial_list_status'
]

# Filter the DataFrame to keep only these columns
df = df[columns_to_keep].copy() # Use .copy() to avoid the Chained Assignment Warning

# Drop rows with missing values in critical columns
df.dropna(subset=['loan_status', 'issue_d'], inplace=True)

# Fill missing values in other columns
# Use a dictionary for cleaner and more robust filling
fill_values = {
    'emp_length': 'Unknown',
    'emp_title': 'Unknown',
}
df.fillna(fill_values, inplace=True)
df['revol_util'].fillna(df['revol_util'].median(), inplace=True)

# --- CORRECTED CODE BLOCK ---

# Convert `int_rate` and `revol_util` from string to float
for col in ['int_rate', 'revol_util']:
    if col in df.columns:
        # Step 1: Convert the column to string type to handle mixed data
        df[col] = df[col].astype(str)
        # Step 2: Replace '%' and convert to float
        df[col] = df[col].str.replace('%', '', regex=False)
        # Handle 'nan' strings that might appear after converting to string
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Convert `emp_length` from string to a numerical value
emp_map = {
    '< 1 year': 0, '1 year': 1, '2 years': 2, '3 years': 3,
    '4 years': 4, '5 years': 5, '6 years': 6, '7 years': 7,
    '8 years': 8, '9 years': 9, '10+ years': 10, 'Unknown': -1
}
df['emp_length'] = df['emp_length'].replace(emp_map)

# Create the binary 'is_default' column
df['is_default'] = np.where(df['loan_status'].isin(['Charged Off', 'Default']), 1, 0)

# Filter out loans that are still in progress
final_outcomes = ['Fully Paid', 'Charged Off', 'Default']
df = df[df['loan_status'].isin(final_outcomes)].copy()

# Convert `issue_d` to a proper datetime object
df['issue_d'] = pd.to_datetime(df['issue_d'], format='%b-%Y')

# Display the data types of the final DataFrame to confirm success
print("\n--- Final DataFrame Info ---")
df.info()
print("\n--- Sample of Cleaned Data ---")
print(df.head())


# Set plotting styles for better visuals
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Assuming your preprocessed DataFrame 'df' is already loaded
# and cleaned as per the previous steps.

# --- 1. Overall Loan Performance Analysis ---

print("--- Overall Loan Performance ---")

# Calculate the overall default rate
total_loans = df.shape[0]
total_defaults = df['is_default'].sum()
default_rate = (total_defaults / total_loans) * 100
print(f"Total Loans Analyzed: {total_loans:,}")
print(f"Overall Default Rate: {default_rate:.2f}%")

# Visualize the distribution of loan status
plt.figure(figsize=(8, 6))
sns.countplot(x='loan_status', data=df, palette='viridis')
plt.title('Distribution of Loan Status')
plt.xlabel('Loan Status')
plt.ylabel('Number of Loans')
plt.xticks(rotation=45)
plt.show()

# --- 2. Key Risk Factor Analysis ---

print("\n--- Key Risk Factor Analysis ---")

# a) Default Rate by Loan Grade
plt.figure(figsize=(10, 6))
grade_default_rate = df.groupby('grade')['is_default'].mean().sort_index()
sns.barplot(x=grade_default_rate.index, y=grade_default_rate.values, palette='coolwarm')
plt.title('Default Rate by Loan Grade')
plt.xlabel('Loan Grade')
plt.ylabel('Default Rate')
plt.show()

# b) Default Rate by Loan Purpose
plt.figure(figsize=(14, 6))
purpose_default_rate = df.groupby('purpose')['is_default'].mean().sort_values(ascending=False)
sns.barplot(x=purpose_default_rate.index, y=purpose_default_rate.values, palette='plasma')
plt.title('Default Rate by Loan Purpose')
plt.xlabel('Loan Purpose')
plt.ylabel('Default Rate')
plt.xticks(rotation=90)
plt.show()

# c) Default Rate by Employment Length
plt.figure(figsize=(10, 6))
emp_length_default_rate = df.groupby('emp_length')['is_default'].mean().sort_index()
sns.barplot(x=emp_length_default_rate.index, y=emp_length_default_rate.values, palette='magma')
plt.title('Default Rate by Employment Length (in Years)')
plt.xlabel('Employment Length')
plt.ylabel('Default Rate')
plt.show()

# d) Relationship between Interest Rate and Default Rate
plt.figure(figsize=(10, 6))
# Create bins for interest rates
bins = [0, 5, 10, 15, 20, 25, 30, 35]
df['int_rate_bin'] = pd.cut(df['int_rate'], bins=bins, right=False)
int_rate_default_rate = df.groupby('int_rate_bin')['is_default'].mean()
sns.barplot(x=int_rate_default_rate.index, y=int_rate_default_rate.values, palette='viridis')
plt.title('Default Rate by Interest Rate Bins')
plt.xlabel('Interest Rate (%)')
plt.ylabel('Default Rate')
plt.show()

# --- 3. Cohort Analysis ---

print("\n--- Cohort Analysis ---")

# Create a column for the loan issue month
df['issue_month'] = df['issue_d'].dt.to_period('M')

# Calculate the default rate per month
monthly_default_rate = df.groupby('issue_month')['is_default'].mean()

# Convert the monthly periods to timestamps for plotting
monthly_default_rate.index = monthly_default_rate.index.to_timestamp()

plt.figure(figsize=(15, 7))
monthly_default_rate.plot(kind='line', marker='o', linestyle='-', color='b')
plt.title('Default Rate Trend Over Time (by Issue Month)')
plt.xlabel('Issue Date')
plt.ylabel('Default Rate')
plt.show()