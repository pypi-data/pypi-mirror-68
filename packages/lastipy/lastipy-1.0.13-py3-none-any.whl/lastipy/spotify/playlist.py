import logging


#TODO test
def replace_tracks_in_playlist(spotify, playlist_name, tracks):
    """Replaces all tracks in the currently-logged-in user's given playlist 
        with the given tracks. If the playlist does not exist, creates it first."""

    playlist_id = _fetch_playlist(spotify, playlist_name)
    
    if playlist_id is None:
        logging.info("Creating playlist " + playlist_name)
        playlist_id = spotify.user_playlist_create(user=spotify.current_user()['id'], name=playlist_name)['id']

    logging.info("Adding " + str(len(tracks)) + " tracks to " + spotify.current_user()['id'] + "'s playlist " + playlist_name + ": " + str(tracks))

    spotify.user_playlist_replace_tracks(user=spotify.current_user()['id'],
                                         playlist_id=playlist_id,
                                         tracks=[track.spotify_id for track in tracks])


def _fetch_playlist(spotify, playlist_name):
    playlists = spotify.current_user_playlists()
    playlists = [playlist for playlist in playlists['items'] if playlist['name'] == playlist_name]
    if playlists:
        return playlists[0]['id']
    else:
        return None

