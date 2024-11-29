import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

movies = pd.read_csv('../movies.csv')

# Tách các thể loại từ cột 'genres'
movies['genres'] = movies['genres'].str.split('|')
all_genres = movies['genres'].explode()

# Trực quan hóa số lượng phim theo thể loại
plt.figure(figsize=(10, 8))
sns.countplot(y=all_genres, order=all_genres.value_counts().index, palette="Set2")
plt.title('Số lượng phim theo thể loại')
plt.xlabel('Số lượng phim')
plt.ylabel('Thể loại')
plt.show()
