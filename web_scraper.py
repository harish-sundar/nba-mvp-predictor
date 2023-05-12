import time
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# gets NBA data from seasons 1989-1990 til 2022-2023
years = list(range(1990, 2024))
url_temp = "https://www.basketball-reference.com/awards/awards_{}.html"

# gets the page of each year listed in range 
for year in years:
     url = url_temp.format(year)
     req = requests.get(url)
     time.sleep(15)
     # writes each year's page to mvp folder 
     with open("mvp/{}.html".format(year), "w+") as f:
         f.write(req.text)

dfs = []
for year in years:
    with open("mvp/{}.html".format(year)) as f:
        page = f.read()
    soup = BeautifulSoup(page, "html.parser")
    # removes unnecessary header from table
    soup.find('tr', class_= 'over_header').decompose()
    mvp_table = soup.find(id="mvp")
    # gets each year's table and converts to dataframe
    curr_mvp = pd.read_html(str(mvp_table))[0]
    # creates a column year
    curr_mvp["Year"] = year
    # appends all dataframes into a list
    dfs.append(curr_mvp)

# puts it all into one dataframe
mvps = pd.concat(dfs)

# converts mvp dataframe into csv file
mvps.to_csv("mvp_data.csv", index=False)

directory_path = 'players'

# puts all the files into a list
player_files = []
for year in years:
    time.sleep(2)
    player_files.append(os.path.join(directory_path, 'players_{}.csv'.format(year)))

df = pd.DataFrame()
dfs = []

# puts all the dataframes in one
for file in player_files:
    data = pd.read_csv(file)
    player_data = pd.concat([df, data], axis = 0)
    # adds a year column to differentiate each df
    year = int(os.path.basename(file).split('_')[1].split('.')[0])
    player_data["Year"] = year
    dfs.append(player_data)

# concats in one dfs
players = pd.concat(dfs)

# converts dataframe to single csv file
players.to_csv("player_data.csv")


# scrapes team data
team_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html"

# gets the team pages for each year in range
for year in years:
    url = team_stats_url.format(year)
    team_data = requests.get(url)
    time.sleep(15)
    with open("teams/{}.html".format(year), "w+") as f:
        f.write(team_data.text)

dfs = []

# parses the team pages into a data frame
for year in years:
    with open("teams/{}.html".format(year)) as f:
        page = f.read()
    
    soup = BeautifulSoup(page, 'html.parser')
    # removes unnecessary header
    soup.find('tr', class_="thead").decompose()
    # gets the eastern conference standings from each page
    e_table = soup.find_all(id="divs_standings_E")[0]
    e_df = pd.read_html(str(e_table))[0]
    e_df["Year"] = year
    e_df["Team"] = e_df["Eastern Conference"]
    del e_df["Eastern Conference"]
    dfs.append(e_df)
    # gets the western conference standings from each page
    w_table = soup.find_all(id="divs_standings_W")[0]
    w_df = pd.read_html(str(w_table))[0]
    w_df["Year"] = year
    w_df["Team"] = w_df["Western Conference"]
    del w_df["Western Conference"]
    dfs.append(w_df)

# adds all team_data to a dataframe
team_data = pd.concat(dfs)
# converts to csv
team_data.to_csv("team_data.csv", index = False)


