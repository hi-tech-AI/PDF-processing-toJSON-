# Table Extraction from PDF to JSON

This Python script extracts data from a PDF file, splits it into multiple parts, processes the tables within the PDFs, and generates a JSON file with the final results.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.x.
- You have installed the required Python libraries (See [Installation](#installation)).

## Installation

1. Clone the repository or download the script files.

2. Install the required Python packages using `pip`:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Place your PDF file in the same directory as the script.

2. Run the script:
    ```sh
    python pdf_to_json.py
    ```

3. Input the name of the PDF file when prompted (e.g., `new-sample.pdf`).

4. The script will process the PDF, split it into parts, extract table data, clean it, and generate a final JSON file named `final_output.json`.

## How It Works

### Splitting the PDF

The `split_pdf` function splits the input PDF into smaller PDF files, each containing two pages.

### Extracting Data

The `get_data` function reads the tables from each PDF part using Camelot, cleans the data, and merges them while handling duplicate columns.

### Cleaning Table Data

The `clean_table` function performs the following operations on the extracted tables:
- Removes rows that contain specific unwanted patterns.
- Replaces newline characters within cells.
- Sets the first row as the header.

### Converting to JSON

The `convert_to_json` function converts the cleaned table data into a dictionary format.

### Generating Final JSON Structure

The `get_final_json` function organizes the extracted data based on a specified structure and consolidates it into a final JSON result.

## Example

```json
[
    {
        "Placement Name 1": [
            {"field1": "value1", "field2": "value2"},
            {"field1": "value3", "field2": "value4"}
        ]
    },
    {
        "Placement Name 2": [
            {"field1": "value5", "field2": "value6"},
            {"field1": "value7", "field2": "value8"}
        ]
    }
]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to modify this README as per your project's requirements. If you have any questions or need further assistance, please let me know!