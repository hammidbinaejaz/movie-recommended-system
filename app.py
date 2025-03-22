from flask import Flask, jsonify
import gdown
import pickle
import os

app = Flask(__name__)

# Google Drive file IDs
MOVIES_FILE_ID = "1CYnGpC3C2bZLZXl3ji4MeSFgATj4cPml"
SIMILARITY_FILE_ID = "1BrqkLMRAdAGEog1gHq_8i_jtQX03W6SY"

# Download function
def download_file(file_id, output):
    if not os.path.exists(output):
        print(f"Downloading {output}...")
        gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

# Ensure files exist
download_file(MOVIES_FILE_ID, "movies.pkl")
download_file(SIMILARITY_FILE_ID, "similarity.pkl")

# Load Data
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

@app.route("/")
def home():
    return jsonify({"message": "API is running!"})

@app.route("/movies")
def get_movies():
    return jsonify({"movies": movies.to_dict()})

@app.route("/recommend/<movie_name>")
def recommend(movie_name):
    if movie_name not in movies["title"].values:
        return jsonify({"error": "Movie not found"})

    index = movies[movies["title"] == movie_name].index[0]
    distances = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)[1:6]
    
    recommendations = [movies.iloc[i[0]]["title"] for i in distances]
    return jsonify({"recommendations": recommendations})

if __name__ == "__main__":
    app.run(debug=True)
