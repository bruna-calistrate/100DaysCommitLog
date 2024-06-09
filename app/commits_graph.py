import pandas as pd
import seaborn as sns

from utils import get_first_name


class CommitsGraph:
    def __init__(self, users_list: list, filter_date: str):
        self.users_list = users_list
        self.filter_date = filter_date

    def create_commit_dataframe(self):
        from app.github_scraper import GithubScraper

        scraper = GithubScraper(
            users_list=self.users_list, filter_date=self.filter_date
        )
        commit_data = scraper.collect_users_data()
        df = pd.DataFrame.from_records(commit_data)
        return df

    def transform_data(self):
        df = self.create_commit_dataframe()
        df["commit_created_at"] = pd.to_datetime(
            df["commit_created_at"]
        ).dt.tz_convert("America/Sao_Paulo")
        df["commit_date"] = df["commit_created_at"].dt.date
        df["commit_author_first_name"] = df["commit_author"].apply(
            get_first_name
        )
        commits_graph_df = pd.pivot_table(
            df,
            index="commit_author_first_name",
            columns="commit_date",
            values="commit_sha",
            aggfunc="count",
        )
        return commits_graph_df

    def create_commit_graph(self):
        commits_graph_data = self.transform_data()
        cmap = sns.color_palette("blend:#9be9a8,#216e39", as_cmap=True)
        ax = sns.heatmap(commits_graph_data, cmap=cmap, cbar=False)
        return ax
