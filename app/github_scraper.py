import os
from collections import defaultdict

import requests
from dotenv import load_dotenv

from app.models import CollectCommitDataResponse, CommitData, RepositoryData
from utils import dt_to_br_timezone, str_to_date, str_to_datetime


class GithubScraper:
    def __init__(
        self, users_list: list, filter_date: str, counter_date: bool = False
    ):
        load_dotenv()

        self.users_list = users_list
        if isinstance(users_list, list) is False:
            self.users_list = [users_list]
        self.filter_date = str_to_date(filter_date)
        self.counter_date = counter_date
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
            data = self.get_repository_data(repository_data=repo)
            if data is not None:
                repositories_names.append(data.repository_name)
        return repositories_names

    def get_repository_data(self, repository_data):
        updated_at = dt_to_br_timezone(
            str_to_datetime(repository_data.get("updated_at"))
        ).date()
        data = {
            "repository_name": repository_data.get("full_name"),
            "repository_updated_at": updated_at,
        }
        if self.counter_date:
            if updated_at == self.filter_date:
                return RepositoryData(**data)
        else:
            if updated_at >= self.filter_date:
                return RepositoryData(**data)
        return None

    def get_repository_commits(self, repository_name: str, user: str):
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
            data = self.get_commit_data(
                commit_data=c,
                repository_name=repository_name,
                repository_owner=user,
            )
            if data is not None:
                commits.append(data)
        return commits

    def get_commit_data(self, commit_data, repository_name, repository_owner):
        commit = commit_data.get("commit")
        author = commit_data.get("author")
        commit_author = commit.get("author")
        commit_date = dt_to_br_timezone(
            str_to_datetime(commit_author.get("date"))
        )

        data = {
            "repository_name": repository_name,
            "repository_owner": repository_owner,
            "commit_user_login": author.get("login") if author else None,
            "commit_author_name": commit_author.get("name"),
            "commit_author_email": commit_author.get("email"),
            "commit_message": commit.get("message"),
            "commit_sha": commit_data.get("sha"),
            "commit_url": commit_data.get("html_url"),
            "commit_date": commit_date.date(),
            "commit_created_at": commit_date,
        }
        if self.counter_date:
            if commit_date.date() == self.filter_date:
                return CommitData(**data)
        else:
            if commit_date.date() >= self.filter_date:
                return CommitData(**data)
        return None

    def collect_users_data(self):
        commits_data = []
        for user in self.users_list:
            repositories = self.get_repositories_names(user=user)
            for repository in repositories:
                repo_commits = self.get_repository_commits(repository, user)
                commits_data.extend(repo_commits)
        return CollectCommitDataResponse(commits_data=commits_data)

    def count_daily_commits(self):
        users_data = self.collect_users_data()
        commits_count = defaultdict(lambda: defaultdict(int))

        for commit in users_data.commits_data:
            author = commit.repository_owner
            commit_date = commit.commit_date
            commits_count[author][commit_date] += 1
        return commits_count

    def count_commits(self):
        users_data = self.collect_users_data()
        users_values = [0 for user in self.users_list]
        commits_count = dict(zip(self.users_list, users_values))

        for commit in users_data.commits_data:
            author = commit.repository_owner
            commits_count[author] += 1
        return commits_count
