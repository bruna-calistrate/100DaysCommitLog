from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel


class RepositoryData(BaseModel):
    """
    Represents repository data.

    Attributes:
    - repository_name (str): The name of the repository.
    - repository_updated_at (datetime): The date and time when the repository was last
      updated.
    """

    repository_name: str
    repository_updated_at: datetime


class CommitData(BaseModel):
    """
    Represents data related to a commit in a repository.

    Attributes:
    - repository_name (str): The name of the repository.
    - repository_owner (str): The owner of the repository.
    - commit_user_login (str, optional): The login of the user who made the commit.
    - commit_author_name (str): The name of the commit author.
    - commit_author_email (str): The email of the commit author.
    - commit_message (str): The message associated with the commit.
    - commit_sha (str): The SHA of the commit.
    - commit_url (str): The URL of the commit.
    - commit_date (date): The date of the commit.
    - commit_created_at (str | datetime): The creation timestamp of the commit.
    """

    repository_name: str
    repository_owner: str
    commit_user_login: Optional[str]
    commit_author_name: str
    commit_author_email: str
    commit_message: str
    commit_sha: str
    commit_url: str
    commit_date: date
    commit_created_at: str | datetime


class CollectCommitDataPayload(BaseModel):
    """
    Collects commit data from input payload.

    Attributes:
    - users_list (list): A list of users for which commit data is to be collected.
    - filter_date (str): A date string used to filter commits based on a specific date.
    """

    users_list: list
    filter_date: str


class CollectCommitCounterPayload(BaseModel):
    """
    Collects users list from input payload.

    Attributes:
    - users_list (list): A list of users for which commit data is to be collected.
    """

    users_list: list


class CollectCommitDataResponse(BaseModel):
    """
    Represents a response containing a list of commit data.

    Attributes:
    - commits_data (List[CommitData]): A list of CommitData objects representing commit
     information.
    """

    commits_data: List[CommitData]
