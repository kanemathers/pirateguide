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
]);
