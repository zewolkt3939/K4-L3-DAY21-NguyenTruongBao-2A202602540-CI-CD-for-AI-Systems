# Thực hiện lab trên AWS (Windows + Ubuntu EC2)

Code và workflow đã hoàn thiện. Các bước dưới đây cần tài khoản AWS/GitHub của bạn.
Chưa có kết quả triển khai cloud cho đến khi bạn tạo S3, EC2 và chạy Actions.

## 1. Chuẩn bị tài khoản và hạ tầng

1. Đăng nhập AWS Console, chọn region `ap-southeast-1` (Singapore).
2. S3 → Create bucket → General purpose. Đặt tên duy nhất, giữ Block all public access,
   bật Versioning và encryption SSE-S3. Ghi lại tên bucket.
3. IAM → Roles → Create role → AWS service → EC2. Tạo role `income-api-read-model`;
   thêm inline policy từ `docs/aws-ec2-policy.json`, thay `REPLACE_BUCKET_NAME`.
   Role này cho API đọc model bằng temporary credentials; không cần copy access key vào VM.
4. EC2 → Launch instance: Ubuntu Server 24.04 LTS (Python 3.12), x86_64,
   instance có khoảng 2 GiB RAM để cài dependencies. Chọn key pair và tải `.pem`.
   Giữ file key bên ngoài repo. Bật public IP, mã hóa root EBS, yêu cầu IMDSv2.
   Advanced details → IAM instance profile → role vừa tạo.
5. Security group: SSH 22 từ IP của bạn; TCP 8080 từ IP của bạn để gọi API.
   GitHub Actions cũng phải truy cập được SSH: dùng runner có IP cố định và whitelist IP đó,
   hoặc mở rule SSH tạm thời cho lần chạy lab rồi thu hẹp/xóa sau khi chụp bằng chứng.
6. Ghi lại IP public của EC2, username `ubuntu`, tên bucket và region.

EC2, EBS, IPv4 public, dung lượng/request S3 có thể phát sinh phí; kiểm tra credits
và trang giá trong tài khoản trước khi tạo. Sau khi nộp bài, terminate EC2,
kiểm tra EBS/IP còn tồn tại, xóa object và các version S3 nếu không cần giữ.

