import vlc

#example url
url="https://player.vimeo.com/external/363536021.hd.mp4?s=6f6e87d86a49149479ebdab6c8bc421aa89f327c&profile_id=175&oauth2_token_id=57447761"
player = vlc.Instance().media_player_new()
player.set_media(vlc.Instance().media_new(url))
player.play()