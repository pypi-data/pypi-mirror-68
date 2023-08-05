import logging, requests
from lastipy.lastfm.library.scrobbled_artist import ScrobbledArtist

URL = 'http://ws.audioscrobbler.com/2.0/?method=library.getartists'
MAX_RESULTS_PER_PAGE = 200


#TODO test
def fetch_recent_artists(user, api_key):
    """Fetches tracks similar to the given track"""

    logging.info("Fetching recent artists for user " + user)
    artists = []
    page = 1
    total_pages = 1
    while page <= total_pages:
        json_response = _send_request(_build_json_payload(user, api_key, page))
        logging.debug("Response: " + str(json_response))
        for artist in json_response['artists']['artist']:
            artists.append(ScrobbledArtist(artist_name=artist['name'], playcount=int(artist['playcount'])))
        total_pages = int(json_response['artists']['@attr']['totalPages'])
        page = page + 1

    logging.info("Fetched recent artists " + str(artists))

    return artists

def _send_request(json_payload):
    response = requests.get(URL, params=json_payload)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()

def _build_json_payload(user, api_key, page):
    payload = {
        'format': 'json',
        'page': page,
        'api_key': api_key,
        'limit': MAX_RESULTS_PER_PAGE,
        'user': user
    }
    return payload
