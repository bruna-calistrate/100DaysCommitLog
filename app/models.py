from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel


class RepositoryData(BaseModel):
    repository_name: str
    repository_updated_at: datetime


class CommitData(BaseModel):
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
    users_list: list
    filter_date: str


class CollectCommitCounterPayload(BaseModel):
    users_list: list


class CollectCommitDataResponse(BaseModel):
    commits_data: List[CommitData]
