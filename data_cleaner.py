import pandas as pd
import matplotlib.pyplot as plt

mvps = pd.read_csv("mvp_data.csv")

# gets only necessary headers for data
mvps = mvps[["Player", "Year", "Pts Won", "Pts Max", "Share"]]

players = pd.read_csv("player_data.csv")

# deletes unnecessary columns
del players["Rk"]

# removes the * from the player's name
players["Player"] = players["Player"].str.replace("*","", regex = False) 

# checks that each player played for only one team that season
def check_player_rows(df): 
    if df.shape[0] == 1:
        return df
    # if player has numerous teams, then it will get the total stats of that season
    else:
        row = df[df["Tm"] == "TOT"]
        # replaces the team with team last played for
        row["Tm"] = df.iloc[-1,:]["Tm"]
        return row
    
# applies the given function to groups of players 
players = players.groupby(["Player", "Year"]).apply(check_player_rows)

# drops both duplicate columns
players.index = players.index.droplevel()
players.index = players.index.droplevel()


# merges player data with team data
combined = players.merge(mvps, how = "outer", on = ["Player", "Year"])
combined[["Pts Won", "Pts Max", "Share"]] = combined[["Pts Won", "Pts Max", "Share"]].fillna(0)

teams = pd.read_csv("team_data.csv")
teams = teams[~teams["W"].str.contains("Division")].copy()

# removes * from team name in data
teams["Team"] = teams["Team"].str.replace("*", "", regex=False)

# removes the duplicate values in Team caused by \xa0 character
for i in range(1,20):
    teams["Team"] = teams["Team"].str.replace('\xa0('+ str(i) + ')', '')

# creates a dictionary that maps each team nickname to team name
nicknames = {}
with open("team_nicknames.csv") as f:
    lines = f.readlines()
    for line in lines[1:]:
        abb,name = line.replace("\n", "").split(",")
        nicknames[abb] = name

# adds new column with full team name for proper merging
combined["Team"] = combined["Tm"].map(nicknames)

total = combined.merge(teams, how = "outer", on=["Team","Year"])
del total["Unnamed: 0"]

# converts all data types to correct datatypes
total = total.apply(pd.to_numeric, errors="ignore")
total["GB"] = total["GB"].str.replace("—","0")

print(total["3P%"].head(10))

# writes cleaned, combined data to a csv file
total.to_csv("player_mvp_combined.csv", index=False)

# shows factors most necessary for a nj