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

- Thiếu ảnh 02-actions-buoc-2, 03-actions-buoc-3, 04-curl-api và 05-cloud-storage.
- Browser Use kết nối được Brave, nhưng quyền đọc github.com và ap-southeast-1.console.aws.amazon.com đã bị từ chối. Chỉ tiếp tục chụp sau khi người dùng bỏ chặn và xác nhận.
- Ảnh trình duyệt phải kèm URL theo quy định. Ảnh API phải thấy hai lệnh curl, IP VM và kết quả. Ảnh S3 cần thấy dữ liệu dvc/ và artifacts/current/model.joblib; có thể tách 05a/05b theo hướng dẫn.
- Ảnh 01 gửi trong chat trước đây có đủ metrics/params nhưng sort Created; hướng dẫn chi tiết yêu cầu F1 giảm dần, nên cần kiểm tra/chụp lại.
- Chưa nộp vlearn.dev hoặc xác minh mở repo ẩn danh. Không đánh dấu đã nộp.
- Bonus không nằm trong phạm vi hoàn thiện tiêu chí chính.
