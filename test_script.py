import os
import json
import pytest
from pdf_to_json import get_data

# Directory containing your test PDFs
TEST_PDF_DIR = 'test_inputs'

# Directory containing expected output JSON files
EXPECTED_OUTPUT_DIR = 'test_outputs'

@pytest.fixture
def setup():
    if not os.path.exists(TEST_PDF_DIR):
        os.makedirs(TEST_PDF_DIR)
    if not os.path.exists(EXPECTED_OUTPUT_DIR):
        os.makedirs(EXPECTED_OUTPUT_DIR)

def test_pdf_scraping(setup):
    test_files = os.listdir(TEST_PDF_DIR)
    for test_file in test_files:
        if test_file.endswith('.pdf'):
            pdf_path = os.path.join(TEST_PDF_DIR, test_file)
            output = get_data(pdf_path)
            output_file = f"output-{test_file.replace('.pdf', '.json')}"
            expected_output_path = os.path.join(EXPECTED_OUTPUT_DIR, output_file)
            
            with open(expected_output_path, 'r') as f:
                expected_output = json.load(f)
            
            assert output == expected_output, f"Output for {test_file} did not match expected output."

if __name__ == "__main__":
    pytest.main(["-v", "-rA"])