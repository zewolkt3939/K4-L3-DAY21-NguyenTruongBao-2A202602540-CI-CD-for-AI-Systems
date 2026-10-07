# Báo cáo Day 21 — CI/CD cho AI Systems

**Nguyễn Trường Bảo — MSSV 2A202602540 — K4**
Ngày thực hiện: 07/10/2026
[Repo GitHub](https://github.com/zewolkt3939/K4-L3-DAY21-NguyenTruongBao-2A202602540-CI-CD-for-AI-Systems)

### 1. Thực nghiệm và lựa chọn tham số

| n_estimators | learning_rate | max_depth | F1 | Accuracy |
|---|---|---|---|---|
| 100 | 0.1 | 3 | 0.7109 | 0.878 |
| 50 | 0.05 | 2 | 0.6051 | 0.846 |
| 200 | 0.1 | 5 | 0.7149 | 0.874 |

Chọn 200 cây, learning_rate=0.1, max_depth=5 vì F1 cao nhất và vượt ngưỡng 0.65. Chênh lệch F1 với cấu hình 100 cây chỉ khoảng 0.004 trên holdout 500 mẫu, nên chưa chứng minh ưu thế trên mọi dữ liệu. Các thí nghiệm được ghi trong MLflow adult-income.

### 2. Vì sao dùng F1

Lớp thu nhập cao chiếm khoảng 24.8%; luôn dự đoán thu nhập thấp vẫn đạt accuracy khoảng 75.2% nhưng F1 lớp dương bằng 0. F1 kết hợp precision và recall để đánh giá nhận diện lớp thu nhập cao. Pipeline dùng F1 riêng cho target=1, không dùng weighted-F1 hay macro-F1 thay thế. Accuracy được ghi để đối chiếu.

### 3. Triển khai và kết quả thực tế

| Lần chạy Actions | Mẫu train | F1 | Accuracy |
|---|---|---|---|
| [Bước 2](https://github.com/zewolkt3939/K4-L3-DAY21-NguyenTruongBao-2A202602540-CI-CD-for-AI-Systems/actions/runs/37634963032) | 22,361 | 0.7149 | 0.874 |
| [Bước 3](https://github.com/zewolkt3939/K4-L3-DAY21-NguyenTruongBao-2A202602540-CI-CD-for-AI-Systems/actions/runs/37635481166) | 44,722 | 0.7354 | 0.882 |

Giữ nguyên holdout 500 mẫu và siêu tham số. Thêm dữ liệu giúp F1 tăng 0.0205, accuracy tăng 0.008 trên holdout này; không đảm bảo cải thiện trên mọi tập dữ liệu. Commit Bước 3 chỉ đổi con trỏ DVC train_batch1, kích hoạt Actions bằng push. Reports thật được lưu tại ket-qua/.

[Kiểm chứng quality gate](https://github.com/zewolkt3939/K4-L3-DAY21-NguyenTruongBao-2A202602540-CI-CD-for-AI-Systems/actions/runs/37634935302): model 1 cây, learning_rate=0.01, max_depth=1 có F1=0, accuracy=0.752; Quality Gate thất bại và Release skipped. Bộ tham số tốt đã được khôi phục.

### 4. Khó khăn và cách giải quyết

- MLflow 2.13 gặp xung đột dependencies: pin Setuptools/SQLAlchemy; 12 tests qua.
- Secrets đặt trong environment S3lab nhưng jobs chưa khai báo environment: thêm environment: S3lab cho Train và Release.
- EC2 chưa gắn role đọc S3: gắn income-api-read-model; API tải model bằng instance credentials.
- API public timeout do thiếu rule 8080: mở TCP 8080 chỉ từ IP public máy kiểm tra /32. Healthz và score qua IP EC2 đã trả kết quả hợp lệ; bằng chứng văn bản ở ket-qua/api-public.txt.
