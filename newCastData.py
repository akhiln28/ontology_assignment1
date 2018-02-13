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
nameBasics = pd.read_csv("name_basics1.tsv",sep='\t')


tittleInfo.runtimeMinutes.replace(to_replace="\\N",value="120",inplace=True)

tittleMovies = tittleInfo.loc[ tittleInfo['titleType'] == 'movie']  #7k
tittleSeries =  tittleInfo.loc[ tittleInfo['titleType'] == 'tvSeries'] #4k
tittleEP =  tittleInfo.loc[ tittleInfo['titleType'] == 'tvEpisode']





root = ET.Element("IMDB")
Celebs = ET.SubElement(root,"Celebs")
crewDF =  pd.read_csv("cdata.csv",sep=',')

for i in range(0,1500):
    nconst = nameBasics.nconst.iloc[i]
    nDF = crewDF[crewDF['celebID']==nconst]
    if(nDF.empty==True):
        continue
    Celeb =  ET.SubElement(Celebs,"Celeb")
    Celeb.set("CelebID",str(nconst))
    name = ET.SubElement(Celeb,"Name")
    name.text = str(nameBasics.primaryName.iloc[i])
    BirthYear = ET.SubElement(Celeb,"BirthYear")
    BirthYear.text = str(nameBasics.birthYear.iloc[i])
    primProf = ET.SubElement(Celeb,"PrimaryProfession")
    primProf.text = str(nameBasics.primaryProfession.iloc[i])
    knownFor = ET.SubElement(Celeb,"KnownFor")
    # knownForTitles = nameBasics.knownForTitles.iloc[0]
    for el in range(0,nDF.shape[0]) :
        tt = ET.SubElement(knownFor,"TitleRef")
        tt.text = str(nDF.ID.iloc[el])
