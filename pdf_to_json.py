import os
import json
import camelot
import PyPDF2

OUTPUT_FILE = "output.json"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_data(filepath):
    tables = camelot.read_pdf(filepath, pages="all")
    all_data = None
    print(f"{filepath} => Total tables extracted:", tables.n)

    for table in tables:
        table = clean_table_plan(table.df)
        if all_data is None:
            all_data = table
        else:
            # Find duplicate columns before merging
            duplicate_columns = set(all_data.columns).intersection(set(table.columns)) - {"Placement Name", "Main Material", "Product"}
            if duplicate_columns:
                print(f"Duplicate columns found: {duplicate_columns}")
                table = table.drop(columns=duplicate_columns)
            all_data = all_data.merge(table, suffixes=('_left', '_right'))

    return convert_to_json(all_data)

def split_pdf(file_path, output_prefix):
    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfFileReader(pdf_file)
        total_pages = reader.numPages

        output_list = []
        for start_page in range(0, total_pages, 2):
            writer = PyPDF2.PdfFileWriter()
            
            for page_num in range(start_page, min(start_page + 2, total_pages)):
                writer.addPage(reader.getPage(page_num))
            
            output_filename = f"{output_prefix}_part_{start_page//2 + 1}.pdf"
            output_list.append(output_filename)
            with open(output_filename, 'wb') as output_pdf:
                writer.write(output_pdf)
    print("Separated PDF file")
    return output_list

def clean_table_plan(dataframe):
    dataframe = dataframe.loc[~dataframe[0].str.contains(r"\(Blanks\)|Displaying", na=False)]
    dataframe = dataframe.apply(lambda column: column.apply(lambda x: x.replace("\n", " ") if isinstance(x, str) else x), axis=1)
    dataframe.columns = dataframe.iloc[0].to_list()
    return dataframe.loc[1:]

def convert_to_json(dataframe):
    parsed_data = []
    for _, row in dataframe.iterrows():
        parsed_data.append(row.to_dict())
    return parsed_data

def has_specified_structure(elem):
    return all(
        isinstance(value, str) and (value == "" or (key == "Placement Name" and value))
        for key, value in elem.items()
    )

def get_final_json(json_data):
    find_item_list = []
    for item_index, item in enumerate(json_data):
        if has_specified_structure(item):
            find_item_list.append({"item_index" : item_index, "item" : item["Placement Name"]})

    final_result = []
    for item_index, item in enumerate(find_item_list):
        if item_index == len(find_item_list) - 1:
            final_result.append({
                f"{item['item']}" : [element for element in json_data[int(item["item_index"] + 1):]]
            })
        else:
            final_result.append({
                f"{item['item']}" : [element for element in json_data[int(item["item_index"] + 1) : int(find_item_list[item_index + 1]["item_index"])]]
            })

    print("Generated final JSON file.")   
    return final_result

if __name__ == "__main__":
    pdf_file = input("Please input PDF file name(i.e. new-sample.pdf) : ")
    
    output_list = split_pdf(pdf_file, 'output')

    initial_result = []
    for file in output_list:
        file_data = get_data(file)
        output_filename = f"output-{pdf_file.replace('.pdf', '.json')}"
        for item in file_data:
            initial_result.append(item)
        os.remove(file)

    final_result = get_final_json(initial_result)
    
    with open("final_output.json", "w") as data:
        json.dump(final_result, data, indent=4)