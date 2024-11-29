import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(self, ratings, movies):
        # Nhận vào các DataFrame ratings và movies
        self.ratings = ratings
        self.movies = movies
        self.user_movie_matrix = None
        self.user_similarity_matrix = None
        self._create_user_movie_matrix()

    def _create_user_movie_matrix(self):
        """
        Tạo ma trận người dùng-phim với các giá trị là ratings.
        """
        # Tạo ma trận người dùng-phim, mỗi hàng là một người dùng và mỗi cột là một bộ phim
        self.user_movie_matrix = self.ratings.pivot_table(index='userId', columns='movieId', values='rating')
        self.user_movie_matrix.fillna(0, inplace=True)

    def _calculate_similarity(self):
        """
        Tính toán độ tương đồng giữa các người dùng sử dụng cosine similarity.
        """
        # Sử dụng cosine similarity để tính toán độ tương đồng giữa các người dùng
        self.user_similarity_matrix = cosine_similarity(self.user_movie_matrix)

    def save_similarity_matrix(self):
        """
        Lưu ma trận độ tương đồng vào tệp similarity_matrix.pkl.
        """
        with open('similarity_matrix.pkl', 'wb') as f:
            pickle.dump(self.user_similarity_matrix, f)
        print("Đã lưu ma trận độ tương đồng vào tệp similarity_matrix.pkl.")

    def get_user_preferences(self, user_id):
        """
        Lấy danh sách các bộ phim mà người dùng thích và không thích dựa trên rating.
        """
        user_ratings = self.user_movie_matrix.loc[user_id]
        liked_movies = user_ratings[user_ratings > 3].index.tolist()  # Phim có rating > 3 là thích
        disliked_movies = user_ratings[user_ratings <= 3].index.tolist()  # Phim có rating <= 3 là không thích
        return liked_movies, disliked_movies

    def evaluate_accuracy(self, user_id, recommended_movies, top_n=5):
        """
        Đánh giá độ chính xác của các bộ phim gợi ý cho người dùng.
        """
        user_ratings = self.ratings[self.ratings['userId'] == user_id]
        liked_movies = set(user_ratings[user_ratings['rating'] >= 4]['movieId'])
        recommended_movie_ids = set(recommended_movies['movieId'])

        # Tính số bộ phim gợi ý mà người dùng thực sự thích
        tp = len(liked_movies & recommended_movie_ids)  # True Positives
        fp = len(recommended_movie_ids - liked_movies)  # False Positives
        fn = len(liked_movies - recommended_movie_ids)  # False Negatives

        # Tính chính xác
        accuracy = tp / (tp + fp) if (tp + fp) > 0 else 0
        print(f"Accuracy for user {user_id}: {accuracy:.4f}")
        return accuracy

    def get_recommendations(self, user_id, top_n=5):
        """
        Gợi ý các bộ phim cho người dùng dựa trên độ tương đồng với các người dùng khác.
        """
        if self.user_similarity_matrix is None:
            self._calculate_similarity()

        # Lấy chỉ số của người dùng trong ma trận
        user_index = self.user_movie_matrix.index.get_loc(user_id)

        # Tính toán độ tương đồng giữa người dùng hiện tại và các người dùng khác
        similar_users = list(enumerate(self.user_similarity_matrix[user_index]))

        # Sắp xếp người dùng theo độ tương đồng, bỏ qua chính người dùng hiện tại
        similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)[1:]

        recommended_movies = {}

        # Duyệt qua các người dùng tương đồng và gợi ý phim
        for similar_user_index, similarity_score in similar_users:
            similar_user_id = self.user_movie_matrix.index[similar_user_index]
            similar_user_ratings = self.user_movie_matrix.loc[similar_user_id]

            for movie_id, rating in similar_user_ratings.items():
                if movie_id not in recommended_movies:
                    recommended_movies[movie_id] = {'score': 0, 'count': 0}
                recommended_movies[movie_id]['score'] += similarity_score * rating
                recommended_movies[movie_id]['count'] += 1

        # Tính điểm trung bình cho các bộ phim và sắp xếp chúng theo điểm số
        recommended_movies = {movie_id: (data['score'] / data['count']) for movie_id, data in
                              recommended_movies.items() if data['count'] > 0}
        recommended_movies = sorted(recommended_movies.items(), key=lambda x: x[1], reverse=True)[:top_n]

        # Lấy thông tin của các bộ phim được gợi ý
        recommended_movies_info = self.movies[self.movies['movieId'].isin([movie[0] for movie in recommended_movies])]

        # Đánh giá độ chính xác
        self.evaluate_accuracy(user_id, recommended_movies_info, top_n)

        return recommended_movies_info

    def get_top_rated_movies(self, top_n=5):
        """
        Gợi ý các bộ phim có đánh giá cao nhất dựa trên điểm trung bình.
        """
        # Tính điểm trung bình của các bộ phim từ ratings
        movie_ratings = self.ratings.groupby('movieId')['rating'].mean()

        # Sắp xếp các bộ phim theo điểm trung bình và lấy các bộ phim có điểm cao nhất
        top_rated_movie_ids = movie_ratings.sort_values(ascending=False).head(top_n).index
        top_rated_movies = self.movies[self.movies['movieId'].isin(top_rated_movie_ids)]
        return top_rated_movies

    def get_movies_by_genre(self, genre, top_n=5):
        """
        Gợi ý các bộ phim có đánh giá cao nhất trong thể loại cụ thể.
        """
        # Lọc các bộ phim theo thể loại
        genre_movies = self.movies[self.movies['genres'].str.contains(genre, case=False, na=False)]

        # Lấy đánh giá của các bộ phim thuộc thể loại này
        genre_movie_ratings = self.ratings[self.ratings['movieId'].isin(genre_movies['movieId'])]
        genre_movie_ratings_avg = genre_movie_ratings.groupby('movieId')['rating'].mean()

        # Lọc các bộ phim có điểm trung bình cao nhất
        top_rated_genre_movie_ids = genre_movie_ratings_avg.sort_values(ascending=False).head(top_n).index
        top_rated_genre_movies = self.movies[self.movies['movieId'].isin(top_rated_genre_movie_ids)]
        return top_rated_genre_movies

    def get_genres(self):
        """
        Lấy danh sách các thể loại phim có sẵn trong bộ dữ liệu.
        """
        # Tách thể loại phim từ cột 'genres' của DataFrame movies
        genres = self.movies['genres'].str.split('|').explode().unique()
        return genres.tolist()
