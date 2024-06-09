import os

import requests


class GithubScraper:
    def __init__(self, users_list: list, filter_date: str):
        from dotenv import load_dotenv

        load_dotenv()

        self.users_list = users_list
        if isinstance(users_list, list) is False:
            self.users_list = [users_list]
        self.filter_date = filter_date
        self.github_token = os.getenv("GITHUB_TOKEN")

    def get_repositories_names(self, user):
        url = f"https://api.github.com/users/{user}/repos"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {self.github_token}",
        }
        req = requests.get(url, headers=headers)
        assert req.status_code == 200, f"failed to fetch repos for {user}"

        repositories_data = req.json()
        repositories_names = []
        for repo in repositories_data:
            updated_at = repo.get("updated_at")
            if updated_at > self.filter_date:
                repositories_names.append(repo.get("full_name"))
        return repositories_names

    def get_repository_commits(self, repository_name):
        url = f"https://api.github.com/repos/{repository_name}/commits"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {self.github_token}",
        }
        req = requests.get(url, headers=headers)
        assert (
            req.status_code == 200
        ), f"failed to fetch commits for {repository_name}"
        commits_data = req.json()

        commits = []
        for c in commits_data:
            commit = c.get("commit")
            author = c.get("author")
            commit_author = commit.get("author")
            commit_date = commit_author.get("date")

            data = {
                "repository_name": repository_name,
                "commit_user_login": author.get("login") if author else None,
                "commit_author": commit_author.get("name"),
                "commit_message": commit.get("message"),
                "commit_sha": c.get("sha"),
                "commit_url": c.get("html_url"),
                "commit_created_at": commit_date,
            }
            if commit_date > self.filter_date:
                commits.append(data)
        return commits

    def collect_users_data(self):
        commits_data = []
        for user in self.users_list:
            repositories = self.get_repositories_names(user=user)
            for repository in repositories:
                commits = self.get_repository_commits(repository)
                commits_data.extend(commits)
        return commits_data
