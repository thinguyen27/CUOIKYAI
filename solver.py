import copy
import time
import queue
from collections import deque
import math
import random
import numpy as np
import pygame

class QLearningAgent:
    def __init__(self, state_space, action_space, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha  # Tỷ lệ học
        self.gamma = gamma  # Hệ số chiết khấu
        self.epsilon = epsilon  # Tỷ lệ khám phá (exploration)

        self.state_space = state_space  # Không gian trạng thái
        self.action_space = action_space  # Không gian hành động

        # Khởi tạo bảng Q với giá trị 0 cho mỗi trạng thái-hành động
        self.q_table = np.zeros((state_space, action_space))

    def encode_state(self, state):
        """
        Mã hóa trạng thái (ma trận trò chơi) thành một số nguyên duy nhất.
        Giả sử state là ma trận 2D chứa các ký tự như '#', '@', '$', '.', v.v.
        """
        state_flat = []
        
        for row in state:
            for char in row:
                # Mã hóa các ký tự thành các giá trị số tương ứng
                if char == '#':  # Tường
                    state_flat.append(1)
                elif char == '@':  # Người chơi
                    state_flat.append(2)
                elif char == '$':  # Thùng
                    state_flat.append(3)
                elif char == '.':  # Dock
                    state_flat.append(4)
                elif char == '*':  # Thùng ở Dock
                    state_flat.append(5)
                else:  # Không gian trống
                    state_flat.append(0)

        # Chuyển đổi state thành mảng 1D
        state_array = np.array(state_flat)
        
        # Mã hóa trạng thái thành một số nguyên (hash) duy nhất và sử dụng modulo để giới hạn chỉ số
        state_hash = hash(tuple(state_array)) % self.state_space  # Giới hạn chỉ số vào phạm vi của bảng Q
        return state_hash

    def choose_action(self, state):
        # Mã hóa trạng thái trước khi lấy hành động
        state_hash = self.encode_state(state)
        
        # Kiểm tra xem trạng thái đã tồn tại trong bảng Q chưa
        if state_hash < len(self.q_table):
            if random.uniform(0, 1) < self.epsilon:
                return random.choice(range(self.action_space))  # Chọn hành động ngẫu nhiên
            else:
                return np.argmax(self.q_table[state_hash])  # Chọn hành động có giá trị Q cao nhất
        else:
            return random.choice(range(self.action_space))  # Nếu chưa có trạng thái trong bảng, chọn ngẫu nhiên

    def update_q_value(self, state, action, reward, next_state):
        # Mã hóa trạng thái
        state_hash = self.encode_state(state)
        next_state_hash = self.encode_state(next_state)

        # Cập nhật giá trị Q
        best_next_action = np.argmax(self.q_table[next_state_hash])  # Tìm hành động tốt nhất từ trạng thái tiếp theo
        self.q_table[state_hash, action] += self.alpha * (reward + self.gamma * self.q_table[next_state_hash, best_next_action] - self.q_table[state_hash, action])

# Thêm vào trong lớp Solve hoặc như một phần của QLearningSolver
class QLearningSolver:
    def __init__(self, game, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.game = game  # Trò chơi Sokoban
        self.alpha = alpha  # Tỷ lệ học
        self.gamma = gamma  # Hệ số chiết khấu
        self.epsilon = epsilon  # Tỷ lệ khám phá (exploration)
        
        # Tạo tác nhân Q-learning
        self.agent = QLearningAgent(state_space=1000, action_space=4)  # Điều chỉnh state_space và action_space phù hợp

    def train(self, screen):
        """
        Phương thức huấn luyện Q-learning liên tục cho đến khi người dùng dừng (nhấn F1).
        """
        episode = 0
        running = True
        while running:  # Vòng lặp huấn luyện vô hạn
            episode += 1
            state = self.game.reset()  # Khởi tạo trạng thái ban đầu
            done = False
            total_reward = 0

            while not done:
                # Mã hóa trạng thái thành chỉ số duy nhất
                state_hash = self.agent.encode_state(state)  # Mã hóa trạng thái thành số nguyên
                
                # Chọn hành động từ bảng Q (epsilon-greedy)
                action = self.agent.choose_action(state)  # Lựa chọn hành động
                
                # Thực hiện hành động và nhận trạng thái tiếp theo
                next_state, reward, done = self.game.step(action)
                
                # Cập nhật giá trị Q
                self.agent.update_q_value(state, action, reward, next_state)
                
                # Cập nhật trạng thái hiện tại và tính tổng phần thưởng
                state = next_state
                total_reward += reward

            print(f"Episode {episode}, Total Reward: {total_reward}")

            # Kiểm tra sự kiện bàn phím (F1 để dừng)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:  # Nhấn F1 để dừng huấn luyện
                        print("Training stopped by user (F1 pressed).")
                        running = False
    def solve(self):
        state = self.game.reset()  # Khởi tạo trạng thái ban đầu
        done = False
        path = []
        max_steps = 1000  # Giới hạn số bước tối đa trong mỗi vòng

        while not done and max_steps > 0:
            # Mã hóa trạng thái thành chỉ số duy nhất
            state_hash = self.agent.encode_state(state)  # Mã hóa trạng thái thành số nguyên
            
            # Lựa chọn hành động tốt nhất từ bảng Q
            action = np.argmax(self.agent.q_table[state_hash])  # Tìm hành động có giá trị Q cao nhất
            
            # Thực hiện hành động và nhận trạng thái tiếp theo
            next_state, reward, done = self.game.step(action)
            path.append(action)
            state = next_state  # Cập nhật trạng thái hiện tại

            max_steps -= 1  # Giảm số bước còn lại

        return path





class Solve:
    def __init__(self, matrix):
        self.matrix = matrix
        self.pathSolution = ""
        self.dockListPosition = self.dockPosition()
        self.heuristic = 0

    def __lt__(self,other):
        return self.heuristic < other.heuristic

    def getMatrix(self):
        return self.matrix

    def getMatrixElement(self, y, x):
        return self.matrix[y][x]

    def setMatrixElement(self, y, x, object_map):
        self.matrix[y][x] = object_map

    def getElementNextStep(self, y, x):
        new_y, new_x = self.playerPosition()[0] + y, self.playerPosition()[1] + x
        return self.getMatrixElement(new_y, new_x)

    def playerPosition(self):
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char == '@':
                    return y, x

    def boxPosition(self):
        boxListPosition = []
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char == '$':
                    boxListPosition.append((y, x))
        return boxListPosition

    def dockPosition(self):
        dockListPosition = []
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char == '.':
                    dockListPosition.append((y, x))
        return dockListPosition
    
    def playerCanMove(self, y, x):
        return self.getElementNextStep(y, x) in [' ', '.']

    def playerCanPushBox(self, y, x):
        return self.getElementNextStep(y, x) in ['*', '$'] and self.getElementNextStep(y + y, x + x) in ['.', ' ']

    def isComplete(self):
        for y in self.matrix:
            for x in y:
                if x == '$':
                    return False
        return True

    def moveBox(self, y_box, x_box, move_y, move_x):
        box_element = self.getMatrixElement(y_box, x_box)
        next_box_element = self.getMatrixElement(y_box + move_y, x_box + move_x)
        if box_element == '$':
            if next_box_element == ' ':
                self.setMatrixElement(y_box, x_box, ' ')
                self.setMatrixElement(y_box + move_y, x_box + move_x, '$')
            elif next_box_element == '.':
                self.setMatrixElement(y_box, x_box, ' ')
                self.setMatrixElement(y_box + move_y, x_box + move_x, '*')
        elif box_element == '*':
            if next_box_element == ' ':
                self.setMatrixElement(y_box, x_box, '.')
                self.setMatrixElement(y_box + move_y, x_box + move_x, '$')
            elif next_box_element == '.':
                self.setMatrixElement(y_box, x_box, '.')
                self.setMatrixElement(y_box + move_y, x_box + move_x, '*')

    def move(self, y, x):
        if self.playerCanMove(y, x):
            player_position = self.playerPosition()
            self.setMatrixElement(player_position[0] + y, player_position[1] + x, '@')
            self.setMatrixElement(player_position[0], player_position[1], ' ')
        elif self.playerCanPushBox(y, x):
            player_position = self.playerPosition()
            self.moveBox(player_position[0] + y, player_position[1] + x, y, x)
            self.setMatrixElement(player_position[0] + y, player_position[1] + x, '@')
            self.setMatrixElement(player_position[0], player_position[1], ' ')

        for i, j in self.dockListPosition:
            if self.getMatrixElement(i, j) not in ['*', '@']:
                self.setMatrixElement(i, j, '.')

    def printState(self):
        for row in self.matrix:
            print(" ".join(row))
        print()

def validMove(state):
    moves = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1)
    }

    valid_moves = []

    for step, (y, x) in moves.items():
        if state.playerCanMove(y, x) or state.playerCanPushBox(y, x):
            valid_moves.append(step)

    return valid_moves

