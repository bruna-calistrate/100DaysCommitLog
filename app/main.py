from fastapi import APIRouter, FastAPI, status

from app.github_scraper import GithubScraper
from app.models import CollectCommitDataPayload, CollectCommitDataResponse


def get_app_router():
    router = APIRouter()

    return router


def create_app() -> FastAPI:
    app = FastAPI()
    app_router = get_app_router()

    @app_router.get(
        "/", description="API health check", status_code=status.HTTP_200_OK
    )
    def root():
        return {"message": "Hello World"}

    @app_router.post(
        "/commit_data/",
        description="Get commit data from GitHub users.",
        status_code=status.HTTP_200_OK,
        response_model=CollectCommitDataResponse,
    )
    def collect_commit_data(commit_data_payload: CollectCommitDataPayload):
        gs = GithubScraper(
            users_list=commit_data_payload.users_list,
            filter_date=commit_data_payload.filter_date,
        )
        commit_data = gs.collect_users_data()
        return commit_data

    @app_router.post(
        "/daily_commit_count/",
        description="Get daily commit count GitHub users.",
        status_code=status.HTTP_200_OK,
        # response_model=CollectCommitDataResponse,
    )
    def collect_daily_commits(commit_data_payload: CollectCommitDataPayload):
        gs = GithubScraper(
            users_list=commit_data_payload.users_list,
            filter_date=commit_data_payload.filter_date,
        )
        commit_data = gs.count_daily_commits()
        return commit_data

    app.include_router(app_router)

    return app
