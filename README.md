gomusic
=======

Quick and easy downloader for music purchased through gomusicnow.com

When you purchase music from gomusicnow.com, you need to download each song
individually. This process is pants if you purchase an entire album and
need to click on 20some links to pull your songs down.

This tool will download all songs you have purchased from an album.

Use it like this:

```$ gomusic <album_id>```

The album id can be seen in the gomusic url.
For example: let's say my, err, friend is viewing Susan Boyle's
blockbuster album 'The Gift'.  Their url will look something like this:
http://www.gomusicnow.com/album.html?id=115189

To download all songs that you purchased from that album (likely zero), you
would do this:
```$ gomusic 115189```

All music files will download to your current directory.

Adding --debug to the command line will spit http requests and repsonses to
stdout.
