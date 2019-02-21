import pandas as pd
import numpy as np

# load in data
movies = pd.read_csv("data/testdoc2_kaggledatahuge_omdb_detailed.csv")

# drop unneeded columns
cols = list(movies)
keys = ['Title','Rated','Runtime','Director','Writer','Awards','Metascore','imdbRating','BoxOffice','Production']
toDrop = np.setdiff1d(cols, keys)
movies.drop(columns=toDrop, inplace=True)
movies.drop_duplicates('Title', inplace=True)

# get rid of nan
movies.dropna(inplace=True)

# create result set
winners = pd.DataFrame(index=movies.index,columns=['Oscar'])

# need to turn the Rated, Director, Writer, Production fields into numbers
ratedDict = {}
directorDict = {}
writerDict = {}
productionDict = {}

def fillDict(dict, df, columnName):
    counter = 0
    for item in df[columnName]:
        if item not in dict:
            dict[item] = counter
            df.replace(item, counter, inplace=True)
            counter += 1

fillDict(ratedDict, movies, 'Rated')
fillDict(directorDict, movies, 'Director')
fillDict(writerDict, movies, 'Writer')
fillDict(productionDict, movies, 'Production')

# counter = 0
# for rating in movies['Rated']:
#     if rating not in ratedDict:
#         ratedDict[rating] = counter
#         movies.replace(rating, counter, inplace=True)
#         counter += 1
#
# counter = 0
# for director in movies['Director']:
#     if director not in directorDict:
#         directorDict[director] = counter
#         movies.replace(director, counter, inplace=True)
#         counter += 1
#
# counter = 0
# for writer in movies['Writer']:
#     if writer not in writerDict:
#         writerDict[writer] = counter
#         movies.replace(writer, counter, inplace=True)
#         counter += 1
#
# counter = 0
# for production in movies['Production']:
#     if production not in directorDict:
#         productionDict[production] = counter
#         movies.replace(production, counter, inplace=True)
#         counter += 1

# remove $ from BoxOffice
movies.replace('[\$,]', '', regex=True, inplace=True)

# remove ' min' from Runtime
movies.replace(' min', '', regex=True, inplace=True)

# modify awards column
for index, row in movies.iterrows():
    total = sum([int(s) for s in row['Awards'].split() if s.isdigit()])
    movies.loc[index, 'Awards'] = total

    # also add to the winners dataframe
    if "Won" in row['Awards']:
        winners.loc[index, 'Oscar'] = 1
    else: winners.loc[index, 'Oscar'] = 0

winners.fillna('0', inplace=True)

movies.to_csv('data/cleaned.csv')
winners.to_csv('data/winners.csv')
