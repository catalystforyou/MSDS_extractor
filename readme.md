# Extracting MSDS from SMILES/English Name/CAS Number

## Dependency

- Python 3.7 or higher
- pip install pubchempy requests beautifulsoup4 pandas tqdm

## Usage

1. Typing the SMILES/English Name/CAS Number into the "msds_input.txt"(one molecule per line);
2. Run `python extract_msds.py` on the current folder;
3. The MSDS information will be extracted automatically into a csv file with timestamp;

## Tips

Sometimes there may be network issues, and when you see "403 Forbidden" in the output file, you can re-run the code to extract information for those failed molecules.

