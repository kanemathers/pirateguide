angular.module('pirateguide.controllers', [])

.controller('MoviesCtrl', [
    '$scope',
    'Sidebar',
    'Movies',
    'TMDB',
    'Config',

    function($scope, Sidebar, Movies, TMDB, Config)
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

            TMDB.request('/movie/' + movie.tmdb_id + '/trailers').success(function(trailers)
            {
                var youtube          = 'https://www.youtube.com/embed/';
                $scope.movie.trailer = youtube + trailers.youtube[0].source;
            });
        };

        $scope.playMovie = function(movie)
        {
            Movies.playMovie(movie.id);
        };

        $scope.baseName = function(path)
        {
            return path.substring(path.lastIndexOf('/') + 1);
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

            Sidebar.push({
                title:    'Movies',
                items:     movies,
                setItem:   $scope.setMovie,
                itemTitle: function(item)
                {
                    return item.info.title;
                },
            });

            Sidebar.push({
                title:     'Unknown',
                items:     unknown,
                itemTitle: function(item)
                {
                    return $scope.baseName(item.path);
                }
            });

            $scope.setMovie(movies[0]);
        });

        $scope.buttons = Config.buttons;
    }
]);
