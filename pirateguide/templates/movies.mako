<p data-ng-repeat="movie in movies">
    <a data-ng-click="setMovie(movie)">{{movie.info.title}}</a>
</p>

<div data-ng-show="movie">
    <h1>{{movie.info.title}}</h1>
</div>
