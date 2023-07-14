import requests
import json
import csv
from tqdm import tqdm


def get_company_data(company: str) -> dict:
    target = 'https://autocomplete.clearbit.com/v1/companies/suggest?query={}'.format(company)
    resp = requests.get(target)
    return json.loads(resp.text)


def read_companies_from(fname: str) -> list:
    with open(fname, 'r') as f:
        return [ln.strip() for ln in f.readlines()]


def extract_company_info(company: str) -> list:
    results = []

    data = get_company_data(company)
    for item in data:
        results.append({'domain': item['domain'], 'name': item['name']})

    return results


def write_results_to_csv(fname: str, results: list) -> None:
    with open(fname, 'w') as f:
        writer = csv.DictWriter(f, results[0].keys())
        writer.writeheader()
        writer.writerows(results)


def main() -> None:
    companies = read_companies_from('companies.txt')

    results = []
    progress_bar = tqdm(total=len(companies), desc='Processing')

    for c in companies:
        results += extract_company_info(c)
        progress_bar.update(1)

    progress_bar.close()

    write_results_to_csv('results.csv', results)


if __name__ == '__main__':
    main()

