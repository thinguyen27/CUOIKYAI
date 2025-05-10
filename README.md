
# Trò Chơi Đẩy Thùng - Sokoban
![Screenshot 2025-05-10 165359](https://github.com/user-attachments/assets/6fc393d1-ae4f-487d-817c-b47be918c207)

## Mô Tả
Trò chơi Sokoban là một trò chơi trí tuệ với các cấp độ khác nhau, nơi người chơi điều khiển một nhân vật để đẩy các thùng vào đúng vị trí mục tiêu trên bản đồ. Mỗi cấp độ có độ khó tăng dần với sự xuất hiện của các chướng ngại vật và các thùng cần được đẩy đến các ô đích. Trong dự án này, chúng tôi sử dụng các thuật toán trí tuệ nhân tạo để tự động giải quyết trò chơi, bao gồm các thuật toán tìm kiếm như BFS, A*, Backtracking, Simulated Annealing, Belief State Search và Q-Learning.

## Mục Tiêu
- Sử dụng các thuật toán tìm kiếm tối ưu để di chuyển các thùng vào các vị trí mục tiêu trong thời gian ngắn nhất.
- Ứng dụng Q-Learning để tạo ra một tác nhân tự động học cách chơi và tối ưu hóa chiến lược trong trò chơi.

## Các Thuật Toán Được Sử Dụng
- **BFS (Breadth-First Search)**: Thuật toán tìm kiếm theo chiều rộng, đảm bảo tìm được giải pháp với số bước ít nhất trong không gian trạng thái không có trọng số.
- **A***: Thuật toán tìm kiếm có trọng số, sử dụng hàm heuristic để ưu tiên các trạng thái có chi phí ước tính thấp nhất.
- **Backtracking**: Phương pháp tìm kiếm đệ quy, thử từng lựa chọn và quay lại nếu gặp bế tắc.
- **Simulated Annealing**: Thuật toán tối ưu hóa mô phỏng quá trình làm nguội vật liệu, cho phép thoát khỏi các cực trị cục bộ để tìm giải pháp tối ưu.
- **Belief State Search**: Thuật toán tìm kiếm trong không gian trạng thái không chắc chắn, giúp tìm kiếm giải pháp khi không thể xác định chính xác trạng thái môi trường.
- **Q-Learning**: Thuật toán học củng cố không giám sát, giúp tác nhân học cách tối ưu hóa hành động qua các phần thưởng và huấn luyện từ môi trường.

## Công Cụ và Thư Viện
- **Python**: Ngôn ngữ lập trình chính cho dự án.
- **Pygame**: Thư viện đồ họa để tạo giao diện trò chơi.
- **Tkinter**: Thư viện để xây dựng giao diện người dùng (GUI).
- **Pillow**: Thư viện xử lý hình ảnh cho các tài nguyên trò chơi.

## Cài Đặt
### Cài đặt môi trường Python
Đảm bảo rằng bạn đã cài đặt Python 3.x và pip. Nếu chưa, bạn có thể tải và cài đặt từ [python.org](https://www.python.org/).

### Cài đặt các thư viện yêu cầu
Chạy lệnh dưới đây để cài đặt các thư viện cần thiết:
```bash
pip install pygame tkinter pillow
```

## Cách Chạy
1. Tải mã nguồn từ kho lưu trữ (repo).
2. Mở terminal và di chuyển đến thư mục chứa mã nguồn.
3. Chạy tệp **`main.py`** để bắt đầu trò chơi:
```bash
python main.py
```
4. Giao diện trò chơi sẽ xuất hiện. Bạn có thể chọn cấp độ và chơi bằng các phím mũi tên hoặc sử dụng các thuật toán giải quyết tự động bằng các phím số từ 1 đến 6.

## Cấu Trúc Dự Án
```
SokobanAI/
│
├── assets/              # Tài nguyên trò chơi như hình ảnh và âm thanh
├── levels/              # Các bản đồ và màn chơi cho trò chơi
├── load_object/         # Các đối tượng trong trò chơi như thùng gỗ, người chơi
├── solver.py            # Các thuật toán giải quyết trò chơi
├── game.py              # Logic chính của trò chơi
├── layer.py             # Định nghĩa các lớp (layers) trong trò chơi
├── main.py              # Điểm khởi đầu của trò chơi
└── README.md            # Tệp README này
```

## Tương Lai
- **Cải tiến thuật toán**: Tối ưu hóa các thuật toán như Q-Learning để giảm thời gian huấn luyện và cải thiện hiệu suất.
- **Thêm cấp độ**: Tạo thêm các cấp độ mới với độ khó tăng dần để thử thách người chơi.
- **Giao diện người dùng**: Cải thiện giao diện trò chơi để dễ dàng hơn cho người chơi tương tác.

## Liên Hệ
- **Nguyễn Trần Quốc Thi** - nhóm trưởng, **23110331**
- **Trương Gia Vỷ** - **20133115**

## Tài Liệu Tham Khảo
- Watkins, C. J. C. H., & Dayan, P. (1992). *Q-learning*. Machine Learning, 8(3), 279-292.
- Russell, S., & Norvig, P. (2016). *Artificial Intelligence: A Modern Approach* (3rd ed.). Pearson Education.
- Kirkpatrick, S., Gelatt, C. D., & Vecchi, M. P. (1983). *Optimization by Simulated Annealing*. Science, 220(4598), 671-680.
