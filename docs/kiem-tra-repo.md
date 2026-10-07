# Kết quả kiểm tra lab — 07/10/2026

## Phần đã hoàn thành

- MLflow: ba cấu hình khác nhau, đủ F1/accuracy; có ảnh 01 và báo cáo phân tích.
- CI/CD: Train và Release sử dụng environment S3lab; Unit Test → Train → Quality Gate → Release.
- [Quality gate](https://github.com/zewolkt3939/K4-L3-DAY21-NguyenTruongBao-2A202602540-CI-CD-for-AI-Systems/actions/runs/37634935302): F1=0, accuracy=0.752; Train success, gate failure, Release skipped.
- [Bước 2](https://github.com/zewolkt3939/K4-L3-DAY21-NguyenTruongBao-2A202602540-CI-CD-for-AI-Systems/actions/runs/37634963032): 22.361 mẫu, F1=0.7149321266968326, accuracy=0.874; cả bốn jobs success.
- [Bước 3](https://github.com/zewolkt3939/K4-L3-DAY21-NguyenTruongBao-2A202602540-CI-CD-for-AI-Systems/actions/runs/37635481166): commit 3fe6714 chỉ đổi data/train_batch1.csv.dvc, 44.722 mẫu; report F1=0.7354260089686099, accuracy=0.882.
- EC2 gắn income-api-read-model, IMDSv2 required; income-api dùng role tải model S3.
- Security group đã bổ sung TCP 8080 từ IP máy kiểm tra 118.71.118.123/32 (rule sgr-01d5f8a50b61b3c34). Cả healthz và score qua public IP EC2 đã trả kết quả hợp lệ.
- Hash CSV local khớp DVC pointer. Không chạy append_batch lần nữa.
- Reports và trạng thái Actions được lưu tại nop-bai/ket-qua/; không chứa credentials.

## Hồ sơ cần hoàn thiện

- Đã kiểm tra ảnh 02, 03, 04 đạt yêu cầu. Hai ảnh 05a/05b hiển thị object dữ liệu DVC có hash khớp con trỏ và artifacts/current/model.joblib, có URL và tên bucket. Tất cả ảnh dưới 1 MB.
- Ảnh 01 đã chụp lại trực tiếp từ MLflow, F1 giảm dần, đủ accuracy và ba cột tham số.
- Công cụ Computer Use hiện lỗi: `Computer Use native pipe is unavailable` (os error 2), nên chưa thể tự chụp lại MLflow hoặc thao tác nộp bài trên vlearn.dev.
- Đã xuất nop-bai/bao-cao.pdf từ bao-cao.md; kiểm tra đúng một trang A4 và xem ảnh render để xác nhận bố cục.
- Chưa nộp vlearn.dev hoặc xác minh mở repo ẩn danh. Không đánh dấu đã nộp.
- Bonus không nằm trong phạm vi hoàn thiện tiêu chí chính.
