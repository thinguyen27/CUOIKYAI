import time
import pygame
import assets
from game import Game
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from solver import Solve, bfs, astar, backtracking, simulated_annealing, belief_state_search,QLearningSolver
import numpy as np

clock = pygame.time.Clock()

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

def show_win_game(screen):
    font = pygame.font.SysFont("Minecraft", 48)
    
    # Tạo văn bản chiến thắng
    win_text = font.render("You Win!", True, (255, 255, 0))  # Sử dụng màu vàng
    text_rect = win_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
    
    # Vẽ nền mờ cho màn hình chiến thắng
    overlay = pygame.Surface((screen.get_width(), screen.get_height()))  # Tạo bề mặt phủ lên màn hình
    overlay.set_alpha(128)  # Đặt độ trong suốt
    overlay.fill((0, 0, 0))  # Màu nền mờ (đen)

    # Tạo hiệu ứng nhấp nháy cho văn bản
    time_to_show = 0.5  # Hiển thị văn bản trong 0.5 giây
    show_time = time.time()
    
    # Vẽ nền mờ lên màn hình
    screen.blit(overlay, (0, 0))
    
    # Hiển thị văn bản chiến thắng
    screen.blit(win_text, text_rect)
    
    # Tạo nút "Quay lại chọn cấp độ"
    font_small = pygame.font.SysFont("Minecraft", 24)
    back_text = font_small.render("Back to Level Selector", True, (255, 255, 255))
    back_button_rect = back_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
    
    # Vẽ nút "Back to Level Selector"
    screen.blit(back_text, back_button_rect)
    
    pygame.display.flip()

    # Chờ người chơi nhấn nút
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    waiting_for_input = False  # Dừng vòng lặp và quay lại menu chọn cấp độ
                    pygame.quit()
                    launch_level_selector()  # Quay lại màn hình chọn cấp độ
                    return

    # Đợi một thời gian ngắn để hiển thị văn bản (nếu cần)
    while time.time() - show_time < time_to_show:
        pass


def start_game(level):
    select_level = level.lower().replace(" ", "")
    matrix = load_map(select_level)
    solution = 'NoSol'
    if matrix is None:
        messagebox.showerror("Error", f"Level {level} not found!")
        return
    assets.load_sprites()

    pygame.init()
    sprites = pygame.sprite.LayeredUpdates()

    pygame.display.set_caption("Sokoban")

    gameSokoban = Game(matrix, [])

    size = gameSokoban.load_size()
    screen = pygame.display.set_mode(size)

    Game.fill_screen_with_ground(size, screen)

    running = True
    list_dock = gameSokoban.listDock()

    # Thêm biến để theo dõi thời gian và điều kiện thắng
    game_completed = False
    win_start_time = None  # Biến để lưu thời gian khi game hoàn thành

    q_learning_solver = QLearningSolver(gameSokoban)

    # Tải bảng Q đã huấn luyện
    q_table = np.load("q_table.npy")  # Tải bảng Q từ file đã lưu
    q_learning_solver.agent.q_table = q_table  # Cập nhật bảng Q trong QLearningSolver
    while running:
        gameSokoban.fill_screen_with_ground(size, screen)
        gameSokoban.print_game(screen)
        gameSokoban.update_player_position()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if gameSokoban.stack_matrix:
                        gameSokoban.matrix = gameSokoban.stack_matrix.pop()

                elif event.key == pygame.K_UP:
                    gameSokoban.move(-1, 0, list_dock)
                    if gameSokoban.player:
                        gameSokoban.player.set_direction("up")

                elif event.key == pygame.K_DOWN:
                    gameSokoban.move(1, 0, list_dock)
                    if gameSokoban.player:
                        gameSokoban.player.set_direction("down")

                elif event.key == pygame.K_LEFT:
                    gameSokoban.move(0, -1, list_dock)
                    if gameSokoban.player:
                        gameSokoban.player.set_direction("left")

                elif event.key == pygame.K_RIGHT:
                    gameSokoban.move(0, 1, list_dock)
                    if gameSokoban.player:
                        gameSokoban.player.set_direction("right")
                elif event.key == pygame.K_1:
                    solution = bfs(Solve(matrix))
                elif event.key == pygame.K_2:
                    solution = backtracking(Solve(matrix))
                elif event.key == pygame.K_3:
                    solution = astar(Solve(matrix))
                elif event.key == pygame.K_4:
                    solution = simulated_annealing(Solve(matrix))
                elif event.key == pygame.K_5:
                    solution = belief_state_search(Solve(matrix))
                elif event.key == pygame.K_6:
                    print("Solving with Q-learning...")
                    solution = q_learning_solver.solve()

                if solution != 'NoSol':
                    print(len(solution))
                    for i in range(len(solution)):
                        gameSokoban.fill_screen_with_ground(size, screen)
                        gameSokoban.print_game(screen)
                        gameSokoban.update_player_position()
                        pygame.display.flip()
                        if(solution[i] == "L"):
                            gameSokoban.move(0, -1, list_dock)
                            if gameSokoban.player:
                                gameSokoban.player.set_direction("left")
                            time.sleep(0.1)
                        elif(solution[i] == "R"):
                            gameSokoban.move(0, 1, list_dock)
                            if gameSokoban.player:
                                gameSokoban.player.set_direction("right")
                            time.sleep(0.1)
                        elif(solution[i] == "U"):
                            gameSokoban.move(-1, 0, list_dock)
                            if gameSokoban.player:
                                gameSokoban.player.set_direction("up")
                            time.sleep(0.1)
                        elif(solution[i] == "D"):
                            gameSokoban.move(1, 0, list_dock)
                            if gameSokoban.player:
                                gameSokoban.player.set_direction("down")
                            time.sleep(0.1)

            if event.type == pygame.QUIT:
                    running = False

        # Kiểm tra nếu trò chơi đã hoàn thành
        if gameSokoban.is_completed(list_dock):
            if not game_completed:  # Nếu game chưa hoàn thành
                win_start_time = pygame.time.get_ticks()  # Ghi lại thời gian khi game hoàn thành
                game_completed = True  # Đánh dấu game đã hoàn thành

        # Nếu game đã hoàn thành và 2 giây đã trôi qua, hiển thị màn hình chiến thắng
        if game_completed and pygame.time.get_ticks() - win_start_time >= 100:
            show_win_game(screen)  # Hiển thị màn hình chiến thắng

    pygame.quit()
    launch_level_selector()


