import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc file ratings.csv và movies.csv
ratings = pd.read_csv('../ratings.csv')
movies = pd.read_csv('../movies.csv')

# Đếm số lượng đánh giá cho mỗi phim
movie_rating_count = ratings.groupby('movieId').size().reset_index(name='rating_count')

# Lấy top 10 phim có nhiều đánh giá nhất
top_movies = movie_rating_count.sort_values('rating_count', ascending=False).head(10)
top_movies = top_movies.merge(movies[['movieId', 'title']], on='movieId')

# Trực quan hóa các phim phổ biến nhất
plt.figure(figsize=(10, 6))
sns.barplot(y='title', x='rating_count', data=top_movies, palette="Blues_d")
plt.title('Top 10 phim có nhiều đánh giá nhất')
plt.xlabel('Số lượng đánh giá')
plt.ylabel('Tên phim')
plt.show()
