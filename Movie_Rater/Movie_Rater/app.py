
from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)
import os
import pickle 

global movies

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app
class Movie(object):

	def __init__(self, filename):
		self.filename = filename
		self.review = "No previous review has been found"
		self.rating = "No previous rating has been found "
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




movies=[]
unpickle_object()
#if the file contained no data it will write new data to it
if not movies:
	path = os.getcwd() +"/static/images"
	for filename in os.listdir(path):
		movies.append(Movie(filename))
	pickle_object()



@app.route('/')
def hello():

	return render_template("movies.html", movies = movies)

@app.route('/rate', methods=["GET","POST"])
def rate():
	for movie in movies:
		if movie.filename == request.args.get("fileName"):
			rating = movie.rating
			summary = movie.review
			if movie.trailer_url == "Empty":
				videoExists = False
			else:
				videoExists = True
			if request.method== "POST":
				form = request.form
				rate_value = int(form["rating"])
				movie.rating = rate_value
				summary = form["summary"]
				movie.add_summary(summary)
				pickle_object()
				return render_template("rate_movie.html", summary = movie.review, rating = movie.rating)
	return render_template('rate_movie.html', rating = rating, summary = summary, video = "https://www.youtube.com/watch?v=dQw4w9WgXcQ")

@app.route('/upload', methods=["POST","GET"])
def mainUploader():
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

