import os
from collections import defaultdict

import requests
from dotenv import load_dotenv

from app.models import CollectCommitDataResponse, CommitData, RepositoryData
from utils import dt_to_br_timezone, str_to_date, str_to_datetime


class GithubScraper:
    """
    A class to scrape GitHub repositories and commits data for specified users.

    Attributes:
    - users_list (list): A list of GitHub users to scrape data from.
    - filter_date (str): A date string to filter the data by.
    - exact_date (bool): A flag to determine if filtering should be done based on exact date
      or after the date.
    - github_token (str): GitHub API token for authentication.

    Methods:
    - get_repositories_names(user): Retrieves the names of repositories for a given user.
    - get_repository_data(repository_data): Retrieves data for a specific repository.
    - get_repository_commits(repository_name, user): Retrieves commits data for a specific
     repository and user.
    - get_commit_data(commit_data, repository_name, repository_owner): Retrieves data for
     a specific commit.
    - collect_users_data(): Collects commits data for all specified users.
    - count_daily_commits(): Counts daily commits for each user.
    - count_commits(): Counts total commits for each user.
    """

    def __init__(
        self, users_list: list, filter_date: str, exact_date: bool = False
    ):
        load_dotenv()

        self.users_list = users_list
        if isinstance(users_list, list) is False:
            self.users_list = [users_list]
        self.filter_date = str_to_date(filter_date)
        self.exact_date = exact_date
        self.github_token = os.getenv("GITHUB_TOKEN")

    def get_repositories_names(self, user):
        """
        Retrieves the names of repositories for a given user by making a GET request to the
        GitHub API.

        Parameters:
        - user (str): The GitHub user for whom to retrieve repository names.

        Returns:
        - list: A list of repository names for the specified user.
        """

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

    def get_repository_data(self, repository_data: dict):
        """
        Retrieves data for a specific repository based on the provided repository data.

        Parameters:
        - repository_data (dict): The data of the repository to extract information from.

        Returns:
        - RepositoryData: An instance of RepositoryData class containing repository name and
         updated date if the conditions are met, otherwise None.
        """

        updated_at = dt_to_br_timezone(
            str_to_datetime(repository_data.get("updated_at"))
        ).date()
        data = {
            "repository_name": repository_data.get("full_name"),
            "repository_updated_at": updated_at,
        }
        if self.exact_date:
            if updated_at == self.filter_date:
                return RepositoryData(**data)
        else:
            if updated_at >= self.filter_date:
                return RepositoryData(**data)
        return None

    def get_repository_commits(self, repository_name: str, user: str):
        """
        Retrieves commits data for a specific repository and user by making a GET request to
        the GitHub API.

        Parameters:
        - repository_name (str): The name of the repository to retrieve commits from.
        - user (str): The GitHub user who owns the repository.

        Returns:
        - list: A list of CommitData instances for the specified repository and user.
        """

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

    def get_commit_data(
        self, commit_data: dict, repository_name: str, repository_owner: str
    ):
        """
        Retrieves data for a specific commit based on the provided commit data.

        Parameters:
        - commit_data (dict): The data of the commit to extract information from.
        - repository_name (str): The name of the repository the commit belongs to.
        - repository_owner (str): The owner of the repository where the commit was made.

        Returns:
        - CommitData: An instance of CommitData class containing commit details if the
         conditions are met, otherwise None.
        """

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
        if self.exact_date:
            if commit_date.date() == self.filter_date:
                return CommitData(**data)
        else:
            if commit_date.date() >= self.filter_date:
                return CommitData(**data)
        return None

    def collect_users_data(self):
        """
        Collects commits data for all specified users by iterating through each user,
        retrieving their repositories, and then fetching commits data for each repository.

        Returns:
        - CollectCommitDataResponse: An instance of CollectCommitDataResponse class
         containing all the collected commits data.
        """
        commits_data = []
        for user in self.users_list:
            repositories = self.get_repositories_names(user=user)
            for repository in repositories:
                repo_commits = self.get_repository_commits(repository, user)
                commits_data.extend(repo_commits)
        return CollectCommitDataResponse(commits_data=commits_data)

    def count_daily_commits(self):
        """
        Counts the number of daily commits for each user based on the collected commits data.

        Returns:
        - dict: A dictionary where keys are authors and values are dictionaries with commit
         dates as keys and the count of commits on that date as values.
        """

        users_data = self.collect_users_data()
        commits_count = defaultdict(lambda: defaultdict(int))

        for commit in users_data.commits_data:
            author = commit.repository_owner
            commit_date = commit.commit_date
            commits_count[author][commit_date] += 1
        return commits_count

    def count_commits(self):
        """
        Counts the total number of commits made by each user based on the collected commits
        data.

        Returns:
        - dict: A dictionary where keys are GitHub users and values are the total count of
         commits made by each user.
        """

        users_data = self.collect_users_data()
        users_values = [0 for user in self.users_list]
        commits_count = dict(zip(self.users_list, users_values))

        for commit in users_data.commits_data:
            author = commit.repository_owner
            commits_count[author] += 1
        return commits_count
