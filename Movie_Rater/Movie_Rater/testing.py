import operator
import pickle
import os
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
		
movies=[]
path = os.getcwd() +"/static/images"
for filename in os.listdir(path):
	movies.append(Movie(filename))
print("Show each filename")
for movie in movies:
    print(movie.filename)
print('-'*50)
# pickle the list of instances
fname = "instance_list.pkl"
# pickle dump the list object
with open(fname, "wb") as fout:
    # default protocol is zero
    # -1 gives highest prototcol and smallest data file size
    pickle.dump(movies, fout, protocol=-1)
print("Data has been pickled to file {}".format(fname))
# pickle load the list object back in (senses protocol)
with open(fname, "rb") as fin:
    movies2 = pickle.load(fin)
print("Pickled data has been reloaded ..")
print('-'*50)
# test loaded list of instances
for movie in movies2:
    print(movie.filename)
