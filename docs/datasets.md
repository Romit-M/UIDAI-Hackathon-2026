# Aadhaar Dataset

## Source
- UIDAI public API
- Data downloaded on Jan 2026

## Files Included
- api_data_aadhar_enrolment_0_500000.csv
- api_data_aadhar_demographic_0_500000.csv
- api_data_aadhar_biometric_0_500000.csv

## Key Columns
- `state`: Name of the Indian state
- `district`: District name
- `date`: Date of record
- `enrolments`: Number of enrolments

## Known Data Issues
- Same state appears under multiple names
- District names are inconsistent

## Cleaning Strategy
- Canonical state mapping
- String normalization
- Pipeline-based preprocessing
