# Extracting MSDS from SMILES/English Name/CAS Number

## Dependency

- Python 3.7 or higher
- pip install pubchempy requests beautifulsoup4 pandas tqdm

## Usage

1. Typing the SMILES/English Name/CAS Number into the "msds_input_${file}.txt"(one molecule per line);
2. Run `python extract_msds.py -f ${file}` on the current folder(the default file is msds_input_sample.txt);
3. The MSDS information will be extracted automatically into a csv file with timestamp;

## Tips

Sometimes easier molecules may not be extracted due to the webserver, and you may look up their MSDS information manually:)

## 文件及说明
- extract_msds.py: 主程序，请运行这个程序（python extract_msds.py -f ${file}, 例如python extract_msds.py -f 1204对应预测msds_1204_input.txt中的信息）。
- msds_input_sample.txt: 默认输入文件示例。
- msds_sample_output.csv: 默认输出文件示例。
- case_1204.docx: 实验中的一个真实案例，我们从中提取了五个化合物的CAS Number，并用本程序成功提取了MSDS信息，存放在msds_1204_output.csv中。
- msds_input_1204.txt: 上述案例的输入文件。
- msds_1204_output.csv: 上述案例的结果。