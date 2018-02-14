import xml.etree.ElementTree as et
import random

tree = et.parse("Updateddata_rating_runtime.xml")
root = tree.getroot()

Movies = root[0].getchildren()
Tvshows = root[1].getchildren()

# for Movie in Movies:
#     if Movie[3][1].text == "120":
#         Movie[3][1].text = str(random.randint(30,110))

for Tvshow in Tvshows:
    if Tvshow[4][0].text == '0': #Noofseasons = 0
        n_seasons = random.randint(2,7)
        n_episodes = random.randint(10,15)
        start_year = random.randint(1930,1960)
        Tvshow[4][0].text = str(n_seasons)
        
        for i in range(n_seasons):
            Season = et.SubElement(Tvshow[4], "Season")
            Number_of_episodes = et.SubElement(Season, "No_of_Episodes")
            Episodes = et.SubElement(Season, "Episodes")
            Season_Year = et.SubElement(Season, "Year")
            Season_Rating = et.SubElement(Season, "Rating")
            Season_Year.text = str(i + start_year)

            Number_of_episodes.text = str(n_episodes)
            temp_season_rating = 0
            for j in range(n_episodes):
                Episode = et.SubElement(Episodes, "Episode")
                Title = et.SubElement(Episode, "Title")
                Rating = et.SubElement(Episode, "Rating")

                Title.text = "Episode #" + str(i) + "." + str(j)
                temp_rating = round(random.uniform(4,9),2)
                Rating.text = str(temp_rating)
                temp_season_rating += temp_rating/n_episodes
            Season_Rating.text = str(temp_season_rating)
        
tree.write("Updateddata_seasons.xml")