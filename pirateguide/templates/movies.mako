<div class="container-fluid">
    <div class="row-fluid">
        <div id="sidebar" class="span3">
            <div class="well sidebar">
                <input class="span12" placeholder="Search..." data-ng-model="search.$">

                <ul class="nav nav-list">
                    <li data-ng-repeat="movie in movies | filter: search | orderBy: 'info.title'">
                        <a data-ng-click="setMovie(movie)">{{movie.info.title}}</a>
                    </li>
                </ul>
            </div>
        </div>
        <div id="content" class="span9" data-ng-show="movie">
            <div class="page-header">
                <h1>{{movie.info.title}} <small>({{movie.info.release_date | date: 'yyyy'}})</small></h1>
                <p class="tagline">{{movie.info.tagline}}</p>
            </div>

            <h2>About</h2>
            <p>{{movie.info.overview}}</p>

            <div class="row-fluid stats-row">
                <div class="span4">
                    {{movie.info.vote_average}}
                </div>
                <div class="span4">
                    <ul class="unstyled inline">
                        <li data-ng-repeat="genre in movie.info.genres">
                            <span class="label">{{genre.name}}</span>
                        </li>
                    </ul>
                </div>
                <div class="span4">
                    {{movie.info.runtime / 60 | number: 1}} hrs
                </div>
            </div>
        </div>
    </div>
</div>
