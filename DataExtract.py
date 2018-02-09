import pandas as pd
import xml.etree.ElementTree as ET

# load all data in Panda dataframes

# titles information
tittleInfo = pd.read_csv( "tittle_basics1.tsv", sep='\t' ) #100k
tittleCrew = pd.read_csv( "tittle_crew1.tsv", sep='\t' )
tittleRatings = pd.read_csv( "tittle_ratings.tsv", sep='\t')
tittleEpisode = pd.read_csv( "tittle_episode1.tsv", sep='\t')
tittlePrinciple = pd.read_csv("tittle_principles1.tsv", sep='\t')
nameBasics = pd.read_csv("name_basics1.tsv",sep='\t')

tittleMovies = tittleInfo.loc[ tittleInfo['titleType'] == 'movie']  #7k
tittleSeries =  tittleInfo.loc[ tittleInfo['titleType'] == 'tvSeries'] #4k

# 100 movies tittle and object in array
movT = (tittleMovies.iloc[:100,:]).tolist();
