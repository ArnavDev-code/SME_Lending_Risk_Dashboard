# SME Lending Risk & Portfolio Performance Analytics

## Project Overview
This project is a comprehensive data analysis of over 2 million loans from LendingClub to identify key risk factors and trends in loan portfolio performance. The primary objective is to transform raw, unstructured data into actionable business intelligence, culminating in an interactive dashboard that provides insights for strategic decision-making in lending.

## Problem Statement
SME lending institutions face the critical challenge of managing risk and minimizing defaults. By analyzing historical loan data, we can uncover patterns and risk drivers that are not immediately obvious. This project addresses this challenge by providing a data-driven framework for understanding and mitigating risk.

## Methodology
The analysis follows a structured data analysis pipeline:

1.  **Data Acquisition & Cleaning:** The `accepted_2007_to_2018Q4.csv.gz` dataset from Kaggle was loaded and processed. This involved handling missing values, standardizing data types (e.g., converting strings with '%' to floats), and filtering out irrelevant columns.
2.  **Exploratory Data Analysis (EDA):** Performed an in-depth statistical analysis to understand the data's structure and relationships. Key analyses included:
    * **Overall Default Rate:** Calculated the portfolio's total default rate.
    * **Risk Factor Analysis:** Explored the relationship between loan defaults and key variables such as loan grade, purpose, and interest rate.
    * **Cohort Analysis:** Analyzed loan performance over time by issue date to identify long-term trends and shifts in portfolio quality.
3.  **Dashboard Development:** All findings were integrated into a professional, interactive dashboard to visualize key metrics, risk breakdowns, and time-series trends.

## Key Findings
* **Loan Grade is a Strong Predictor:** A clear correlation was found between lower loan grades (e.g., D, E, F) and significantly higher default rates.
* **Purpose-Driven Risk:** Loans for "small_business" and "debt_consolidation" showed a higher default risk compared to other purposes.
* **Time-Series Trends:** The monthly default rate exhibited fluctuations, providing valuable insight into periods of higher or lower risk within the portfolio.

## Technologies Used
* **Data Manipulation:** Python, Pandas, NumPy
* **Data Visualization:** Matplotlib, Seaborn, Power BI
* **Version Control:** Git, GitHub

## Project Files
* `analysis.py`: Contains all the Python code for data cleaning and EDA.
* `accepted_loans_cleaned.csv`: A cleaned and preprocessed version of the original dataset, ready for direct use in the dashboard.
