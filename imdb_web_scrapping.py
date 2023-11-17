# Import necessary libraries
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# Downloading the IMDb top 250 movies' data
Url = 'http://www.imdb.com/chart/top'
response = requests.get(Url)
soup = BeautifulSoup(response.text, "html.parser")
movies = soup.select('td.titleColumn')
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]

# Create an empty list to store movie information
movie_list = []

# Iterate over the movies to extract each movie's data
for index in range(0, len(movies)):
    # Separate movie into 'place', 'title', 'year'
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index)) + 1:-7]
    year = re.search('\((.*?)\)', movie_string).group(1)
    place = movie[:len(str(index)) - (len(movie))]
    data = {
        "place": place,
        "movie_title": movie_title,
        "rating": ratings[index],
        "year": year,
        "star_cast": crew[index]
    }
    movie_list.append(data)

# Print movie details with their ratings
for movie in movie_list:
    print(movie['place'], '-', movie['movie_title'], '(' + movie['year'] + ') -',
          'starring ' + movie['star_cast'], movie['rating'])

# Create a DataFrame from the extracted data
df = pd.DataFrame(movie_list)

# Save the DataFrame to a CSV file
df.to_csv('imdb_top_250_movies.csv', index=False)
