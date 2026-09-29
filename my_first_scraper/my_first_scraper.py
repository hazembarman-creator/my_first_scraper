import requests
from bs4 import BeautifulSoup
import csv

def request_github_trending(url):
    response = requests.get(url)
    return response.text

def extract(page):
    soup = BeautifulSoup(page, 'html.parser')
    return soup.find_all('article', class_='Box-row')  # Ensure this matches the current structure

def transform(html_repos):
    repositories = []
    for repo in html_repos:
        # Use safe navigation to prevent AttributeError
        try:
            developer_tag = repo.h1.find('a')
            if developer_tag is None:
                continue  # Skip if the developer tag is not found
            developer = developer_tag.text.strip()  # Developer name
            
            # Extract the repository name
            repository_name = developer_tag['href'].split('/')[-1]  # Repository name
            
            # Find the number of stars, safely
            stars_tag = repo.find('span', class_='Counter')
            nbr_stars = stars_tag.text.strip() if stars_tag else '0'  # Default to '0' if not found

            repositories.append({
                'developer': developer,
                'repository_name': repository_name,
                'nbr_stars': nbr_stars
            })
        except Exception as e:
            print(f"An error occurred: {e}")  # Log any errors for debugging
    return repositories

def format(repositories_data):
    csv_string = "Developer,Repository Name,Number of Stars\n"
    for repo in repositories_data:
        csv_string += f"{repo['developer']},{repo['repository_name']},{repo['nbr_stars']}\n"
    return csv_string

if __name__ == "__main__":
    url = "https://github.com/trending"
    page_content = request_github_trending(url)
    html_repos = extract(page_content)
    repositories_data = transform(html_repos)
    csv_output = format(repositories_data)

    # Write to CSV file
    with open('trending_repositories.csv', 'w') as f:
        f.write(csv_output)

    print("Data has been written to trending_repositories.csv")

import requests

def request_github_trending(url):
    try:
        response = requests.get(url, timeout=10)  # Set a timeout
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.exceptions.Timeout:
        print("Request timed out.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def extract(page):
    soup = BeautifulSoup(page, 'html.parser')
    return soup.find_all('article', class_='Box-row')[:5]  # Limit to 5 for testing
 
import socket

def check_internet():
    try:
        # Check if we can connect to a public DNS server
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False

if not check_internet():
    print("No internet connection.")

if __name__ == "__main__":
    url = "https://github.com/trending"
    print("Checking internet connection...")
    if not check_internet():
        print("No internet connection.")
    else:
        print("Fetching GitHub trending page...")
        page_content = request_github_trending(url)
        if page_content:
            print("Extracting repositories...")
            html_repos = extract(page_content)
            print("Transforming data...")
            repositories_data = transform(html_repos)
            print("Formatting data...")
            csv_output = format(repositories_data)
            print("Writing to CSV...")
            with open('trending_repositories.csv', 'w') as f:
                f.write(csv_output)
            print("Data has been written to trending_repositories.csv")
