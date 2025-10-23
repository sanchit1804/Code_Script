import pandas as pd # type: ignore
from ydata_profiling import ProfileReport
import os
import argparse

# Default input/output
DEFAULT_INPUT = 'data.csv'
DEFAULT_OUTPUT = 'report.html'

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate HTML EDA report from CSV")
parser.add_argument("--input", "-i", default=DEFAULT_INPUT, help="Path to CSV file")
parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help="Path to save HTML report")
args = parser.parse_args()

input_path = args.input
output_path = args.output

# Check input file exists
if not os.path.exists(input_path):
    print(f"Input file '{input_path}' not found.")
    exit(1)

# Read CSV and generate report
df = pd.read_csv(input_path)
profile = ProfileReport(df, title="Automated EDA Report", explorative=True)
os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
profile.to_file(output_path)

print(f"✅ Report generated: {output_path}")