def box_toDock(state):
    sum = 0
    box_list = state.boxPosition()
    dock_list = state.dockPosition()
    for box in box_list:
        min_distance = float('inf')
        for dock in dock_list:
            distance = (abs(dock[0] - box[0]) + abs(dock[1] - box[1]))
            if distance < min_distance:
                min_distance = distance
        sum += min_distance
    return sum

def player_toBox(state):
    sum = 0
    box_list = state.boxPosition()
    player_pos = state.playerPosition()
    for box in box_list:
        sum += abs(box[0] - player_pos[0]) + abs(box[1] - player_pos[1])
    return sum

def isDeadlock(state):
    boxListPosition = state.boxPosition()

    deadlock_conditions = [
        # Goc tren ben trai
        lambda box_y, box_x: (
                state.getMatrixElement(box_y, box_x - 1) in ['#', '$', '*'] and
                state.getMatrixElement(box_y - 1, box_x) in ['#', '$', '*'] and
                state.getMatrixElement(box_y - 1, box_x - 1) in ['#', '$', '*']
        ),
        # Goc tren ben phai
        lambda box_y, box_x: (
                state.getMatrixElement(box_y, box_x + 1) in ['#', '$', '*'] and
                state.getMatrixElement(box_y - 1, box_x) in ['#', '$', '*'] and
                state.getMatrixElement(box_y - 1, box_x + 1) in ['#', '$', '*']
        ),
        # Goc duoi ben trai
        lambda box_y, box_x: (
                state.getMatrixElement(box_y, box_x - 1) in ['#', '$', '*'] and
                state.getMatrixElement(box_y + 1, box_x) in ['#', '$', '*'] and
                state.getMatrixElement(box_y + 1, box_x - 1) in ['#', '$', '*']
        ),
        # Goc duoi ben phai
        lambda box_y, box_x: (
                state.getMatrixElement(box_y, box_x + 1) in ['#', '$', '*'] and
                state.getMatrixElement(box_y + 1, box_x) in ['#', '$', '*'] and
                state.getMatrixElement(box_y + 1, box_x + 1) in ['#', '$', '*']
        ),
    ]

    for box in boxListPosition:
        y, x = box

        if any(condition(y, x) for condition in deadlock_conditions):
            return True

    return False

