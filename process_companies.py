import json

def process_json(input_file, output_file):
    # Load the raw JSON file
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Extract the required information and flatten the JSON structure
    flat_data = []
    for result in data.get("results", []):
        for hit in result.get("hits", []):
            flat_entry = {
                "company_id": hit.get("id"),
                "company_name": hit.get("name"),
                "short_description": hit.get("one_liner"),
                "long_description": hit.get("long_description"),
                "batch": hit.get("batch"),
                "status": hit.get("status"),
                "subindustry": hit.get("subindustry")
            }
            flat_data.append(flat_entry)

    # Write the flattened JSON to an output file
    with open(output_file, 'w') as file:
        json.dump(flat_data, file, indent=4)

# Define the input and output file paths
input_file = 'yc-w24-companies.raw.json'
output_file = 'yc-w24-companies.flat.json'

# Run the process
process_json(input_file, output_file)

print(f'Processed data has been written to {output_file}')
