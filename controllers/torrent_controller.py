from urllib.parse import urlparse, parse_qs

def parse_magnet_uri(magnet_link):
    # Parse the magnet link
    parsed = urlparse(magnet_link)
    params = parse_qs(parsed.query)
    
    # Extract info hash
    info_hash = params.get('xt')[0].split(":")[-1]
    
    # Extract display name (optional)
    display_name = params.get('dn', ['Unknown'])[0]
    
    return info_hash, display_name