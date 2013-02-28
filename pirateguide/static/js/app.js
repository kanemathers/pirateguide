angular.module('pirateguide', [
    'pirateguide.controllers',
    'pirateguide.services',
    'pirateguide.directives'
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
