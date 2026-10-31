# import requests

# URL = "https://api.github.com/users/octocat/repos"

# response = requests.get(URL, timeout=10)
# print(response.status_code)

# repos = response.json()
# print(len(repos))
# print(repos[0]["name"])

import csv
import requests

URL = "https://api.github.com/users/octocat/repos"


def fetch():
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    return response.json()


def transform(repos):
    rows = []
    for repo in repos:
        rows.append({
            "name": repo["name"],
            "language": repo["language"],
            "stars": repo["stargazers_count"],
            "updated_at": repo["updated_at"],
        })
    return rows


def save(rows, filename="repos.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "language", "stars", "updated_at"])
        writer.writeheader()
        writer.writerows(rows)


def main():
    try:
        repos = fetch()
    except requests.RequestException as error:
        print(f"Could not fetch data: {error}")
        return
    rows = transform(repos)
    save(rows)
    print(f"Saved {len(rows)} repos to repos.csv")


if __name__ == "__main__":
    main()

