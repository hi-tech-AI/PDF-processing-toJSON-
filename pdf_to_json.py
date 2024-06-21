import os
import json
import camelot

def get_data(filepath):
    tables = camelot.read_pdf("./test_inputs/" + filepath, pages="all")
    all_data = None
    print(f"{filepath} => Total tables extracted:", tables.n)
    for table in tables:
        table = clean_table(table.df)
        if all_data is None:
            all_data = table
        else:
            # Find duplicate columns before merging
            duplicate_columns = set(all_data.columns).intersection(set(table.columns)) - {"Placement Name", "Main Material", "Product"}
            if duplicate_columns:
                print(f"Duplicate columns found: {duplicate_columns}")
                table = table.drop(columns=duplicate_columns)
            all_data = all_data.merge(table, on=["Placement Name", "Main Material", "Product"], suffixes=('_left', '_right'))
    return convert_to_json(all_data)

def clean_table(dataframe):
    dataframe = dataframe.loc[~dataframe[0].str.contains(r"\(Blanks\)|Displaying", na=False)]
    dataframe = dataframe.apply(lambda column: column.apply(lambda x: x.replace("\n", " ") if isinstance(x, str) else x), axis=1)
    dataframe.columns = dataframe.iloc[0].to_list()
    return dataframe.loc[1:]

def convert_to_json(dataframe):
    parsed_data = []
    for _, row in dataframe.iterrows():
        parsed_data.append(row.to_dict())
    return parsed_data

if __name__ == "__main__":
    files = ['old-1.pdf', 'old-2.pdf', 'old-3.pdf']
    for file in files:
        file_data = get_data(file)
        output_filename = f"./test_outputs/output-{file.replace('.pdf', '.json')}"
        with open(output_filename, "w") as f:
            json.dump(file_data, f, indent=4)