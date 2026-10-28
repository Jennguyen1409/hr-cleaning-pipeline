
import pandas as pd
import logging
import os

os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def extract_data(file_path):
    """Read the raw CSV file"""
    print(f"📂 Reading file: {file_path}")
    df = pd.read_csv(file_path)
    logging.info(f"Data extracted successfully. Rows: {len(df)}")
    print(f"Extracted {len(df)} rows")
    print(f"Columns: {len(df.columns)}")
    return df
    
def clean_data(df):
    """Clean the data: remove duplicates, fill missing values"""
    
    print("🧹 Starting cleaning process...")
    
    # 1. Remove duplicates
    df = df.drop_duplicates()
    logging.info(f"Duplicates removed. Rows: {len(df)}")
    print(f"After removing duplicates: {len(df)} rows")
    
    # 2. Fill missing values
    # Fill text columns with 'Unknown'
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna('Unknown')
    
    # Fill numeric columns with 0
    for col in df.select_dtypes(include=['number']).columns:
        df[col] = df[col].fillna(0)
    
    logging.info("Missing values filled")
    print("Missing values filled")
    
    # 3. Clean text columns (strip whitespace)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
    
    print("Text columns cleaned")
    return df

def validate_data(df):
    """Validate data: filter out invalid rows"""
    
    print("🔍 Starting validation...")
    
    # 1. Remove negative values in numeric columns
    for col in df.select_dtypes(include=['number']).columns:
        before = len(df)
        df = df[df[col] >= 0]
        removed = before - len(df)
        if removed > 0:
            logging.info(f"Removed {removed} rows with negative {col}")
            print(f"Removed {removed} rows with negative {col}")
    
    # 2. Drop rows with any null values (if any remain)
    before = len(df)
    df = df.dropna()
    removed = before - len(df)
    if removed > 0:
        logging.info(f"Removed {removed} rows with null values")
        print(f"Removed {removed} rows with null values")
    
    print(f"Validated data. Rows: {len(df)}")
    return df

def generate_report(df_original, df_final):
    """Generate a data quality report"""
    
    report = f"""
    ============================================
    DATA QUALITY REPORT
    ============================================
    Original rows: {len(df_original)}
    Final rows: {len(df_final)}
    Rows removed: {len(df_original) - len(df_final)}
    
    Columns: {', '.join(df_final.columns)}
    
    Data quality checks completed:
    - Duplicates removed
    - Missing values filled
    - Text columns cleaned (whitespace removed)
    - Negative values filtered out
    - Null values removed
    ============================================
    """
    
    with open('data/quality_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    logging.info("Data quality report generated")
    print("Data quality report saved to data/quality_report.txt")

def save_data(df):
    """Save the cleaned data to CSV"""
    df.to_csv('data/clean_data.csv', index=False)
    logging.info(f"Clean data saved. Rows: {len(df)}")
    print(f"💾 Saved {len(df)} rows to clean_data.csv")
    
def run_pipeline():
    print("=" * 60)
    print("🧹 STARTING LARGE DATA CLEANING PIPELINE")
    print("=" * 60)
    
    file_path = 'data/raw_data.csv'
    
    df_original = extract_data(file_path)
    df_cleaned = clean_data(df_original)
    df_validated = validate_data(df_cleaned)
    save_data(df_validated)
    generate_report(df_original, df_validated)
    
    print("=" * 60)
    print("PIPELINE COMPLETE!")
    print("=" * 60)
    logging.info("Cleaning pipeline executed successfully")

if __name__ == "__main__":
    run_pipeline()
