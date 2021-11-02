from bs4 import BeautifulSoup
import requests

original = "https://mldb.org/"

letters = ['0', '_'] + [chr(i) for i in range(ord('A'), ord('Z') + 1)]

for letter in letters:
	for i in range(0, 10000, 30):
		url = original + f"aza-{letter}-{i}.html"
		
		text = requests.get(url).text
		soup = BeautifulSoup(text, 'lxml')

		for element in soup.select(".h > td:nth-child(2) > a"):
			artist_url = original + element["href"]

			artist_text = requests.get(artist_url).text
			artists_soup = BeautifulSoup(artist_text, 'lxml')

			for element in artists_soup.select("#thelist > tr > td > a"):
				song_url = original + element["href"]

				song_text = requests.get(song_url).text
				songs_soup = BeautifulSoup(song_text, 'lxml')

				info = songs_soup.select("#thelist > tr > td > a")

				artist = info[0].string
				album = info[1].string

				lyrics = songs_soup.select_one(".songtext").text
				print(lyrics)