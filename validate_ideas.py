import enum
import json
import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    logging.info("Read JSON data from file.")
    return data

def make_request_1(audience, product):
    url = 'https://xhkl-v10v-x6df.n7c.xano.io/api:-DstEoh_/free/validation_main'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'origin': 'https://founderpal.ai',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }
    payload = {
        "audience": audience,
        "product": product
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    logging.info(f"Request 1 completed with audience: {audience} and product: {product}")
    return response.json()

def make_request_2(key):
    url = f'https://xhkl-v10v-x6df.n7c.xano.io/api:-DstEoh_/free/get_validation?key={key}'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'origin': 'https://founderpal.ai',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    logging.info(f"Request 2 completed with key: {key}")
    return response.json()

def process_response(data, response_2):
    audit = json.loads(response_2["audit"])
    data["ideaValidatorSummary"] = audit.get("summary")

    scores = [int(audit.get("priority_score")), int(audit.get("consequences_score")), int(audit.get("budget_score")), int(audit.get("competition_score")), int(audit.get("marketing_score")), int(audit.get("differentiation_score"))]
    average_score = sum(scores) / len(scores)
    data["ideaValidatorScore"] = average_score

    # Add all scores and texts to the data
    data["priority_score"] = audit.get("priority_score")
    data["priority_text"] = audit.get("priority_text")
    data["consequences_score"] = audit.get("consequences_score")
    data["consequences_text"] = audit.get("consequences_text")
    data["budget_score"] = audit.get("budget_score")
    data["budget_text"] = audit.get("budget_text")
    data["competition_score"] = audit.get("competition_score")
    data["competition_text"] = audit.get("competition_text")
    data["marketing_score"] = audit.get("marketing_score")
    data["marketing_text"] = audit.get("marketing_text")
    data["differentiation_score"] = audit.get("differentiation_score")
    data["differentiation_text"] = audit.get("differentiation_text")

    logging.info("Processed response and updated data.")
    return data

def save_json(data, idx):
    file_path = f'results/intermediate_results.{idx}.json'
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    logging.info(f"Saved JSON data to {file_path}")

def main(input_file, output_file):
    companies_data = read_json(input_file)
    updated_data = []

    for idx, company in enumerate(companies_data):
        logging.info(f"Processing company: {company['company_name']}")

        audience = company["subindustry"]
        product = company["long_description"]

        key = make_request_1(audience, product)
        validation_data = make_request_2(key)

        company = process_response(company, validation_data)
        updated_data.append(company)

        save_json(company, idx)  # Save intermediate results

    save_json(updated_data, 'full')  # Save final results

if __name__ == "__main__":
    input_file = 'yc-w24-companies.flat.json'
    output_file = 'results/yc-w24-companies.updated.json'
    main(input_file, output_file)
