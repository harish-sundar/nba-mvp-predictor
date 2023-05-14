import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_cleaner import total

# gets the top 10 players with highest MVP Share who have played over 70 games
def highest_mvp_share_visual():
    highest_scoring_players = total[total["G"] > 70].sort_values("Share", ascending=False).head(10)
    # create the bar plot
    ax = highest_scoring_players.plot.bar(x="Player", y="Share")
    # adjust x-axis label font size
    plt.xticks(rotation=45, ha='right', fontsize=8)
    # show the plot
    plt.show()

# scatterplot that shows the relationship between a player's team performace and share of mvp votes
def mvp_votes_team_performance_visual():
    # select relevant columns
    data = total[["Player", "Year", "Share", "W/L%"]]
    # create the scatter plot
    plt.scatter(data["Share"], data["W/L%"])
    # add axis labels and title
    plt.xlabel("Share of MVP Votes")
    plt.ylabel("Team Win-Loss Percentage")
    plt.title("Relationship Between MVP Votes and Team Performance")
    # show the plot
    plt.show()

# correlation matrix between each predictor (check Share correlation for most dependent on MVP votes)
def corr_matrix_between_predictors():
    # sets predictors
    corr_columns = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%',
        '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST',
        'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Pts Won', 'Pts Max', 'Share']
    # gets the necessary data
    corr_data = total[corr_columns]
    # creates a correlation matrix
    corr_matrix = corr_data.corr()
    # sets font for readability
    sns.set(font_scale=0.5)
    # sets the size of the plot
    plt.figure(figsize=(20, 10))
    # creates the heatmap with seaborn
    sns.heatmap(corr_matrix, annot=True, cmap="YlGnBu")
    plt.title("Correlation between NBA player statistics and MVP Share")
    # shows plot
    plt.show()

# gets a boxplot of share by position 
def position_share_corr_visual():
    # create a box plot of Share by position using seaborn
    sns.boxplot(x='Pos', y='Share', data=total)
    plt.title("MVP Share by Position")
    plt.xlabel("Position")
    plt.ylabel("MVP Share")
    plt.xticks(rotation=45)
    plt.show()





