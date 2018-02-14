import xml.etree.ElementTree as et

tree = et.parse("Updateddata_seasons.xml")
root = tree.getroot()

html = et.Element("html")
head = et.SubElement(html, "head")
title = et.SubElement(head, "title")
title.text = "IMDB"

body = et.SubElement(html, "body")
MoviesTable = et.SubElement(body, "table")

Movies = root[0].getchildren()

for Movie in Movies:
    if(float(Movie[4].text) > 5):
        htmlmovie = et.SubElement(MoviesTable, "tr")
        titletd = et.SubElement(htmlmovie, "td")
        # directortd = et.SubElement(htmlmovie, "td")
        ratingtd = et.SubElement(htmlmovie, "td")
        yeartd = et.SubElement(htmlmovie, "td")

        titletd.text = Movie[0].text
        ratingtd.text = Movie[4].text
        yeartd.text = Movie[3][0].text


tree = et.ElementTree(html)
tree.write("Movies_with_rating_5.html")
