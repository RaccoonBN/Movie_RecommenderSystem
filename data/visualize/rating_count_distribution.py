import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc file ratings.csv
ratings = pd.read_csv('../ratings.csv')

# Đếm số lượng đánh giá cho mỗi phim
movie_rating_count = ratings.groupby('movieId').size().reset_index(name='rating_count')

# Trực quan hóa phân bố số lượng đánh giá cho các phim
plt.figure(figsize=(8, 6))
sns.histplot(movie_rating_count['rating_count'], bins=50, kde=False, color='green')
plt.title('Phân bổ số lượng đánh giá trên mỗi phim')
plt.xlabel('Số lượng đánh giá')
plt.ylabel('Số lượng phim')
plt.show()
