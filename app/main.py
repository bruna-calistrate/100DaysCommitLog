from datetime import date, timedelta
from io import BytesIO

from fastapi import APIRouter, BackgroundTasks, FastAPI, Response, status

from app.commits_graph import CommitsGraph
from app.github_scraper import GithubScraper
from app.models import (
    CollectCommitCounterPayload,
    CollectCommitDataPayload,
    CollectCommitDataResponse,
)


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
        "/commit_counter/",
        description="Get daily commit count GitHub users.",
        status_code=status.HTTP_200_OK,
    )
    def collect_commits(commit_data_payload: CollectCommitCounterPayload):
        filter_date = date.today() - timedelta(days=1)
        gs = GithubScraper(
            users_list=commit_data_payload.users_list,
            filter_date=filter_date,
            counter_date=True,
        )
        commit_data = gs.count_commits()
        return commit_data

    @app_router.post(
        "/plot_commit_graph/",
        description="Plot commit graph of users.",
        status_code=status.HTTP_201_CREATED,
    )
    async def plot_commit_graph(commit_data_payload: CollectCommitDataPayload):
        background_tasks = BackgroundTasks()
        graph = BytesIO()
        cg = CommitsGraph(
            users_list=commit_data_payload.users_list,
            filter_date=commit_data_payload.filter_date,
        )
        commit_graph_fig = cg.create_commit_graph()
        commit_graph_fig.savefig(graph, format="png", bbox_inches="tight")

        graph_contents: bytes = graph.getvalue()
        background_tasks.add_task(graph.close)
        headers = {"Content-Disposition": "inline; filename='out.png'"}
        return Response(graph_contents, headers=headers, media_type="image/png")

    app.include_router(app_router)

    return app
