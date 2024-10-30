
# Tài Liệu API Cho Quản Lý Peers

## 1. Route: **/peer/sign_up**
- **Phương thức:** `POST`
- **Mục đích:** Đăng ký một peer mới vào hệ thống.
  
### Dữ liệu nhận vào:
```json
{
  "name": "string",     // Tên peer (bắt buộc)
  "password": "string"  // Mật khẩu peer (bắt buộc)
}
```

### Dữ liệu trả ra:
- **Thành công (201):**
```json
{
  "message": "Peer signed up successfully",
  "ip_address": "string", // Địa chỉ IP của peer
  "port": "integer"       // Cổng của peer
}
```

- **Lỗi (400):**
```json
{
  "error": "Name already exists"
}
```
```json
{
  "error": "Invalid input, name and password are required"
}
```

---

## 2. Route: **/peer/login**
- **Phương thức:** `POST`
- **Mục đích:** Đăng nhập vào một peer đã tồn tại.

### Dữ liệu nhận vào:
```json
{
  "name": "string",     // Tên peer (bắt buộc)
  "password": "string"  // Mật khẩu peer (bắt buộc)
}
```

### Dữ liệu trả ra:
- **Thành công (201):**
```json
{
  "message": "Peer found",
  "peer_id": "string",   // ID của peer
  "ip_address": "string", // Địa chỉ IP của peer
  "port": "integer"       // Cổng của peer
}
```
Ngoài ra khi thành công sẽ lưu vào cookies với key là 'peer_id' (dùng để xác minh sau này)
- **Lỗi (404):**
```json
{
  "message": "Peer not found!"
}
```

---

## 3. Route: **/peer/protected**
- **Phương thức:** `GET`
- **Mục đích:** Truy cập vào một route bảo vệ yêu cầu peer đã đăng nhập.

### Dữ liệu nhận vào:
- Không có dữ liệu nhận vào.
- Nhưng lưu ý là cookies với key là 'peer_id' phải được set trước đó (phải login trước)
### Dữ liệu trả ra:
- **Thành công (200):**
```json
{
  "message": "Protected route accessed!",
  "peer_id": "string" // ID của peer
}
```
- **Lỗi (403):**
```json
{
  "error": "Peer ID is missing!"
}
```

---

## 4. Route: **/peer/start_peer**
- **Phương thức:** `POST`
- **Mục đích:** Hàm này cho phép một peer khởi động server của mình để bắt đầu tham gia vào mạng P2P.

### Dữ liệu nhận vào:
```json
{
  "ip_address": "string", // Địa chỉ IP của peer (bắt buộc)
  "port": "integer"       // Cổng của peer (bắt buộc)
}
```

### Dữ liệu trả ra:
- **Thành công (200):**
```json
{
  "status": "Peer server started on port {port}" // Thông báo khởi động server thành công
}
```
- **Lỗi (401):**
```json
{
  "error": "Bạn cần phải đăng nhập trước khi Upload"
}
```

---

## Lưu ý
- Tất cả các yêu cầu POST cần phải có `Content-Type: application/json` trong header.
- Route `/peer/protected` yêu cầu peer đã đăng nhập và có ID trong cookie.
