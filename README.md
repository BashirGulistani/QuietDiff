# QuietDiff

QuietDiff compares two CSV/XLSX files and produces a clean diff you can share or automate.

## Install

### From source
pip install -e .

## Usage

### Basic
quietdiff old.xlsx new.xlsx --key "SKU"

### Multiple keys
quietdiff old.csv new.csv --key "loyalty_number" --key "order_id"

### Only compare specific columns
quietdiff a.xlsx b.xlsx --key "id" --include "status" --include "total" --include "email"

### Ignore columns
quietdiff a.xlsx b.xlsx --key "id" --ignore "updated_at" --ignore "last_seen"

### Numeric tolerance
quietdiff a.csv b.csv --key "id" --tolerance 0.01

### Fuzzy matching fallback (helps when keys shift slightly)
quietdiff a.csv b.csv --key "name" --fuzzy --fuzzy-threshold 0.92

### Output paths
quietdiff a.xlsx b.xlsx --key "SKU" --out-dir out/

## Outputs

- out/diff.json
- out/diff.csv
- out/report.html

## What it detects

- added rows
- removed rows
- changed rows (cell-level changes)
- duplicate keys in either file

## Exit codes

- 0: no changes
- 1: changes found
- 2: invalid input / errors

## License
MIT
# QuietDiff
