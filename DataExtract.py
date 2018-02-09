import pandas as pd
import xml.etree.ElementTree as ET
import sys
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
		dirNameDF = nameBasics[nameBasics['nconst']== dirID]
		if(dirNameDF.empty==False):
			dirName = dirNameDF.primaryName.iloc[0]
			Director.text = dirName
		else:
			Director.text = ""
	else :
		Director.text = ""
	#add casts
	Stars = ET.SubElement(Crew,"Stars")
	castDF = tittlePrinciple[tittlePrinciple['tconst']==tconst]
	if(castDF.empty==False):
		castIDList = (castDF.principalCast.iloc[0]).split(',');
		for castID in castIDList:
			castNameDF = nameBasics[nameBasics['nconst']== castID]
			if(castNameDF.empty==False):
				castName = castNameDF.primaryName.iloc[0]
				castBirtyear = castNameDF.birthYear.iloc[0]
				star = ET.SubElement(Stars,"star")
				sname = ET.SubElement(star,"name")
				sdob = ET.SubElement(star,"BirthYear")
				sname.text = castName
				sdob.text = castBirtyear
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


	# castDF = tittlePrinciple[tittlePrinciple['tconst']==tconst ]
	# castId = castDF.principalCast.tolist()
	# for cast in castId:

reload(sys)
sys.setdefaultencoding('utf8')
tree = ET.ElementTree(root)
tree.write("GenIMDBdata.xml")


