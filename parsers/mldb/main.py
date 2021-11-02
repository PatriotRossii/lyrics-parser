from bs4 import BeautifulSoup
import requests


class Lyrics:
	def __init__(self, artist, album, lyrics):
		self.artist = artist
		self.album = album
		self.lyrics = lyrics


class MLDBSource:
	original_url = "https://mldb.org/"
	letters = ['X'] #+ [chr(i) for i in range(ord('A'), ord('Z') + 1)]

	def get_artists(self):
		artist_urls = []
		for letter in MLDBSource.letters:
			for i in range(0, 10000, 30):
				url = MLDBSource.original_url + f"aza-{letter}-{i}.html"

				text = requests.get(url).text
				soup = BeautifulSoup(text, 'lxml')

				result = soup.select(".h > td:nth-child(2) > a")
				if not result:
					break

				for element in result:
					artist_urls.append(MLDBSource.original_url  + element["href"])
		return artist_urls

	def get_songs(self, artists_urls):
		song_urls = []
		for artist_url in artists_urls:
			artist_text = requests.get(artist_url).text
			artists_soup = BeautifulSoup(artist_text, 'lxml')

			for element in artists_soup.select("#thelist > tr > td > a"):
				song_urls.append(MLDBSource.original_url + element["href"])
		return song_urls

	def get_lyrics(self, song_urls):
		lyrics = []
		for song_url in song_urls:
			song_text = requests.get(song_url).text
			songs_soup = BeautifulSoup(song_text, 'lxml')

			info = songs_soup.select("#thelist > tr > td")
			length = len(info)

			artist = None
			album = None

			a_artist = info[0].find('a')
			a_album = info[1].find('a')

			if a_artist:
				artist = a_artist.string
			if a_album:
				album = a_album.string

			lyric = songs_soup.select_one(".songtext").text
			lyrics.append(Lyrics(artist, album, lyric))
		return lyrics

	def get(self):
		return self.get_lyrics(self.get_songs(self.get_artists()))
