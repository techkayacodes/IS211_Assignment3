import argparse
import csv
import re
import requests

def download_log_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open('web_log.csv', 'wb') as file:
            file.write(response.content)
            print("File downloaded successfully.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

# URL to the datafile
url = "http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv"

# Call the function to download the file
download_log_file(url)

def process_log_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            path, datetime_accessed, browser, status, request_size = row
            # Further processing based on the requirements

def search_for_image_hits(file_path):
    image_hits = 0
    total_hits = 0

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            path, _, _, _, _ = row
            if re.search(r'\.(jpg|gif|png)$', path, re.IGNORECASE):
                image_hits += 1
            total_hits += 1

    image_percentage = (image_hits / total_hits) * 100
    print(f"Image requests account for {image_percentage:.1f}% of all requests")

def find_most_popular_browser(file_path):
    browser_counts = {'Firefox': 0, 'Chrome': 0, 'Internet Explorer': 0, 'Safari': 0}

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            _, _, user_agent, _, _ = row
            if re.search(r'Firefox', user_agent):
                browser_counts['Firefox'] += 1
            elif re.search(r'Chrome', user_agent):
                browser_counts['Chrome'] += 1
            elif re.search(r'Internet Explorer', user_agent):
                browser_counts['Internet Explorer'] += 1
            elif re.search(r'Safari', user_agent):
                browser_counts['Safari'] += 1

    most_popular_browser = max(browser_counts, key=browser_counts.get)
    print(f"The most popular browser is {most_popular_browser}")

def main(url):
    print(f"Running main with URL = {url}...")
    file_path = download_log_file(url)
    process_log_file(file_path)
    search_for_image_hits(file_path)
    find_most_popular_browser(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)