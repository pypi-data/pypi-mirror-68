from lastipy.spotify.parse_spotify_tracks import parse_tracks
import spotipy
import logging


#TODO test
def get_tracks_in_playlists(spotify):
    """Returns all tracks in the currently-logged-in user's playlists"""

    logging.info("Fetching all tracks in " + spotify.current_user()['id'] + "'s playlists")

    playlists = spotify.current_user_playlists()['items']

    tracks = []
    for playlist in playlists:
        tracks = tracks + get_tracks_in_playlist(spotify, playlist_id=playlist['id'])

    logging.info("Fetched tracks " + str(tracks))

    return tracks


def get_tracks_in_playlist(spotify, playlist_id):
    """Returns all tracks in the given playlist"""

    tracks_in_playlist = []

    keep_fetching = True
    while keep_fetching:
        json_response = spotify.playlist_tracks(playlist_id=playlist_id,
                                                offset=len(tracks_in_playlist))
        if json_response['items']:
            tracks_in_playlist = tracks_in_playlist + parse_tracks(json_response['items'])
        else:
            keep_fetching = False

    return tracks_in_playlist


def get_saved_tracks(spotify):
    """Returns the currently-logged-in users's saved tracks"""

    logging.info("Fetching " + spotify.current_user()['id'] + "'s saved tracks")

    saved_tracks = []
    keep_fetching = True
    while keep_fetching:
        json_response = spotify.current_user_saved_tracks(offset=len(saved_tracks))
        if json_response['items']:
            saved_tracks = saved_tracks + parse_tracks(json_response['items'])
        else:
            keep_fetching = False

    logging.info("Fetched tracks: " + str(saved_tracks))

    return saved_tracks


def add_tracks_to_library(spotify, tracks):
    logging.info("Adding " + str(tracks) + " to " + spotify.current_user()['id'] + "'s library")
    # Spotify only allows 50 tracks to be added to a library at once, so we need to chunk 'em up
    limit = 50
    track_chunks = [tracks[i:i + limit] for i in range(0, len(tracks), limit)]  
    for chunk in track_chunks:
        spotify.current_user_saved_tracks_add([track.spotify_id for track in chunk])