import os
import requests
from dotenv import load_dotenv
import argparse

def fetch_all_repos(token):
    """
    Fetches all repositories for the authenticated user, handling pagination.
    """
    repos = []
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    params = {
        "per_page": 100,
        "page": 1,
        "type": "owner" # Only fetch repos owned by the user
    }

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error fetching repositories: {response.status_code}")
            print(response.json())
            break
        
        page_repos = response.json()
        if not page_repos:
            break
        
        repos.extend(page_repos)
        params["page"] += 1
        
    return repos

def filter_repos_by_topic(repos, topic):
    """
    Filters repositories by a given topic.
    """
    filtered = []
    for repo in repos:
        topics = repo.get("topics", [])
        if topic.lower() in [t.lower() for t in topics]:
            filtered.append(repo)
    return filtered

def main():
    load_dotenv()
    token = os.getenv("ADMIN_TOKEN")
    
    if not token:
        print("Error: ADMIN_TOKEN not found in .env file.")
        return

    parser = argparse.ArgumentParser(description="Filter GitHub repositories by topic.")
    parser.add_argument("topic", help="The topic to filter by (e.g., 'python', 'automation')")
    args = parser.parse_args()

    print(f"Fetching repositories for the authenticated user...")
    all_repos = fetch_all_repos(token)
    print(f"Found {len(all_repos)} repositories.")

    filtered_repos = filter_repos_by_topic(all_repos, args.topic)
    
    if not filtered_repos:
        print(f"No repositories found with topic: {args.topic}")
    else:
        print(f"\nRepositories with topic '{args.topic}':")
        for i, repo in enumerate(filtered_repos, 1):
            print(f"{i}. {repo['full_name']} ({repo['html_url']})")

if __name__ == "__main__":
    main()