# Hàm BFS
def bfs(game):
    start = time.time()
    node_generated = 0
    start_state = copy.deepcopy(game)
    node_generated += 1

    if isDeadlock(start_state):
        print("No Solution!")
        return "NoSol"

    queue = deque([start_state])
    visited = set()
    visited.add(tuple(map(tuple, start_state.getMatrix())))

    print("Processing BFS......")

    while queue:
        currState = queue.popleft()
        move = validMove(currState)
        for step in move:
            newState = copy.deepcopy(currState)
            node_generated += 1

            if step == 'U':
                newState.move(-1, 0)
            elif step == 'D':
                newState.move(1, 0)
            elif step == 'L':
                newState.move(0, -1)
            elif step == 'R':
                newState.move(0, 1)

            newState.pathSolution += step

            if newState.isComplete():
                end = time.time()
                print("Time to find solution:", round(end - start, 10), "seconds")
                print("Solution:", newState.pathSolution)
                return newState.pathSolution

            if (tuple(map(tuple, newState.getMatrix())) not in visited) and (not isDeadlock(newState)):
                queue.append(newState)
                visited.add(tuple(map(tuple, newState.getMatrix())))

    print("No Solution!")
    return "NoSol"

# Hàm A*
def astar(game):
    start = time.time()
    node_generated = 0
    start_state = copy.deepcopy(game)
    node_generated += 1
    start_state.heuristic = player_toBox(start_state) + box_toDock(start_state)

    if isDeadlock(start_state):
        print("No Solution!")
        return "NoSol"

    open_list = queue.PriorityQueue()
    open_list.put(start_state)
    close_list = set()

    print("Processing A*......")

    while not open_list.empty():
        cur_state = open_list.get()
        move = validMove(cur_state)
        close_list.add(tuple(map(tuple, cur_state.getMatrix())))

        for step in move:
            new_state = copy.deepcopy(cur_state)
            node_generated += 1

            if step == 'U':
                new_state.move(-1, 0)
            elif step == 'D':
                new_state.move(1, 0)
            elif step == 'L':
                new_state.move(0, -1)
            elif step == 'R':
                new_state.move(0, 1)

            new_state.pathSolution += step
            new_state.heuristic = player_toBox(new_state) + box_toDock(new_state)

            if new_state.isComplete():
                end = time.time()
                print("Time to find solution:", round(end - start, 10), "seconds")
                print("Solution:", new_state.pathSolution)
                return new_state.pathSolution

            if (tuple(map(tuple, new_state.getMatrix())) not in close_list) and not isDeadlock(new_state):
                open_list.put(new_state)

    print("No Solution!")
    return "NoSol"

