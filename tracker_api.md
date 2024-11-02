# Tài liệu API cho Quản lý Tracker

## 1. Route: **/tracker/all_peer**
- **Phương thức:** `GET`
- **Mục đích:** Lấy danh sách tất cả các peer hiện đang được đăng ký với tracker.
- **Dữ liệu yêu cầu:** Không có.

- **Dữ liệu trả về:**
  - **Thành công (200):**
  1 list các peers
    ```json
    [
      {
        "name": "string",  
        "ip_address": "string",
        "port": "integer"
      }
      ...
    ]
    ```

## 2. Route: **/tracker/peer/<name>**
- **Phương thức:** `GET`
- **Mục đích:** Lấy thông tin về một peer cụ thể theo tên.
- **Dữ liệu yêu cầu:**
  - `name` (string): Tên của peer cần lấy thông tin.

- **Dữ liệu trả về:**
  - **Thành công (200):**
    ```json
    {
      "name": "string",  
      "ip_address": "string",
      "port": "integer"
    }
    ```
  - **Lỗi (404):**
    ```json
    {
      "error": "Peer không tồn tại"
    }
    ```

## 3. Route: **/tracker/uploading**
- **Phương thức:** `POST`
- **Mục đích:** Tải một tệp lên tracker.
- **Dữ liệu yêu cầu:**
  - `file`: Tệp tin cần tải lên (được bao gồm trong form-data).

- **Dữ liệu trả về:**
  - **Thành công (201):**
    ```json
    {
      "message": "Tệp đã được tải lên thành công"
    }
    ```
  - **Lỗi (400):**
    ```json
    {
      "error": "Không có phần tệp trong yêu cầu"
    }
    ```
    hoặc
    ```json
    {
      "error": "Không có tệp nào được chọn"
    }
    ```
  - **Lỗi (401):**
    ```json
    {
      "error": "Bạn cần phải đăng nhập trước khi tải lên"
    }
    ```
  - **Lỗi (500):**
    ```json
    {
      "error": "Không thể tải lên tệp"
    }
    ```

## 4. Route: **/tracker/peer/set_inactive**
- **Phương thức:** `POST`
- **Mục đích:** Đặt trạng thái của một peer thành không hoạt động.
- **Dữ liệu yêu cầu:** Không có (cần có cookie với key là 'peer_id').

- **Dữ liệu trả về:**
  - **Thành công (200):**
    ```json
    {
      "message": "Trạng thái của peer đã được cập nhật thành không hoạt động"
    }
    ```
  - **Lỗi (400):**
    ```json
    {
      "error": "Thiếu peer_id"
    }
    ```
  - **Lỗi (404):**
    ```json
    {
      "error": "Peer không tồn tại hoặc trạng thái không thay đổi"
    }
    ```

## 5. Route: **/tracker/downloading/<encoded_magnet>**
- **Phương thức:** `POST`
- **Mục đích:** Tải một tệp liên kết với liên kết magnet đã cho.
- **Dữ liệu yêu cầu:**
  - `encoded_magnet` (string): Liên kết magnet được mã hóa cho yêu cầu.

- **Dữ liệu trả về:**
  - **Thành công (200):**
    ```json
    {
      "message": "Tệp đã được tải xuống thành công"
    }
    ```
  - **Lỗi (401):**
    ```json
    {
      "error": "Bạn cần phải đăng nhập trước khi kết nối tới peer"
    }
    ```
  - **Lỗi (404):**
    ```json
    {
      "error": "Tệp không tồn tại"
    }
    ```
    hoặc
    ```json
    {
      "error": "Không có dữ liệu nào được tải xuống"
    }
    ```