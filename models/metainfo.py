class Metainfo:
    def __init__(self, tracker_url, piece_length, pieces):
        self.tracker_url = tracker_url
        self.piece_length = piece_length
        self.pieces = pieces  # Danh sách các hash của các piece