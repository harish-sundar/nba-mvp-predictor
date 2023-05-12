import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

stats = pd.read_csv("player_mvp_combined.csv")

# fills null stats with 0
stats = stats.fillna(0)

# defines predictors for machine learning
predictors = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
       '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 
       'Year', 'W', 'L', 'W/L%', 'GB', 'PS/G', 'PA/G', 'SRS']

# defines training and test data for machine learning
train = stats[stats["Year"] < 2023]
test = stats[stats["Year"] == 2023]

# makes a model for predicting the shares based on Share column
reg = Ridge(alpha=.1)

# trains the model
reg.fit(train[predictors], train["Share"])
predictions = reg.predict(test[predictors])
predictions = pd.DataFrame(predictions, columns = ["predictions"], index = test.index)

# merges the predictions and the test column together to compare predictions vs reality
combination = pd.concat([test[["Player", "Share"]], predictions], axis = 1)

# calculates the mean squared error of the model
mean_squared_error(combination["Share"], combination["predictions"])

# sorts the mvp candidates 
combination = combination.sort_values("Share", ascending = False)
# adds a rank column
combination["Rk"] = list(range(1,combination.shape[0] + 1))


# sorts the predicted mvp candidates 
combination = combination.sort_values("predictions", ascending = False)
# adds a rank column
combination["Predicted_Rk"] = list(range(1,combination.shape[0] + 1))

# checks if actual and predicted are both in top 5, if so it gives a point
# error metric
def find_ap(combination):
    actual = combination.sort_values("Share", ascending = False).head(5)
    predicted = combination.sort_values("predictions", ascending = False)
    ps = []
    found = 0
    seen = 1
    # goes through all predicted rows
    for index, row in predicted.iterrows():
        # checks if the player predicted is actual values
        if row["Player"] in actual["Player"].values:
            # if so, adds a point
            found += 1
            ps.append(found/seen)
        seen += 1
    return sum(ps)/ len(ps)


all_predictions = []
def add_ranks(combination): 
    # sorts the mvp candidates 
    combination = combination.sort_values("Share", ascending = False)
    # adds a rank column
    combination["Rk"] = list(range(1,combination.shape[0] + 1))
    # sorts the predicted mvp candidates 
    combination = combination.sort_values("predictions", ascending = False)
    # adds a rank column
    combination["Predicted_Rk"] = list(range(1,combination.shape[0] + 1))
    # adds the difference between actual and predicted rank
    combination["Diff"] = combination["Rk"] - combination["Predicted_Rk"]
    return combination

years = list(range(1990, 2024))


sc = StandardScaler()

# backtesting - makes predictions for most of our errors
def backtest(stats, model, year, predictors):
    aps = []
    all_predictions = []
    for year in years[5:]:
        # train is all data before year
        train = stats[stats["Year"] < year]
        # tests the year with the training data
        test = stats[stats["Year"] == year]
        # fitting the model to make predictions
        sc.fit(train[predictors], train["Share"])

        train[predictors] = sc.transform(train[predictors])
        test[predictors] = sc.transform(test[predictors])
        # makes predictions with model and converts to df
        predictions = model.predict(test[predictors])
        predictions = pd.DataFrame(predictions, columns = ["predictions"], index = test.index)
        # merges the predictions and the test column together to compare predictions vs reality
        combination = pd.concat([test[["Player", "Share"]], predictions], axis = 1)
        combination = add_ranks(combination)
        all_predictions.append(combination)
        aps.append(find_ap(combination))
    return sum(aps)/len(aps), aps, pd.concat(all_predictions)

# adds another column which takes the ratio of a players stats to the mean 
stat_ratios = stats[["PTS", "AST", "STL", "BLK", "3P", "Year"]].groupby("Year").apply(lambda x: x/x.mean())
# Add this line to reset the index
stat_ratios = stat_ratios.reset_index(drop=True) 
# adds columns to stats
stats[["PTS_R", "AST_R", "STL_R", "BLK_R", "3P_R"]] = stat_ratios[["PTS", "AST", "STL", "BLK", "3P"]]
# adds columns to predictors
predictors += ["PTS_R", "AST_R", "STL_R", "BLK_R", "3P_R"]

stats["NPos"] = stats["Pos"].astype("category").cat.codes
stats["NTm"] = stats["Tm"].astype("category").cat.codes

# creates a random forest regressor
rf = RandomForestRegressor(n_estimators = 50, random_state = 1,min_samples_split=5)

mean_ap, aps, all_predictions = backtest(stats, reg, years[30:], predictors)


print(mean_ap)