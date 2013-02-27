angular.module('pirateguide.controllers', [])

.controller('MoviesCtrl', [
    '$scope',
    'Movies',

    function($scope, Movies)
    {
        Movies.all().success(function(movies)
        {
            $scope.movies = movies;
        });

        $scope.setMovie = function(movie)
        {
            $scope.movie = movie;
        };
    }
]);
