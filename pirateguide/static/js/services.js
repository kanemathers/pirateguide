angular.module('pirateguide.services', [])

.factory('Movies', [
    '$http',

    function($http)
    {
        return {
            all: function()
            {
                return $http.get('/movies');
            },

            startStream: function(movie_id)
            {
                $http.post('/movies/stream', {
                    'id': movie_id
                });
            }
        };
    }
])

.factory('TMDB', [
    '$http',
    'Config',

    function($http, Config)
    {
        var settings = {
            api_base: 'http://api.themoviedb.org/3/',
            img_base: null
        };

        var stripSlash = function(path)
        {
            if (path.charAt(0) === '/')
                path = path.slice(1);

            return path;
        };

        var TMDB = {
            request: function(request, params)
            {
                params          = params || {};
                params.api_key  = Config.api_key;
                params.callback = 'JSON_CALLBACK';

                return $http.jsonp(settings.api_base + stripSlash(request),
                                   {params: params});
            },

            imgUrl: function(path)
            {
                var query = '/original/' + stripSlash(path);

                return settings.img_base + stripSlash(query);
            }
        };

        // TODO: requests made beofre this completes will error due to the
        // missing img_base. need to queue them up and retry them once this
        // block completes
        TMDB.request('/configuration').success(function(config)
        {
            settings.img_base = config.images.base_url;
        });

        return TMDB;
    }
]);
