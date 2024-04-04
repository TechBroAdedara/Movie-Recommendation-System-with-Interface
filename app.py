import streamlit as st
import requests
import pickle
new_df = pickle.load(open("movie_list.pkl", 'rb'))
similarities = pickle.load(open("similarities.pkl", 'rb'))

#API Logic here ---------------
key = "6e850d4349959c41efb7704632a47526"

def get_movie_poster(movie_id):
    #We use the movie_ID to get information of the TMDB webpage the movie info is contained in
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}")
    data=response.json()
    #The key: poster_path contains the poster img URL that we would 
    #   pass to the API once more
    return "https://image.tmdb.org/t/p/w185"+data['poster_path']

#Function to handle recommendations here---------
def recommend(selected_movie_name):
    idx = new_df[new_df["original_title"] == selected_movie_name].index[0]
    distances = similarities[idx]
    recommendations = sorted(list(enumerate(distances)), 
                             reverse = True, 
                             key=lambda x:x[1])[0:10]
    
    recommendation_list = []
    movie_posters = []
    for i in recommendations:
        movie = new_df.iloc[i[0]]
        recommendation_list.append(movie.original_title)
        movie_posters.append(get_movie_poster(movie.id))
    return recommendation_list, movie_posters


#Main Interface here-----------
st.title("Movie Recommender System")
selected_movie_name = st.selectbox("Choose a movie you like", new_df["original_title"].values)
try:
    if st.button("Recommend"): 
        names, posters = recommend(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.text(names[0])
            st.image(posters[0])

        with col2:
            st.text(names[1])
            st.image(posters[1])

        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])
except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
    st.write ("CONNECTION PROBLEMS. Please connect to the internet to see recommendations")

