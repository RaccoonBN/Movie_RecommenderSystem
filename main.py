import pandas as pd
from recommender import MovieRecommender
from GUI import MovieGUI
import tkinter as tk


def load_data():
    ratings = pd.read_csv('data/ratings.csv')
    movies = pd.read_csv('data/movies.csv')
    return ratings, movies


if __name__ == "__main__":
    # Tải dữ liệu
    ratings, movies = load_data()

    # Khởi tạo mô hình gợi ý
    recommender = MovieRecommender(ratings, movies)

    # Khởi tạo GUI
    root = tk.Tk()
    movie_gui = MovieGUI(root, recommender)
    root.mainloop()
