pirateguide
===========

Basically, turns this:

![Before](/docs/before.png)

Into this:

![After](/docs/after.png)

Installing
----------

Get the code:

    $ git clone git://github.com/kanemathers/pirateguide.git

Install it:

    $ cd pirateguide
    $ python setup.py install

Configuring
-----------

Open ``config.ini`` for editing and you'll see the following block:

    ###
    # configure pirateguide
    ###
    movies.directories = /path/to/your/movies
                         /can/have/more/if/want
    movies.blacklist = %(here)s/blacklist.txt
    movies.btn.play = vlc "{0}"
    movies.api_key = ec6a8e3f49b6bf68ae03c6904ad70d0e

### Explanation

``movies.directories``: Path to the folder your movies are stored in. You
                        can have multiple paths separated by line breaks.

``movies.blacklist``: Path to a textfile of words to be stripped from movie
                      filenames.

``movies.btn.play``: Command to execute when a movie is clicked to play. The
                     path, to the movie, will be put in place of ``{0}``.
                     You can leave this blank to not allow playing movies.

``movies.api_key``: API key from themoviedb.org. Feel free to get your own.

Using the Client
----------------

Run pirateguide:

    $ pirateguide -i [config.ini]

Note: The ``-i`` flag is used to initialize the database. This only needs to
be run once. Though, it's safe to call again.

This will scan your library paths and fetch the movie info for discovered
files.

A watchdog will also be started to monitor filesystem changes to keep the
database in sync.

Finally, start the web interface:

    $ pserve [config.ini]

Navigate to [http://localhost:6543](http://localhost:6543)
