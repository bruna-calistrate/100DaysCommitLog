import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from app.github_scraper import GithubScraper


class CommitsGraph:
    """
    A class to create a heatmap graph representing daily commits data for specified GitHub users.

    Attributes:
    - users_list (list): A list of GitHub users for whom to visualize commit data.
    - filter_date (str): A date string to filter the commit data by.

    Methods:
    - create_commits_dataframe(): Creates a pandas DataFrame from the daily commits data.
    - create_commit_graph(): Creates a heatmap graph of daily commits data using seaborn and
     matplotlib.
    """

    def __init__(self, users_list: list, filter_date: str):
        self.users_list = users_list
        self.filter_date = filter_date

    def create_commits_dataframe(self):
        """
        Creates a pandas DataFrame from the daily commits data for the specified users.

        Returns:
        - DataFrame: A DataFrame containing daily commits data for each user.
        """

        scraper = GithubScraper(
            users_list=self.users_list, filter_date=self.filter_date
        )
        daily_commits = scraper.count_daily_commits()
        df = pd.DataFrame.from_dict(daily_commits).sort_index()
        df = df.reindex(sorted(df.columns), axis=1)
        return df

    def create_commit_graph(self):
        """
        Creates a heatmap graph representing daily commits data for the specified users.

        Returns:
        - Figure: A matplotlib Figure object representing the heatmap graph.
        """

        fig = plt.figure(figsize=(5, 5))

        commits_graph_data = self.create_commits_dataframe()
        cmap = sns.color_palette("blend:#9be9a8,#216e39", as_cmap=True)
        ax = sns.heatmap(commits_graph_data, cmap=cmap, cbar=False)
        ax.set(xlabel="", ylabel="")
        return fig
