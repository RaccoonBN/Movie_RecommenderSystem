import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc file ratings.csv
ratings = pd.read_csv('../ratings.csv')

# Đếm số lượng đánh giá cho mỗi người dùng
user_rating_count = ratings.groupby('userId').size().reset_index(name='rating_count')

# Trực quan hóa phân bố số lượng phim mà mỗi người dùng đã đánh giá
plt.figure(figsize=(8, 6))
sns.histplot(user_rating_count['rating_count'], bins=50, kde=False, color='purple')
plt.title('Phân bố số lượng phim mà mỗi người dùng đã đánh giá')
plt.xlabel('Số lượng phim đã đánh giá')
plt.ylabel('Số lượng người dùng')
plt.show()
