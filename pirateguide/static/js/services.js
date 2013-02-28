angular.module('pirateguide.services', [])

.factory('Movies', [
    '$http',

    function($http)
    {
        return {
            all: function()
            {
                return $http.get('/movies');
            }
        };
    }
])

.factory('TMDB', [
    '$http',
    'api_key',

    function($http, api_key)
    {
        var api_base = 'http://api.themoviedb.org/3/';

        return {
            request: function(request, params)
            {
                params          = params || {};
                params.api_key  = api_key;
                params.callback = 'JSON_CALLBACK';

                if (request.charAt(0) === '/')
                    request = request.slice(1)

                return $http.jsonp(api_base + request, {params: params});
            }
        };
    }
]);
