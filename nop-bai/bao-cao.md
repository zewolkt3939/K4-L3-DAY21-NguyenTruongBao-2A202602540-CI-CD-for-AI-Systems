# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Nguyễn Trường Bảo |
| MSSV | 2A202602540 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/zewolkt3939/K4-L3-DAY21-NguyenTruongBao-2A202602540-CI-CD-for-AI-Systems |
| Ngày nộp | Chưa nộp |

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.1 | 5 | 0.7149 | 0.8740 |

**Bộ đã chọn:** `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`.

Lần 3 có F1 cao nhất (0,7149), vượt ngưỡng 0,65. Lần 1 có accuracy cao hơn
(0,8780 so với 0,8740), nhưng F1 thấp hơn (0,7109). Vì mục tiêu là nhận diện
lớp thu nhập cao, tôi chọn theo F1. Lợi thế chỉ khoảng 0,004 trên holdout
500 mẫu nên chưa chứng minh sự vượt trội trên mọi dữ liệu. Cấu hình 50 cây,
learning_rate 0,05 cho F1 thấp nhất: giảm learning_rate cần thêm vòng boosting
để mô hình học đủ. Các lần chạy được lưu trong experiment `adult-income` của MLflow.

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Lớp thu nhập trên 50K chiếm khoảng 24,8%. Mô hình luôn dự đoán thu nhập thấp
vẫn đạt accuracy khoảng 75,2%, nhưng F1 của lớp dương bằng 0 vì bỏ sót toàn
bộ người thu nhập cao. F1 kết hợp precision và recall, phản ánh khả năng
nhận diện lớp cần quan tâm. Pipeline dùng `f1_score(y_eval, preds)` cho
`target=1`, yêu cầu F1 từ 0,65 trở lên. Weighted-F1 chịu ảnh hưởng tỉ lệ lớp;
macro-F1 trung bình hai lớp. Cả hai đều khác F1 riêng của lớp dương nên không
được dùng thay chỉ số đã chọn. Accuracy vẫn được log để đối chiếu.

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| MLflow không import/chạy SQLite | Setuptools và SQLAlchemy mới bỏ API mà MLflow 2.13 cần | Cố định Setuptools 80.9.0, SQLAlchemy 2.0.30; 12 kiểm thử đã qua. |
| Dependency DVC không build trên Windows | Đường dẫn thư mục tạm quá dài | Dùng thư mục Temp ngắn; cố định bộ SDK S3 tương thích. |
| Khung workflow ghi đè model trước quality gate | Upload nằm trong job Train | Giữ model ở GitHub artifact; chỉ publish trong Release sau khi gate qua. |

## 4. So Sánh Bước 2 và Bước 3

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ train_batch1) | Chờ Actions | Chờ Actions |
| Bước 3 (thêm train_batch2) | Chờ Actions | Chờ Actions |

Chưa triển khai AWS nên chưa có kết quả từ hai lần GitHub Actions để điền
bảng này. Sau khi tạo S3, EC2 và Secrets, lấy số liệu thật từ artifact
`report` của từng lần chạy. Giữ nguyên holdout khi so sánh; thêm dữ liệu
cùng phân phối không đảm bảo F1 sẽ tăng.
