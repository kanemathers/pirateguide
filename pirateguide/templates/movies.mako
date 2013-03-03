<div class="container-fluid">
    <div class="row-fluid">
        <div id="sidebar" class="span3">
            <div class="well">
                <input class="span12" placeholder="Search..." data-ng-model="search.$">

                <ul class="nav nav-list">
                    <li data-ng-repeat="movie in movies | filter: search | orderBy: 'info.title'">
                        <a data-ng-click="setMovie(movie)">{{movie.info.title}}</a>
                    </li>

                    <li class="divider"></li>

                    <li data-ng-repeat="file in unknown | filter: search | orderBy: 'path'">
                        <a title="{{file.path}}">{{baseName(file.path)}}</a>
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
                <div class="span4 likes">
                    <h3>Likes</h3>

                    <div class="likebar">
                        <div class="bar" style="width: {{movie.info.vote_average * 10}}%"></div>
                    </div>
                </div>
                <div class="span4 tags">
                    <h3>Tags</h3>

                    <ul class="unstyled inline taglist">
                        <li data-ng-repeat="genre in movie.info.genres">
                            <span class="badge badge-important">{{genre.name}}</span>
                        </li>
                    </ul>
                </div>
                <div class="span4 runtime">
                    <h3>Runtime</h3>

                    <strong>{{movie.info.runtime / 60 | number: 1}} hrs</strong>
                </div>
            </div>
        </div>
    </div>

    <div id="push"></div>
</div>

<div id="footer">
    <div class="container-fluid">
        <div class="row-fluid">
            <div class="span9 offset3">
                <button class="btn btn-primary btn-medium pull-right" data-ng-show="stream" data-ng-click="startStream(movie)">Stream</button>
            </div>
        </div>
    </div>
</div>
