from flask import Flask, render_template, request
import requests
import pickle
import pandas as pd


app = Flask(__name__)


#functions
def img_fetcher(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=a6f31f6cd4aa2cf07c4d64f3a5c9a9fa&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def recommender(movie):
    movie_ind = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_ind]
    movies_l = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    rec_movies = []
    rec_movies_img = []

    for i in movies_l:
        movies_id = movies_list.iloc[i[0]].movie_id


        rec_movies_img.append(img_fetcher(movies_id))
        rec_movies.append(movies_list.iloc[i[0]].title)
    return rec_movies, rec_movies_img



# declarations
movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = pd.DataFrame(movies_list)


@app.route('/')
def index():
    return render_template('index.html', movie_n = movies_list['title'].values)

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_movie = request.form['selected_movie']
    name, img = recommender(selected_movie)
    print(name[0])
    print(img[0])
    imns = zip(name, img)
    return render_template('index.html', imns = imns, movie_n = movies_list['title'].values)

if __name__ == "__main__":
    app.run(debug=True)