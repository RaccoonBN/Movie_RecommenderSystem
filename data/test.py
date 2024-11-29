import pandas as pd
from sklearn.model_selection import train_test_split

# Đọc dữ liệu ratings (giả sử tệp ratings.csv có sẵn)
ratings = pd.read_csv('ratings.csv')

# Chia dữ liệu thành hai phần: 80% huấn luyện, 20% kiểm tra
train_ratings, test_ratings = train_test_split(ratings, test_size=0.2, random_state=42)

# Lưu bộ dữ liệu kiểm tra vào tệp CSV mới
test_ratings.to_csv('test_ratings.csv', index=False)

print("Đã tạo bộ dữ liệu kiểm tra và lưu vào test_ratings.csv")
