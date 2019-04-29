import pickle
import os
movies = []
fname='testing.pkl'
class Movie(object):

	def __init__(self, filename):
		self.filename = filename
		self.review = ""
		self.rating = ""
		self.trailer_url=""
	
	def add_rating(self,input):
		self.rating = f"{input} Stars"

	def add_summary(self,input):
		self.review = f"{input}"
		
path = os.getcwd() +"/static/images"
for filename in os.listdir(path):
	movies.append(Movie(filename))
	print(filename)
with open(fname, "wb") as fout:
    pickle.dump(movies, fname, protocol=-1)
print("Pickling has been successful!")
with open(fname, "rb") as fin:
    movies2 = pickle.load(fin)
print("Data unpickled!")
for movie in movies2:
    print(f" filename is {movie.filename}")
    

