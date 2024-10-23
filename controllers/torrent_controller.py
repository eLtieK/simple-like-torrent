# import bencodepy
# from urllib.parse import urlparse, parse_qs

# # Function to parse a magnet URI
# # "magnet:?xt=urn:btih:1234567890abcdef1234567890abcdef12345678&dn=examplefile.txt"
# def parse_magnet_uri(magnet_link):
#     # Parse the magnet link
#     parsed = urlparse(magnet_link)
#     params = parse_qs(parsed.query)
    
#     # Extract info hash
#     info_hash = params.get('xt')[0].split(":")[-1]
    
#     # Extract display name (optional)
#     display_name = params.get('dn', ['Unknown'])[0]
    
#     return info_hash, display_name

# # Function to create a .torrent file (Metainfo)
# def create_torrent_file(info_hash, file_name, output_file):
#     # Sample torrent metadata (in Bencode format)
#     torrent_data = {
#         "info": {
#             "piece length": 512000,  # Example piece length (512KB)
#             "pieces": b"abcd1234efgh5678abcd1234efgh5678",  # Placeholder piece hashes (20-byte SHA-1 hashes)
#             "name": file_name.encode(),  # File name
#             "length": 1024000  # Example file size (1MB)
#         }
#     }
    
#     # Bencode the data
#     encoded_data = bencodepy.encode(torrent_data)
    
#     # Write the encoded data to a .torrent file
#     with open(output_file, "wb") as f:
#         f.write(encoded_data)
    
#     print(f"Torrent file '{output_file}' created successfully!")

# def read_torrent_file(output_file):
#     # Đọc file .torrent
#     with open(output_file, "rb") as f:
#         bencoded_data = f.read()
    
#     # Giải mã dữ liệu
#     decoded_data = bencodepy.decode(bencoded_data)
    
#     return decoded_data

# # Example magnet URI
# magnet_link = "magnet:?xt=urn:btih:1234567890abcdef1234567890abcdef12345678&dn=examplefile.txt"

# # Step 1: Parse the magnet URI
# info_hash, file_name = parse_magnet_uri(magnet_link)

# # Print extracted information
# print("Extracted Info:")
# print(f"Info Hash: {info_hash}")
# print(f"File Name: {file_name}")

# # Step 2: Create a .torrent file using the extracted info
# output_file = "examplefile.torrent"
# create_torrent_file(info_hash, file_name, output_file)

# torrent_data = read_torrent_file(output_file)

# # In dữ liệu đã giải mã
# print(torrent_data)
