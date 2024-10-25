import base64

def decode_magnet_link(magnet_link):
    # Kiểm tra xem magnet link có bắt đầu bằng 'magnet:' không
    if not magnet_link.startswith("magnet:?"):
        return None

    # Tách các phần của magnet link
    parts = magnet_link[8:].split('&')  # Bỏ qua 'magnet:'
    info_hash = None

    # Lặp qua từng phần để tìm info_hash
    for part in parts:
        if part.startswith("xt=urn:btih:"):
            # Lấy info_hash
            info_hash = part[13:]  # Bỏ qua 'xt=urn:btih:'
            break

    return info_hash

def decode_pieces(base64_string, piece_size):
    #Giải mã chuỗi Base64 thành dữ liệu nhị phân.
    binary_data = base64.b64decode(base64_string)

    # Chúng ta sẽ chia dữ liệu nhị phân thành nhiều phần, mỗi phần có kích thước là piece_size.
    pieces = []
    for i in range(0, len(binary_data), piece_size):
        # Lấy một phần dữ liệu có kích thước là piece_size
        piece = binary_data[i:i + piece_size]
        pieces.append(piece)  # Thêm phần này vào danh sách các pieces

    return pieces  # Trả về danh sách các pieces

def download_file(metainfo_id, pieces):
    """
    Ghép các piece từ danh sách và tải xuống cho client.

    Args:
        metainfo_id (str): ID của metainfo để nhận dạng tệp.
        pieces (list): Danh sách các piece (nên là chuỗi hoặc bytes).

    Returns:
        str: Đường dẫn đến file đã tải xuống.
    """
    # Đường dẫn tới file sẽ được tạo
    output_file_path = f"downloads/{metainfo_id}.bin"  # Bạn có thể thay đổi định dạng nếu cần

    # Đảm bảo thư mục tồn tại
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Ghép nối các piece lại
    with open(output_file_path, 'wb') as output_file:  # Mở file ở chế độ ghi nhị phân
        for piece in pieces:
            output_file.write(piece)  # Ghi từng piece vào file

    return output_file_path