angular.module('pirateguide.controllers', [])

.controller('MoviesCtrl', [
    '$scope',
    'Movies',

    function($scope, Movies)
    {
        Movies.all().success(function(resp)
        {
            var movies  = [];
            var unknown = [];

            angular.forEach(resp, function(i)
            {
                if (i.tmdb_id)
                    movies.push(i);
                else
                    unknown.push(i);
            });

            $scope.movies  = movies;
            $scope.unknown = unknown;
        });

        $scope.setMovie = function(movie)
        {
            $scope.movie = movie;
        };
    }
]);
