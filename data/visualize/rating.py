import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ratings = pd.read_csv('../ratings.csv')

# Trực quan hóa phân bố đánh giá của người dùng
plt.figure(figsize=(8, 6))
sns.histplot(ratings['rating'], bins=10, kde=False, color='blue')
plt.title('Phân bổ đánh giá của người dùng')
plt.xlabel('Rating')
plt.ylabel('Số lượng')
plt.show()
