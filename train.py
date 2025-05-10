import pygame
import numpy as np
from solver import QLearningSolver  # Chỉ import QLearningSolver từ solver.py
from game import Game  # Import Game từ game.py
import os

# Định nghĩa lại hàm load_map ở đây
def load_map(level):
    list_map = []
    path = f"levels\\{level}.txt"
    if not os.path.exists(path):
        print(f"Thư mục {path} không tồn tại.")
        return
    else:
        with open(path, "r") as file:
            for line in file:
                row = [char for char in line.rstrip('\n')]
                list_map.append(row)
    return list_map

def train_game(level):
    # Khởi tạo pygame
    pygame.init()

    # Load level và khởi tạo trò chơi
    matrix = load_map(level)  # Bạn có thể điều chỉnh hàm này nếu cần
    game = Game(matrix, [])  # Khởi tạo game với ma trận từ file level

    # Khởi tạo QLearningSolver để huấn luyện
    q_learning_solver = QLearningSolver(game)
    
    # Huấn luyện Q-learning liên tục
    print("Training Q-learning... Press F1 to stop.")
    
    # Tạo cửa sổ pygame (không cần hiện thị nhưng cần để theo dõi sự kiện)
    screen = pygame.display.set_mode((100, 100))  # Cửa sổ nhỏ không cần hiển thị
    
    # Thực hiện huấn luyện trong vòng lặp
    q_learning_solver.train(screen)  # Chạy vòng lặp huấn luyện, truyền màn hình pygame để theo dõi sự kiện

    # Lưu bảng Q đã huấn luyện nếu cần thiết (có thể thêm tính năng lưu bảng Q vào file)
    np.save("q_table.npy", q_learning_solver.agent.q_table)  # Lưu bảng Q
    print("Training complete and Q-table saved.")

if __name__ == "__main__":
    level = "level1"  # Bạn có thể thay đổi hoặc lấy từ input
    train_game(level)
