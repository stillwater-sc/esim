{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Data Exploration Notebook\n",
    "\n",
    "## Project: Customer Behavior Analysis\n",
    "\n",
    "### Objective\n",
    "Perform initial exploratory data analysis on customer transaction data to understand key insights and prepare for further analysis."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Import essential libraries\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# Set up visualization styles\n",
    "plt.style.use('seaborn')\n",
    "sns.set(font_scale=1.2)\n",
    "\n",
    "# Suppress warnings\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')"
   ],
   "outputs": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Load the dataset\n",
    "# Replace 'customer_transactions.csv' with your actual data file\n",
    "df = pd.read_csv('customer_transactions.csv')\n",
    "\n",
    "# Display basic information about the dataset\n",
    "print(\"Dataset Information:\")\n",
    "print(df.info())\n",
    "\n",
    "# Show first few rows\n",
    "print(\"\\nFirst 5 Rows:\")\n",
    "print(df.head())"
   ],
   "outputs": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Check for missing values\n",
    "print(\"Missing Values:\")\n",
    "print(df.isnull().sum())\n",
    "\n",
    "# Basic statistical description\n",
    "print(\"\\nStatistical Description:\")\n",
    "print(df.describe())"
   ],
   "outputs": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Data Cleaning\n",
    "# Example: Remove rows with missing values\n",
    "df_cleaned = df.dropna()\n",
    "\n",
    "# Example: Convert date columns\n",
    "# Modify as per your actual date column names\n",
    "df_cleaned['transaction_date'] = pd.to_datetime(df_cleaned['transaction_date'])\n",
    "\n",
    "# Example: Create additional features\n",
    "df_cleaned['transaction_month'] = df_cleaned['transaction_date'].dt.to_period('M')\n",
    "df_cleaned['transaction_day_of_week'] = df_cleaned['transaction_date'].dt.day_name()"
   ],
   "outputs": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Visualization: Distribution of Numeric Variables\n",
    "plt.figure(figsize=(15, 5))\n",
    "\n",
    "# Example numeric columns - modify based on your dataset\n",
    "numeric_cols = ['transaction_amount', 'customer_age']\n",
    "\n",
    "for i, col in enumerate(numeric_cols, 1):\n",
    "    plt.subplot(1, len(numeric_cols), i)\n",
    "    sns.histplot(df_cleaned[col], kde=True)\n",
    "    plt.title(f'Distribution of {col}')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ],
   "outputs": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Categorical Variable Analysis\n",
    "plt.figure(figsize=(15, 5))\n",
    "\n",
    "# Example categorical columns - modify based on your dataset\n",
    "cat_cols = ['customer_segment', 'product_category']\n",
    "\n",
    "for i, col in enumerate(cat_cols, 1):\n",
    "    plt.subplot(1, len(cat_cols), i)\n",
    "    df_cleaned[col].value_counts().plot(kind='bar')\n",
    "    plt.title(f'Distribution of {col}')\n",
    "    plt.xticks(rotation=45)\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ],
   "outputs": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Correlation Analysis\n",
    "# Select only numeric columns\n",
    "numeric_df = df_cleaned.select_dtypes(include=[np.number])\n",
    "\n",
    "plt.figure(figsize=(10, 8))\n",
    "sns.heatmap(\n",
    "    numeric_df.corr(), \n",
    "    annot=True, \n",
    "    cmap='coolwarm', \n",
    "    linewidths=0.5,\n",
    "    fmt='.2f',\n",
    "    square=True\n",
    ")\n",
    "plt.title('Correlation Heatmap of Numeric Variables')\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ],
   "outputs": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Time Series Analysis (if applicable)\n",
    "# Group data by month and aggregate\n",
    "monthly_sales = df_cleaned.groupby('transaction_month')['transaction_amount'].sum()\n",
    "\n",
    "plt.figure(figsize=(12, 5))\n",
    "monthly_sales.plot(kind='line', marker='o')\n",
    "plt.title('Monthly Transaction Amount')\n",
    "plt.xlabel('Month')\n",
    "plt.ylabel('Total Transaction Amount')\n",
    "plt.show()"
   ],
   "outputs": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Key Insights and Next Steps\n",
    "\n",
    "1. Data Completeness:\n",
    "   - Assess missing values and their impact\n",
    "   - Consider imputation strategies if needed\n",
    "\n",
    "2. Distribution Analysis:\n",
    "   - Identify skewness in numeric variables\n",
    "   - Note any outliers or unusual patterns\n",
    "\n",
    "3. Categorical Insights:\n",
    "   - Understand distribution of categories\n",
    "   - Potential for segmentation analysis\n",
    "\n",
    "4. Correlation Observations:\n",
    "   - Identify potential feature relationships\n",
    "   - Consider feature engineering\n",
    "\n",
    "### Recommended Follow-up Actions:\n",
    "- Detailed feature engineering\n",
    "- Advanced statistical testing\n",
    "- Prepare data for machine learning models"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
