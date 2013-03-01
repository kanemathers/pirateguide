angular.module('pirateguide.controllers', [])

.controller('MoviesCtrl', [
    '$scope',
    'Movies',
    'TMDB',

    function($scope, Movies, TMDB)
    {
        var findPoster = function(posters)
        {
            var closest = null;

            angular.forEach(posters, function(poster)
            {
                var ratio = poster.width / poster.height;

                if (!closest || Math.abs(ratio - screenRatio) - Math.abs(closest, screenRatio))
                    closest = poster;
            });

            return closest;
        };

        $scope.setMovie = function(movie)
        {
            $scope.movie = movie;

            TMDB.request('/movie/' + movie.tmdb_id + '/images').success(function(images)
            {
                var bg  = findPoster(images.backdrops);
                var url = TMDB.imgUrl(bg.file_path);

                $scope.$emit('bg:change', url);
            });
        };

        var screen      = angular.element(window);
        var screenRatio = screen.width() / screen.height();

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
    }
]);
