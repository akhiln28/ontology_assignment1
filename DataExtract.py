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
	Title = ET.SubElement(movie,"Title")
	Title.text = ptitle
	Genre = ET.SubElement(movie,"Genres")
	genre = ET.SubElement(Genre,"Genre")
	genre.text = genres
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
tree.write("data.xml")


