angular.module('pirateguide', [
    'pirateguide.controllers',
    'pirateguide.services'
])

.config([
    '$routeProvider',

    function($routeProvider)
    {
        $routeProvider
            .when('/movies', {
                controller:  'MoviesCtrl',
                templateUrl: '/partials/movies.html'
            })

            .otherwise({redirectTo: '/movies'});
    }
]);
