# Discogs-APY
A lightweight Python wrapper for the Discogs API.

### Usage
Initialise the client using your user token. No support for OAuth yet. Maybe I'll get around to it.
```
client = Discogs-APY.Client(user_token)
```
The client object has Release, Master, Artist, and Label methods. Calling them with a valid discogs ID will return an object of the same name:
```
release = client.release(725292)
Black Holes & Revelations - https://api.discogs.com/releases/725292
```
The object attributes are populated using the json returned from the discogs request.
```
release.artists
[Muse - https://api.discogs.com/artists/1003]
```
Where appropriate, the json data is passed through a database object so that nested endpoints can be accessed using chained dot notation:
```
release.tracklist[0].extraartists[1]
Audrey Riley - https://api.discogs.com/artists/257846
```
Not all attributes are populated with a value. Accessing an attribute with no value will raise a key error.
```
release.members
KeyError: "The 'artist' attribute is not in the json dictionary"
```