# Hàm Backtracking
def backtracking(game):
    start = time.time()
    node_generated = 0
    start_state = copy.deepcopy(game)
    visited = set()

    if isDeadlock(start_state):
        print("No Solution!")
        return "NoSol"

    print("Processing Backtracking......")

    def solve(state):
        nonlocal node_generated

        # Nếu hoàn thành, trả về đường đi
        if state.isComplete():
            return state.pathSolution

        # Lưu trạng thái vào visited
        visited.add(tuple(map(tuple, state.getMatrix())))

        # Thử từng bước đi khả dụng
        for step in validMove(state):
            newState = copy.deepcopy(state)
            node_generated += 1

            # Thực hiện bước đi
            if step == 'U':
                newState.move(-1, 0)
            elif step == 'D':
                newState.move(1, 0)
            elif step == 'L':
                newState.move(0, -1)
            elif step == 'R':
                newState.move(0, 1)

            newState.pathSolution += step

            # Kiểm tra deadlock hoặc trạng thái đã ghé qua
            if tuple(map(tuple, newState.getMatrix())) in visited or isDeadlock(newState):
                continue

            # Đệ quy tìm giải pháp từ trạng thái mới
            solutionPath = solve(newState)
            if solutionPath:  # Nếu tìm được giải pháp, trả về
                return solutionPath

        # Không tìm thấy đường đi, quay lui
        return None

    # Bắt đầu giải bài toán
    solution = solve(start_state)
    end = time.time()

    if solution:
        print("Time to find solution:", round(end - start, 10), "seconds")
        print("Solution:", solution)
        return solution
    else:
        print("No Solution!")
        return "NoSol"

# Hàm Simulated Annealing
def simulated_annealing(game, initial_temperature=1000, cooling_rate=0.95, max_iterations=2000):
    start = time.time()
    node_generated = 0

    # Sao chép trạng thái ban đầu
    current_state = copy.deepcopy(game)
    node_generated += 1

    # Đặt nhiệt độ ban đầu
    temperature = initial_temperature

    # Đường đi tốt nhất và heuristic ban đầu
    best_path = ""
    best_heuristic = player_toBox(current_state) + box_toDock(current_state)

    print("Processing SIMULATED ANNEALING......")

    for _ in range(max_iterations):
        # Kiểm tra nếu đã hoàn thành
        if current_state.isComplete():
            end = time.time()
            print("Time to find solution:", round(end - start, 10), "seconds")
            print("Number of visited nodes:", node_generated)
            print("Solution:", best_path, "Number steps:", len(best_path))
            return best_path

        # Lấy tất cả các nước đi hợp lệ
        moves = validMove(current_state)
        if not moves:
            break

        # Chọn ngẫu nhiên một bước đi
        step = random.choice(moves)
        next_state = copy.deepcopy(current_state)
        node_generated += 1

        # Thực hiện bước đi
        if step == 'U':
            next_state.move(-1, 0)
        elif step == 'D':
            next_state.move(1, 0)
        elif step == 'L':
            next_state.move(0, -1)
        elif step == 'R':
            next_state.move(0, 1)

        # Tính toán heuristic của trạng thái tiếp theo
        next_heuristic = player_toBox(next_state) + box_toDock(next_state)

        # Tính toán xác suất chọn trạng thái kém hơn
        delta = next_heuristic - best_heuristic
        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperature):
            current_state = next_state
            best_path += step
            best_heuristic = next_heuristic

        # Giảm nhiệt độ từ từ
        temperature *= cooling_rate

    print("No Solution Found!")
    return "NoSol"


# Belief State Search
def belief_state_search(game):
    start = time.time()
    node_generated = 0
    start_state = copy.deepcopy(game)
    node_generated += 1

    if isDeadlock(start_state):
        print("No Solution!")
        return "NoSol"

    # Giả thuyết về các trạng thái có thể có trong Belief State Search
    belief_states = [start_state]

    print("Processing Belief State Search......")

    while belief_states:
        current_level = []
        for state in belief_states:
            moves = validMove(state)
            for step in moves:
                new_state = copy.deepcopy(state)
                node_generated += 1

                # Thực hiện bước đi
                if step == 'U':
                    new_state.move(-1, 0)
                elif step == 'D':
                    new_state.move(1, 0)
                elif step == 'L':
                    new_state.move(0, -1)
                elif step == 'R':
                    new_state.move(0, 1)

                new_state.pathSolution += step

                if new_state.isComplete():
                    end = time.time()
                    print("Time to find solution:", round(end - start, 10), "seconds")
                    print("Solution:", new_state.pathSolution)
                    return new_state.pathSolution

                # Thêm trạng thái mới vào danh sách belief states
                current_level.append(new_state)

        belief_states = current_level  # Cập nhật lại belief states

    print("No Solution!")
    return "NoSol"