def show_main_menu():
    main_menu = tk.Tk()
    main_menu.title("Sokoban Game")

    window_width = 576
    window_height = 512
    main_menu.geometry(f"{window_width}x{window_height}")

    # Load ảnh và resize về đúng kích thước cửa sổ
    bg_image = Image.open("assets/background.png")  # Thay bằng đúng đường dẫn ảnh của bạn
    bg_image = bg_image.resize((window_width, window_height))  # Resize ảnh mượt

    bg_photo = ImageTk.PhotoImage(bg_image)

    # Đặt ảnh làm nền
    bg_label = tk.Label(main_menu, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


     # Load ảnh cho nút Play
    play_img = Image.open("assets/button.png") 
    play_img = play_img.resize((70, 70))  
    play_photo = ImageTk.PhotoImage(play_img)

    # Tạo nút Play bằng ảnh
    play_button = tk.Button(main_menu,
    image=play_photo,
    borderwidth=0,
    highlightthickness=0,
    bg="white",
    activebackground="white",
    command=lambda: [main_menu.destroy(), launch_level_selector()])
    play_button.place(relx=0.5, rely=0.4, anchor="center")

    # Giữ ảnh trong bộ nhớ
    bg_label.image = bg_photo

    main_menu.mainloop()


def launch_level_selector():
    root = tk.Tk()
    root.title("Choose Level")
    window_width, window_height = 576, 512
    root.geometry(f"{window_width}x{window_height}")

    # Load ảnh nền
    bg_image = Image.open("assets/background_levels.png").resize((window_width, window_height))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Thiết lập size nút level
    level_size = 60
    level_spacing = 20
    cols, rows = 3, 3
    total_width = cols * level_size + (cols - 1) * level_spacing
    total_height = rows * level_size + (rows - 1) * level_spacing
    start_x = (window_width - total_width) // 2
    start_y = (window_height - total_height) // 2

    # Load ảnh nút level
    level_img = Image.open("assets/level.png").resize((level_size, level_size))
    level_photo = ImageTk.PhotoImage(level_img)

    # Danh sách giữ ảnh tránh bị xóa
    photo_refs = []

    # Tạo các nút level
    for i in range(1, 10):
        level_name = f"level{i}"
        row = (i - 1) // 3
        col = (i - 1) % 3
        x = start_x + col * (level_size + level_spacing)
        y = start_y + row * (level_size + level_spacing)

        btn = tk.Button(
            root,
            image=level_photo,
            text=str(i),
            compound="center",  # Text nằm giữa ảnh
            fg="green",
            font=("Minecraft", 14, "bold"),
            width=level_size, height=level_size,
            borderwidth=0, highlightthickness=0,
            command=lambda lvl=level_name: [root.destroy(), start_game(lvl)]
        )
        btn.place(x=x, y=y)

        # Lưu ảnh tham chiếu
        btn.image = level_photo
        photo_refs.append(level_photo)

    # Nút quay lại
    back_img = Image.open("assets/back.png").resize((40, 40))
    back_photo = ImageTk.PhotoImage(back_img)
    back_button = tk.Button(
        root, image=back_photo,
        borderwidth=0, highlightthickness=0,
        command=lambda: [root.destroy(), show_main_menu()]
    )
    back_button.place(x=20, y=window_height - 80)
    back_button.image = back_photo
    photo_refs.append(back_photo)

    bg_label.image = bg_photo
    root.mainloop()



# Chạy chương trình
if __name__ == "__main__":
    show_main_menu()




    
    




