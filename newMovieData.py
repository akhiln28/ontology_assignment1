import pandas as pd
import xml.etree.ElementTree as ET
import sys
from random import *
import importlib
# load all data in Panda dataframes


# titles information
tittleInfo = pd.read_csv( "tittle_basics1.tsv", sep='\t' ) #100k
# tittleCrew = pd.read_csv( "tittle_crew1.tsv", sep='\t' )
tittleRatings = pd.read_csv( "tittle_ratings.tsv", sep='\t')
# tittleEpisode = pd.read_csv( "tittle_episode1.tsv", sep='\t')
# tittlePrinciple = pd.read_csv("tittle_principles1.tsv", sep='\t')
# nameBasics = pd.read_csv("name_basics1.tsv",sep='\t')


tittleInfo.runtimeMinutes.replace(to_replace="\\N",value="120",inplace=True)

tittleMovies = tittleInfo.loc[ tittleInfo['titleType'] == 'movie']  #7k
tittleSeries =  tittleInfo.loc[ tittleInfo['titleType'] == 'tvSeries'] #4k
tittleEP =  tittleInfo.loc[ tittleInfo['titleType'] == 'tvEpisode']





root = ET.Element("IMDB")

Movies = ET.SubElement(root,"Movies")

crewDF =  pd.read_csv("cdata.csv",sep=',')

#DF.empty , df[ df.col == 'val'] //for searching
for i in range(0,400):
    movie = ET.SubElement(Movies,"Movie")
    ptitle = tittleMovies.primaryTitle.iloc[i] #string
    genres = tittleMovies.genres.iloc[i]	#string maybe aaray also
    year = tittleMovies.startYear.iloc[i]  #int
    runtime = tittleMovies.runtimeMinutes.iloc[i] #string
    tconst =  tittleMovies.tconst.iloc[i] #string
    movie.set("MovieID",str(tconst))
    rateDF = tittleRatings[ tittleRatings['tconst']== tconst]
    rating = " "
    if(rateDF.empty==False):
        rating = rateDF.averageRating.iloc[0]
    Title = ET.SubElement(movie,"Title")
    Title.text = str(ptitle)
    Crew = ET.SubElement(movie,"Crew")
    Director = ET.SubElement(Crew,"Director")
    tcrew = crewDF[ crewDF['ID']==tconst ]
    Director.text = str(tcrew.celebID.iloc[0])
    #add casts
    Stars = ET.SubElement(Crew,"Cast")
    castDF = tcrew.iloc[1:,:]
    for cL in range(0,castDF.shape[0]):
        castIDT = ET.SubElement(Stars,"CelebRef")
        castIDT.text = str(tcrew.celebID.iloc[cL])
    #add genre
    Genre = ET.SubElement(movie,"Genres")
    genreList = genres.split(',')
    for gtext in genreList :
        genre = ET.SubElement(Genre,"Genre")
        genre.text = gtext
    Desc = ET.SubElement(movie,"Description")
    Year = ET.SubElement(Desc,"Year")
    Year.text = str(year)
    rtime = ET.SubElement(Desc,"RunTime")
    rtime.text = runtime
    Rate = ET.SubElement(movie,"Ratings")
    Rate.text = str(rating);

