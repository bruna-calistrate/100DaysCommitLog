import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from app.github_scraper import GithubScraper


class CommitsGraph:
    def __init__(self, users_list: list, filter_date: str):
        self.users_list = users_list
        self.filter_date = filter_date

    def create_commits_dataframe(self):
        scraper = GithubScraper(
            users_list=self.users_list, filter_date=self.filter_date
        )
        daily_commits = scraper.count_daily_commits()
        df = pd.DataFrame.from_dict(daily_commits).sort_index()
        df = df.reindex(sorted(df.columns), axis=1)
        return df

    def create_commit_graph(self):
        fig = plt.figure(figsize=(5, 5))

        commits_graph_data = self.create_commits_dataframe()
        cmap = sns.color_palette("blend:#9be9a8,#216e39", as_cmap=True)
        ax = sns.heatmap(commits_graph_data, cmap=cmap, cbar=False)
        ax.set(xlabel="", ylabel="")
        return fig
