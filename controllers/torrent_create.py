import bencodepy
from urllib.parse import urlparse, parse_qs
import hashlib

# Chia file thành các piece
def generate_pieces(file_path, piece_length):
    pieces = []

    # Mở file dưới dạng binary (dạng byte)
    with open(file_path, "rb") as f:
        while True:
            # Đọc một đoạn với độ dài = piece_length
            piece = f.read(piece_length)
            if not piece:
                break
            # Tạo SHA-1 hash cho piece
            piece_hash = hashlib.sha1(piece).digest()
            pieces.append(piece_hash)

    # Nối tất cả các hash lại thành một chuỗi duy nhất
    return b''.join(pieces)

# Cấu trúc info chứa thông tin về file
def generate_info_hash(file_name, piece_length, pieces, file_length):
    info = {
        "name": file_name.encode(),
        "piece length": piece_length,
        "pieces": pieces,
        "length": file_length  # Nếu chỉ có một file
    }
    
    # Bencode thông tin
    bencoded_info = bencodepy.encode(info)
    
    # Tạo SHA-1 hash từ bencoded info
    info_hash = hashlib.sha1(bencoded_info).hexdigest()
    
    return info_hash

# Function to parse a magnet URI
# "magnet:?xt=urn:btih:1234567890abcdef1234567890abcdef12345678&dn=examplefile.txt"
def create_magnet_link(info_hash, file_name):
    base_url = "magnet:?xt=urn:btih:"
    magnet_link = f"{base_url}{info_hash}&dn={file_name}"
    return magnet_link

def create_torrent_file(file_name, piece_length, pieces, file_length, output_file):
    # Torrent metadata for a single file
    torrent_data = {
        "info": {
            "name": file_name.encode(),  # Tên của file
            "piece length": piece_length,  # Độ dài từng piece
            "pieces": pieces,  # Các piece đã được tạo SHA-1 hash
            "length": file_length  # Độ dài file (bytes)
        }
    }
    
    # Bencode the data
    encoded_data = bencodepy.encode(torrent_data)
    
    # Write the encoded data to a .torrent file
    with open(output_file, "wb") as f:
        f.write(encoded_data)
    
    print(f"Torrent file '{output_file}' created successfully!")

def parse_magnet_uri(magnet_link):
    # Parse the magnet link
    parsed = urlparse(magnet_link)
    params = parse_qs(parsed.query)
    
    # Extract info hash
    info_hash = params.get('xt')[0].split(":")[-1]
    
    # Extract display name (optional)
    display_name = params.get('dn', ['Unknown'])[0]
    
    return info_hash, display_name


