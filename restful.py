#!/usr/bin/env python3

import argparse
import requests
import json
import csv

class RestfulClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def _handle_response(self, response):
        print(f"HTTP Status Code: {response.status_code}")
        if not response.ok:
            print(f"Error: {response.text}")
            exit(1)

    def get_data(self, endpoint):
        # print(endpoint)
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url)
        self._handle_response(response)
        return response.json()

    def post_data(self, endpoint, data):
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=json.loads(data), headers=headers)
        self._handle_response(response)
        return response.json()

    def dump_to_stdout(self, data):
        print(json.dumps(data, indent=2))

    def dump_to_json_file(self, data, filename):
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)

    def dump_to_csv_file(self, data, filename):
        keys = data[0].keys()
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

def parse_args():
    parser = argparse.ArgumentParser(description="Simple command-line REST client for JSONPlaceholder.")
    parser.add_argument("method", choices=["get", "post"], help="Request method")
    parser.add_argument("endpoint", help="Request endpoint URI fragment")
    parser.add_argument("-d", "--data", help="Data to send with request")
    parser.add_argument("-o", "--output", help="Output to .json or .csv file (default: dump to stdout)")

    return parser.parse_args()

def main():
    base_url = "https://jsonplaceholder.typicode.com"
    args = parse_args()

    rest_client = RestfulClient(base_url)

    if args.method == "get":
        response_data = rest_client.get_data(args.endpoint)
    elif args.method == "post":
        if not args.data:
            print("Error: -d/--data is required for the post method.")
            exit(1)
        response_data = rest_client.post_data(args.endpoint, args.data)

    if args.output:
        if args.output.endswith(".json"):
            rest_client.dump_to_json_file(response_data, args.output)
        elif args.output.endswith(".csv"):
            if isinstance(response_data, list) and response_data:
                rest_client.dump_to_csv_file(response_data, args.output)
            else:
                print("Error: Cannot dump non-list data to CSV.")
                exit(1)
        else:
            print("Error: Output file format not supported. Please use .json or .csv.")
            exit(1)
    else:
        rest_client.dump_to_stdout(response_data)

if __name__ == "__main__":
    main()
