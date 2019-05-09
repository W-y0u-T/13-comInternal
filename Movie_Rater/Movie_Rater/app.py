
from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)
import os
import pickle 
import operator

global movies, movies_by_year

path = os.getcwd() +"/static/images"
app.config['UPLOAD_FOLDER'] = path

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app
class Movie(object):

	def __init__(self, filename):
		self.title = "A Place Holder"
		self.year = "2000"
		self.director = "Place Holder"
		self.filename = filename
		self.review = "No previous review has been found"
		self.rating = "No previous rating has been found"
		self.trailer_url="Empty"
	

	def add_summary(self,input):
		self.review = f"{input}"


fname = "movies_list.pkl"
#function which stores the movie class instances into a pickle file
def pickle_object():
	#opens file 
	with open(fname, "wb") as fout:
		#converts the list into a pickle file
		pickle.dump(movies, fout, protocol=-1)

#function which takes the pickle file and turns it back into a list filled with class instances
def unpickle_object():
	global movies
	#checks if file contains anything or exists and then opens and unpickles it 
	if os.path.isfile(fname):
		if os.path.getsize(fname) > 0:
			with open(fname, "rb") as fin:
				movies = pickle.load(fin)

def sort_list_by_year():
	global movies
	return(sorted(movies, key=operator.attrgetter('year')))

def sort_list_by_alphabet():
	global movies
	return(sorted(movies, key=operator.attrgetter('title')))







movies=[]
sorted_movies = []
#first runs this function to read file and places it into a 
unpickle_object()
#if the file contained no data it will write new data to it
if not movies:
	for filename in os.listdir(path):
		movies.append(Movie(filename))
	pickle_object()


#app.route for home page
@app.route('/')
def hello():
	#checks which if the user wants the movies to be sorted by year or alphabet then returns the movies and 
	sort = request.args.get("sortBy")
	sorted_movies = sort_list_by_year()
	if sort == "year":
		sorted_movies = sort_list_by_year()
		return render_template("movies.html", movies = sorted_movies)
	else:
		sorted_movies = sort_list_by_alphabet()
		return render_template("movies.html", movies = sorted_movies)
	

#app.route for rating page and allows the client to view their previous rating and change it.
@app.route('/rate', methods=["GET","POST"])
def rate():
	unpickle_object
	#for loop to make sure the data we are sending to and from the page is going to the right place
	for movie in movies:
		if movie.filename == request.args.get("fileName"):
			rating = movie.rating
			summary = movie.review
			video = movie.trailer_url
			rateAgain = request.args.get("toRate")
			
			#to check if the page needs to display the rating options or the previous rating
			if rateAgain == "True" or movie.review =="No previous rating has been found":
				toRate = True
			else:
				toRate = False
				#requests information from the form
			if request.method== "POST":
				form = request.form
				rate_value = form["rating"]
				checkbox = form["toRateAgain"]
				summary = form["summary"]
				video = form["youtubeID"]
				title = form["title"]
				year = form["year"]
				director = form["direct"]
				movie.trailer_url = video
				movie.add_summary(summary)
				movie.rating = rate_value
				movie.title = title
				movie.year = year
				movie.director = director
				#if statement to see if the user wants to change the rating
				
				pickle_object()
				return render_template("rate_movie.html", summary = movie.review, rating = movie.rating, video = video, toRate = False)
	return render_template('rate_movie.html', rating = rating, summary = summary, video = video, toRate = toRate)

@app.route('/upload', methods=["POST","GET"])
def mainUploader():
	#for the page with the uploader
	if request.method == "POST":
		file = request.files["file"]
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		movies.append(Movie(filename))
		pickle_object()
	return render_template("upload.html")

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug = True)
