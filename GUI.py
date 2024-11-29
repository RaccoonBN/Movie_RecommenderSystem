import tkinter as tk
from tkinter import messagebox, ttk

class MovieGUI:
    def __init__(self, master, recommender):
        self.master = master
        self.recommender = recommender
        master.title("Gợi Ý Phim")

        # Khung chính
        self.main_frame = tk.Frame(master, bg="#34495e")
        self.main_frame.pack(padx=10, pady=10)

        # Tiêu đề
        self.title_label = tk.Label(self.main_frame, text="Hệ Thống Gợi Ý Phim", font=("Arial", 24, "bold"), bg="#34495e", fg="#ecf0f1")
        self.title_label.pack(pady=10)

        # Nhập ID người dùng
        self.label = tk.Label(self.main_frame, text="Nhập ID người dùng:", font=("Arial", 14), bg="#34495e", fg="#ecf0f1")
        self.label.pack(pady=5)

        self.user_id_entry = tk.Entry(self.main_frame, font=("Arial", 14), justify='center')
        self.user_id_entry.pack(pady=5)

        self.submit_button = tk.Button(self.main_frame, text="Gợi ý phim", command=self.get_recommendations, bg="#2980b9", fg="#ecf0f1", font=("Arial", 14))
        self.submit_button.pack(pady=10)

        # Button cho người mới
        self.new_user_button = tk.Button(self.main_frame, text="Dành Cho Người Mới", command=self.show_new_user_window, bg="#27ae60", fg="#ecf0f1", font=("Arial", 14))
        self.new_user_button.pack(pady=10)

        # Khung hiển thị kết quả
        self.result_frame = tk.Frame(self.main_frame, bg="#ecf0f1", bd=2, relief=tk.GROOVE)
        self.result_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Bảng phim thích
        self.liked_frame = tk.LabelFrame(self.result_frame, text="Phim Bạn Thích", font=("Arial", 12, "bold"), bg="#ecf0f1")
        self.liked_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.liked_list = tk.Listbox(self.liked_frame, width=50, height=5, font=("Arial", 12), bg="#ecf0f1")
        self.liked_list.pack(padx=10, pady=10)

        # Bảng phim không thích
        self.disliked_frame = tk.LabelFrame(self.result_frame, text="Phim Bạn Không Thích", font=("Arial", 12, "bold"), bg="#ecf0f1")
        self.disliked_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.disliked_list = tk.Listbox(self.disliked_frame, width=50, height=5, font=("Arial", 12), bg="#ecf0f1")
        self.disliked_list.pack(padx=10, pady=10)

        # Bảng gợi ý phim
        self.recommendations_frame = tk.LabelFrame(self.result_frame, text="Gợi Ý Phim", font=("Arial", 12, "bold"), bg="#ecf0f1")
        self.recommendations_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.recommendations_list = tk.Listbox(self.recommendations_frame, width=100, height=5, font=("Arial", 12), bg="#ecf0f1")
        self.recommendations_list.pack(padx=10, pady=10)

        # Khung cho người mới
        self.new_user_window = None

    def get_recommendations(self):
        user_id = self.user_id_entry.get()
        if not user_id.isdigit():
            messagebox.showerror("Lỗi", "Vui lòng nhập một ID người dùng hợp lệ!")
            return

        user_id = int(user_id)
        try:
            # Lấy phim người dùng thích và không thích
            liked_movies, disliked_movies = self.recommender.get_user_preferences(user_id)

            # Lấy gợi ý phim
            recommendations = self.recommender.get_recommendations(user_id)

            # Xóa danh sách cũ
            self.liked_list.delete(0, tk.END)
            self.disliked_list.delete(0, tk.END)
            self.recommendations_list.delete(0, tk.END)

            # Hiển thị tối đa 10 phim cho mỗi loại
            max_display = 10  # Số lượng phim tối đa cho mỗi loại

            # Hiển thị thông tin phim thích (tối đa 10 phim)
            liked_movies_info = self.recommender.movies[self.recommender.movies['movieId'].isin(liked_movies)]
            liked_movies_to_show = liked_movies_info.head(max_display)
            for _, row in liked_movies_to_show.iterrows():
                self.liked_list.insert(tk.END, f"{row['title']} - {row['genres']}")

            # Hiển thị thông tin phim không thích (tối đa 10 phim)
            disliked_movies_info = self.recommender.movies[self.recommender.movies['movieId'].isin(disliked_movies)]
            disliked_movies_to_show = disliked_movies_info.head(max_display)
            for _, row in disliked_movies_to_show.iterrows():
                self.disliked_list.insert(tk.END, f"{row['title']} - {row['genres']}")

            # Hiển thị gợi ý phim (tối đa 10 phim)
            recommendations_to_show = recommendations.head(max_display)
            for _, row in recommendations_to_show.iterrows():
                self.recommendations_list.insert(tk.END, f"{row['title']} - {row['genres']}")

        except KeyError:
            messagebox.showerror("Lỗi", "ID người dùng không hợp lệ!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

    def show_new_user_window(self):
        # Tạo cửa sổ mới cho người mới
        if not self.new_user_window:
            self.new_user_window = tk.Toplevel(self.master)
            self.new_user_window.title("Giao Diện Người Mới")
            self.new_user_window.geometry("800x600")

            # Hiển thị phim được đánh giá cao
            self.top_rated_frame = tk.LabelFrame(self.new_user_window, text="Phim Được Đánh Giá Cao", font=("Arial", 12, "bold"), bg="#ecf0f1")
            self.top_rated_frame.pack(pady=10, fill=tk.BOTH, expand=True)
            self.top_rated_list = tk.Listbox(self.top_rated_frame, width=100, height=5, font=("Arial", 12), bg="#ecf0f1")
            self.top_rated_list.pack(padx=10, pady=10)

            # Hiển thị khung chọn thể loại
            self.genre_label = tk.Label(self.new_user_window, text="Chọn Thể Loại:", font=("Arial", 12, "bold"),
                                        bg="#ecf0f1")
            self.genre_label.pack(pady=10)

            # Lấy danh sách thể loại từ phương thức get_genres
            genres = self.recommender.get_genres()

            # Cập nhật giá trị của genre_combo bằng danh sách thể loại
            self.genre_combo = ttk.Combobox(self.new_user_window, width=40, font=("Arial", 12))
            self.genre_combo['values'] = genres
            self.genre_combo.pack(pady=5)

            # Button để lấy gợi ý phim theo thể loại
            self.genre_button = tk.Button(self.new_user_window, text="Gợi Ý Phim Theo Thể Loại", command=self.get_genre_recommendations, bg="#f39c12", fg="#ecf0f1", font=("Arial", 14))
            self.genre_button.pack(pady=10)

            # Khung gợi ý phim theo thể loại
            self.genre_recommendations_frame = tk.LabelFrame(self.new_user_window, text="Gợi Ý Phim Theo Thể Loại", font=("Arial", 12, "bold"), bg="#ecf0f1")
            self.genre_recommendations_frame.pack(pady=10, fill=tk.BOTH, expand=True)
            self.genre_recommendations_list = tk.Listbox(self.genre_recommendations_frame, width=100, height=5, font=("Arial", 12), bg="#ecf0f1")
            self.genre_recommendations_list.pack(padx=10, pady=10)

        # Hiển thị danh sách phim được đánh giá cao
        top_rated_movies = self.recommender.get_top_rated_movies()
        for _, row in top_rated_movies.iterrows():
            self.top_rated_list.insert(tk.END, f"{row['title']} - {row['genres']}")

    def get_genre_recommendations(self):
        selected_genre = self.genre_combo.get()
        if not selected_genre:
            messagebox.showerror("Lỗi", "Vui lòng chọn một thể loại phim!")
            return

        # Lấy gợi ý phim theo thể loại
        genre_recommendations = self.recommender.get_movies_by_genre(selected_genre)

        # Xóa danh sách cũ
        self.genre_recommendations_list.delete(0, tk.END)

        # Hiển thị gợi ý phim theo thể loại
        for _, row in genre_recommendations.iterrows():
            self.genre_recommendations_list.insert(tk.END, f"{row['title']} - {row['genres']}")

if __name__ == "__main__":
    root = tk.Tk()
    recommender = 'MovieRecommender'
    app = MovieGUI(root, recommender)
    root.geometry("800x600")
    root.resizable(False, False)
    root.mainloop()
