import hashlib

def check_integrity(file_piece, expected_hash):
    sha256 = hashlib.sha256()
    sha256.update(file_piece)
    return sha256.hexdigest() == expected_hash