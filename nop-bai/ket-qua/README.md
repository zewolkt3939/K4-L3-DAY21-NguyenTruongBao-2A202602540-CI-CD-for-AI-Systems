# Bằng chứng bổ sung từ pipeline thật

Các JSON report được tải từ GitHub Actions artifacts; các JSON run ghi trạng thái jobs thực tế. Đây là bằng chứng bổ sung, không thay thế chuỗi ảnh rubric.

| Kiểm chứng | Run | Report |
|---|---|---|
| Model yếu bị chặn | [37634935302](https://github.com/zewolkt3939/K4-L3-DAY21-NguyenTruongBao-2A202602540-CI-CD-for-AI-Systems/actions/runs/37634935302) | [quality-gate-report.json](quality-gate-report.json) |
| Bước 2, dữ liệu ban đầu | [37634963032](https://github.com/zewolkt3939/K4-L3-DAY21-NguyenTruongBao-2A202602540-CI-CD-for-AI-Systems/actions/runs/37634963032) | [buoc-2-report.json](buoc-2-report.json) |
| Bước 3, commit chỉ cập nhật dữ liệu | [37635481166](https://github.com/zewolkt3939/K4-L3-DAY21-NguyenTruongBao-2A202602540-CI-CD-for-AI-Systems/actions/runs/37635481166) | [buoc-3-report.json](buoc-3-report.json) |

[api-public.txt](api-public.txt) ghi kết quả thật gọi API bằng IP public EC2. Khi chụp 04, chạy hai lệnh curl trong terminal Windows và giữ IP cùng kết quả trong ảnh:

```powershell
curl.exe http://18.142.249.146:8080/healthz
curl.exe -X POST http://18.142.249.146:8080/score -H 'Content-Type: application/json' -d '{"features":[28,2,14,2,11,0,1,0,0,45]}'
```

Port 8080 chỉ cho phép IP public máy kiểm tra tại thời điểm cấu hình; khi đổi mạng cần cập nhật rule /32 tương ứng.