Nguồn: [S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/GetStartedWithS3.html),
[EC2 IAM roles](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html),
[EC2 pricing](https://aws.amazon.com/ec2/pricing/on-demand/),
[S3 pricing](https://aws.amazon.com/s3/pricing/).

## 2. Credentials cho máy local và GitHub Actions

Tạo IAM principal riêng cho lab với policy `docs/aws-ci-policy.json` sau khi thay tên bucket.
Tạo access key cho principal này để dùng trong lab. Không dùng root access key.
Trên PowerShell, nhập credentials qua `Read-Host` để không ghi key vào lịch sử lệnh:

```powershell
if (-not (Test-Path '.venv')) { python -m venv .venv }
$env:AWS_ACCESS_KEY_ID = Read-Host 'AWS access key ID'
$secureKey = Read-Host 'AWS secret access key' -AsSecureString
$env:AWS_SECRET_ACCESS_KEY = [System.Net.NetworkCredential]::new('', $secureKey).Password
$env:AWS_DEFAULT_REGION = 'ap-southeast-1'
$env:ARTIFACT_BUCKET = 'TEN_BUCKET_THAT'
.\.venv\Scripts\python.exe -m pip install --progress-bar off --no-cache-dir -r requirements-aws.txt
```

GitHub → Settings → Secrets and variables → Actions, thêm năm secrets:

| Secret | Giá trị |
|---|---|
| STORAGE_CREDENTIALS | JSON `{"aws_access_key_id":"...","aws_secret_access_key":"..."}`; thêm `aws_session_token` nếu dùng credentials tạm thời |
| ARTIFACT_BUCKET | Tên bucket |
| SERVER_HOST | Public IPv4 EC2 |
| SERVER_USER | `ubuntu` |
| SERVER_SSH_KEY | Toàn bộ private key `.pem` của key pair EC2 |

Repository variable: `AWS_REGION=ap-southeast-1`.
Credentials tạm thời phải còn hiệu lực khi workflow chạy.

## 3. Chạy local và đưa dữ liệu lên S3

```powershell
.\.venv\Scripts\python.exe prepare_data.py
.\.venv\Scripts\python.exe -m pytest tests/ -v
.\.venv\Scripts\python.exe -m src.experiments
.\.venv\Scripts\mlflow.exe ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1
```

Mở http://127.0.0.1:5000, chọn experiment `adult-income`, hiển thị params,
`f1_score`, `accuracy`, chụp `01-mlflow-ui.png`.

Nếu `.dvc/` chưa tồn tại, chạy `.\.venv\Scripts\dvc.exe init` trước.
Sau đó cấu hình remote và track dữ liệu:

```powershell
$env:PATH = "$PWD\.venv\Scripts;$env:PATH"
python -m src.configure_dvc
dvc add data/train_batch1.csv data/holdout.csv data/train_batch2.csv
dvc push
```

Remote được ghi vào `.dvc/config.local` để không commit credentials. Workflow tự cấu hình
remote theo `ARTIFACT_BUCKET`, nên chỉ cần commit `.dvc/` metadata và các file `.dvc`.

## 4. Cấu hình EC2 một lần

Từ PowerShell, thay đường dẫn key và IP thật:

```powershell
scp -i 'C:\duong-dan\income.pem' -r src scripts requirements-serve.txt ubuntu@IP_EC2:~/income-app/
ssh -i 'C:\duong-dan\income.pem' ubuntu@IP_EC2
```

Nếu thư mục chưa tồn tại, SSH trước và chạy `mkdir -p ~/income-app`, rồi chạy lại scp.
Trong terminal SSH:

```bash
cd ~/income-app
bash scripts/setup_vm.sh TEN_BUCKET_THAT ap-southeast-1
```

Script tạo venv, systemd service và quyền restart service cho deployment.
Service được khởi động bởi Release sau khi model đã được upload.

## 5. Chạy pipeline Bước 2

```powershell
git add .
git commit -m 'feat: complete income model CI/CD for AWS'
git push origin main
```

Vào Actions → Income Model CI/CD. Chờ bốn jobs màu xanh, tải artifact `report`,
điền số liệu Bước 2 vào báo cáo và chụp `02-actions-buoc-2.png`.
Workflow giữ model trong GitHub artifact đến khi quality gate qua; chỉ job Release
mới ghi `artifacts/current/model.joblib`. Mỗi model cũng được lưu theo run ID trên S3.

Để chứng minh quality gate chặn triển khai, có thể chạy một pipeline riêng với
`n_estimators: 1`, `learning_rate: 0.01`, `max_depth: 1`. Kiểm tra report thực tế;
khi F1 dưới 0.65, Quality Gate phải đỏ và Release phải skipped. Khôi phục bộ tham số
đã chọn, commit/push và chờ pipeline xanh trước khi thực hiện Bước 3.

## 6. Bước 3: thêm dữ liệu và kích hoạt lại

Thực hiện một lần sau khi Bước 2 thành công:

```powershell
python append_batch.py
dvc add data/train_batch1.csv
dvc push
git add data/train_batch1.csv.dvc
git commit -m 'data: add 22361 new Adult samples'
git push origin main
```

`dvc push` phải hoàn thành trước `git push`. Chụp `03-actions-buoc-3.png`, tải report,
điền metrics Bước 3 và nhận xét theo số liệu thực tế. Script append sẽ từ chối
chạy lần hai nếu kích thước batch1 đã thay đổi so với lô ban đầu.

## 7. Kiểm tra API và nộp bài

```powershell
$vmAddress = 'IP_EC2'
Invoke-RestMethod "http://${vmAddress}:8080/healthz"
$payload = @{features=@(28,2,14,2,11,0,1,0,0,45)} | ConvertTo-Json
Invoke-RestMethod "http://${vmAddress}:8080/score" -Method Post -ContentType 'application/json' -Body $payload
```

Nếu rubric yêu cầu lệnh curl, dùng `curl.exe` trên Windows hoặc chạy hai lệnh trong
`tasks/buoc-3.md` trên terminal Linux. Lưu ảnh kết quả với IP vào `04-curl-api.png`.
Chụp S3 Console thấy `dvc/` và `artifacts/current/model.joblib` thành `05-cloud-storage.png`.

Điền báo cáo bằng kết quả thật, commit `nop-bai/`, kiểm tra repo public và nộp URL repo lên vlearn.dev.
Các ô Bước 2/Bước 3 còn trống phải được thay bằng report từ hai lần Actions, không dùng
kết quả mô phỏng local để chứng minh triển khai cloud.
