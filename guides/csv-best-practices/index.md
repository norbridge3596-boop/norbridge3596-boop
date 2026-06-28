---
layout: page
title: "Data Cleaning 101: CSV Best Practices"
subtitle: "Clean data is the foundation of every automation pipeline"
date: 2026-06-28
---

If you've worked with data for more than five minutes, you've encountered a messy CSV. Missing values, inconsistent formatting, duplicate rows, encoding nightmares — the list goes on.

Cleaning data isn't glamorous, but it's the most important step in any automation pipeline. Garbage in, garbage out. Here's how to do it right.

## Why Clean Data Matters

A clean dataset means:

- **Reliable results** — No surprises from malformed data
- **Faster processing** — Clean data processes consistently
- **Fewer bugs** — Edge cases are handled before they bite you
- **Better insights** — Your analysis is only as good as your data

## Common CSV Problems (And How to Fix Them)

### 1. Missing Values

CSV files often have empty cells. How you handle them depends on context:

```python
import pandas as pd

df = pd.read_csv('data.csv')

# Check for missing values
print(df.isnull().sum())

# Options:
# Drop rows with any missing values
df_clean = df.dropna()

# Fill with a specific value
df_clean = df.fillna('N/A')

# Forward fill (use previous value)
df_clean = df.ffill()

# Interpolate numeric values
df_clean = df.interpolate()
```

### 2. Duplicate Rows

Duplicates can silently skew your results:

```python
# Check for duplicates
duplicates = df.duplicated().sum()
print(f"Found {duplicates} duplicate rows")

# Remove duplicates (keep first occurrence)
df_clean = df.drop_duplicates()

# Remove duplicates based on specific columns
df_clean = df.drop_duplicates(subset=['email', 'id'])
```

### 3. Inconsistent Formats

Dates, numbers, and text often arrive in different formats:

```python
# Standardize dates
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Clean text fields
df['name'] = df['name'].str.strip().str.lower()

# Fix numeric columns
df['price'] = pd.to_numeric(df['price'], errors='coerce')
```

### 4. Encoding Issues

The dreaded `Ã©` instead of `é`:

```python
# Try different encodings
encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']

for encoding in encodings:
    try:
        df = pd.read_csv('data.csv', encoding=encoding)
        print(f"Success with {encoding}")
        break
    except UnicodeDecodeError:
        continue
```

## Automation-Ready Cleaning Pipeline

Here's a reusable cleaning function that handles the most common issues:

```python
import pandas as pd
import numpy as np

def clean_csv(input_path, output_path=None, config=None):
    """
    Automated CSV cleaning pipeline.
    
    Args:
        input_path: Path to input CSV
        output_path: Path for cleaned output (default: input_clean.csv)
        config: Optional config dict for custom rules
    
    Returns:
        Summary of cleaning operations performed
    """
    if config is None:
        config = {}
    
    # Read with auto-detection
    df = pd.read_csv(input_path, low_memory=False)
    report = {'rows_before': len(df), 'columns': list(df.columns)}
    
    # Remove completely empty rows
    df = df.dropna(how='all')
    
    # Strip whitespace from all string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    
    # Remove duplicates
    before_dedup = len(df)
    df = df.drop_duplicates()
    report['duplicates_removed'] = before_dedup - len(df)
    
    # Standardize dates
    date_cols = config.get('date_columns', [])
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Handle missing values
    null_strategy = config.get('null_strategy', 'drop')
    if null_strategy == 'drop':
        before_null = len(df)
        df = df.dropna()
        report['null_rows_removed'] = before_null - len(df)
    elif null_strategy == 'fill':
        df = df.fillna({
            col: config.get('fill_value', '') 
            for col in df.columns
        })
    
    # Save cleaned data
    if output_path is None:
        output_path = input_path.replace('.csv', '_clean.csv')
    
    df.to_csv(output_path, index=False)
    
    report['rows_after'] = len(df)
    report['output_path'] = output_path
    
    return report

# Usage
summary = clean_csv('messy_data.csv', config={
    'date_columns': ['created_at', 'updated_at'],
    'null_strategy': 'drop'
})
print(f"Cleaned: {summary['rows_after']} rows (removed {summary['rows_before'] - summary['rows_after']})")
```

## CSV Best Practices Checklist

### When Creating CSVs
- [ ] Use UTF-8 encoding
- [ ] Include header row with consistent column names
- [ ] Use commas only as delimiters (escape internal commas)
- [ ] Quote fields containing commas or newlines
- [ ] Use consistent date formats (ISO 8601: YYYY-MM-DD)
- [ ] Avoid empty rows and inline formatting

### When Processing CSVs
- [ ] Always check for encoding mismatches
- [ ] Validate against expected schema
- [ ] Log cleaning operations for audit trail
- [ ] Keep original files as backup
- [ ] Document any assumptions made during cleaning

## Tools That Help

Need to clean CSV files regularly? Check out the [CSV Cleaner tool](https://github.com/norbridge3596-boop/csv-cleaner) — it automates all of these steps and more.

<div class="affiliate-disclosure">
<strong>📚 Recommended Reading & Tools:</strong>
<ul>
  <li><a href="https://www.amazon.com/dp/1491957662?tag=norbridge-20" target="_blank" rel="nofollow sponsored">Python for Data Analysis (3rd Edition)</a> — The definitive guide to pandas</li>
  <li><a href="https://www.amazon.com/dp/1492041130?tag=norbridge-20" target="_blank" rel="nofollow sponsored">Data Pipelines Pocket Reference</a> — Building reliable data pipelines</li>
  <li><a href="https://www.amazon.com/dp/1492052965?tag=norbridge-20" target="_blank" rel="nofollow sponsored">Fundamentals of Data Engineering</a> — Broader data engineering concepts</li>
</ul>
</div>

---

*This guide contains affiliate links. As an Amazon Associate, I earn from qualifying purchases at no extra cost to you.*

*Tracking a complex data project? The [Build Log Template Pack]({{ '/store/' | relative_url }}) can help keep everything organized.*
