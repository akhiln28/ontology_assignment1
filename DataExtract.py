import pandas as pd
import xml.etree.ElementTree as ET
import sys
from random import *
import importlib
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
tittleEP =  tittleInfo.loc[ tittleInfo['titleType'] == 'tvEpisode']


tittleInfo.runtimeMinutes.replace(to_replace="\\N",value="120",inplace=True)



root = ET.Element("IMDB")

Movies = ET.SubElement(root,"Movies")

#DF.empty , df[ df.col == 'val'] //for searching
for i in range(0,10):
	movie = ET.SubElement(Movies,"Movie")
	ptitle = tittleMovies.primaryTitle.iloc[i] #string
	genres = tittleMovies.genres.iloc[i]	#string maybe aaray also
	year = tittleMovies.startYear.iloc[i]  #int
	runtime = tittleMovies.runtimeMinutes.iloc[i] #string
	tconst =  tittleMovies.tconst.iloc[i] #string
	#temp Dataframe for getiing ratings
	rateDF = tittleRatings[ tittleRatings['tconst']== tconst]
	rating = " "
	if(rateDF.empty==False):
		rating = rateDF.averageRating.iloc[0]  #np.float
	#generate xml
	Title = ET.SubElement(movie,"Title")
	Title.text = ptitle
	Crew = ET.SubElement(movie,"Crew")
	Director = ET.SubElement(Crew,"Director")
	#get director info
	dirDF =  tittleCrew[ tittleCrew['tconst']== tconst]
	if(dirDF.empty==False):
		dirIDList = (dirDF.directors.iloc[0]).split(',')
		dirID = dirIDList[0]										#TODO one or more Directors
		Director.text = str(dirID)
	else :
		Director.text = ""
	#add casts
	Stars = ET.SubElement(Crew,"Cast")
	castDF = tittlePrinciple[tittlePrinciple['tconst']==tconst]
	if(castDF.empty==False):
		castIDList = (castDF.principalCast.iloc[0]).split(',');
		for castID in castIDList:
			castIDT = ET.SubElement(Stars,"CelebRef")
			castIDT.text = str(castID)
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


TVshows = ET.SubElement(root,'TVshows')

#DF.empty , df[ df.col == 'val'] //for searching
for i in range(0,10):
	TVshow = ET.SubElement(TVshows,"TVshow")

	ptitle = tittleSeries.primaryTitle.iloc[i] #string
	genres = tittleSeries.genres.iloc[i]	#string maybe aaray also
	year = tittleSeries.startYear.iloc[i]  #int
	runtime = tittleSeries.runtimeMinutes.iloc[i] #string
	tconst =  tittleSeries.tconst.iloc[i] #string
	TVshow.set("TvShowID",str(tconst))
	#temp Dataframe for getiing ratings
	rateDF = tittleRatings[ tittleRatings['tconst']== tconst]
	rating = " "
	if(rateDF.empty==False):
		rating = rateDF.averageRating.iloc[0]  #np.float
	#generate xml
	Title = ET.SubElement(TVshow,"Title")
	Title.text = str(ptitle)
	Crew = ET.SubElement(TVshow,"Crew")
	Director = ET.SubElement(Crew,"Director")
	#get director info
	dirDF =  tittleCrew[ tittleCrew['tconst']== tconst]
	if(dirDF.empty==False):
		dirIDList = (dirDF.directors.iloc[0]).split(',')
		dirID = dirIDList[0]										#TODO one or more Directors
		Director.text = str(dirID)
	else :
		Director.text = ""
	#add casts
	Stars = ET.SubElement(Crew,"Cast")
	castDF = tittlePrinciple[tittlePrinciple['tconst']==tconst]
	if(castDF.empty==False):
		castIDList = (castDF.principalCast.iloc[0]).split(',');
		for castID in castIDList:
			castIDT = ET.SubElement(Stars,"CelebRef")
			castIDT.text = str(castID)
	#add genre
	Genre = ET.SubElement(TVshow,"Genres")
	genreList = genres.split(',')
	for gtext in genreList :
		genre = ET.SubElement(Genre,"Genre")
		genre.text = str(gtext)
	Desc = ET.SubElement(TVshow,"Description")
	Year = ET.SubElement(Desc,"Year")
	Year.text = str(year)
	rtime = ET.SubElement(Desc,"RunTime")
	rtime.text = str(runtime)
	#seasons
	Seasons = ET.SubElement(TVshow,"Seasons")
	numSeason = ET.SubElement(Seasons,"Number_of_Seasons")
	
	#episodes
	tittleEpisode.seasonNumber.replace(to_replace="\\N",value="0",inplace=True)
	#all eps of series
	epDF = tittleEpisode[tittleEpisode['parentTconst']==tconst]
	numSeason.text = str(epDF.seasonNumber.unique().size)
	if(epDF.empty==False):
		epDF.sort_values('seasonNumber',inplace=True)
		sList = epDF.seasonNumber.unique().tolist()
		sList= map(int,sList)
		for sL in sList:
			sDF = epDF[epDF['seasonNumber']==str(sL)]
			Season = ET.SubElement(Seasons,"Season")
			numEp = ET.SubElement(Season,"No_of_Episodes")
			numEp.text = str(sDF.shape[0])
			Epi = ET.SubElement(Season,"Episodes")
			yearS = " "
			for idx in range(0,sDF.shape[0]):
				etconst = sDF.tconst.iloc[idx]
				EpiDF = tittleEP[tittleEP['tconst']==etconst]
				episodeTag = ET.SubElement(Epi,"Episode")
				if(EpiDF.empty==False):
					epText = str(EpiDF.primaryTitle.iloc[0])
					episodeTag.text = str(EpiDF.primaryTitle.iloc[0])
					i = randint(1,10)
					j = randint(1,10)
					rate = str(i)+"."+str(j)
					ratTag = ET.SubElement(Epi,"Rating")
					ratTag.text = str(rate)
					yearS = EpiDF.startYear.iloc[0]
			Syear = ET.SubElement(Season,"Year")
			Syear.text = str(yearS)
			i = randint(1,10)
			j = randint(1,10)
			Srate = str(i)+"."+str(j)
			SratTag = ET.SubElement(Season,"Rating")
			SratTag.text = str(Srate)
			#rating for seasom
	Rate = ET.SubElement(TVshow,"Ratings")
	Rate.text = str(rating);


Celebs = ET.SubElement(root,"Celebs")
for i in range(0,100):
	Celeb =  ET.SubElement(Celebs,"Celeb")
	nconst = nameBasics.nconst.iloc[i]
	Celeb.set("CelebID",str(nconst))
	name = ET.SubElement(Celeb,"Name")
	name.text = str(nameBasics.primaryName.iloc[i])
	BirthYear = ET.SubElement(Celeb,"BirthYear")
	BirthYear.text = str(nameBasics.birthYear.iloc[i])
	primProf = ET.SubElement(Celeb,"PrimaryProfession")
	primProf.text = str(nameBasics.primaryProfession.iloc[i])
	knownFor = ET.SubElement(Celeb,"KnownFor")
	knownForTitles = nameBasics.knownForTitles.iloc[0]
	for el in knownForTitles.split(',') :
		tt = ET.SubElement(knownFor,"TitleRef")
		tt.text = str(el)
tree = ET.ElementTree(root)
tree.write("GenIMDBdata.xml")


