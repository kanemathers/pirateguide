<input class="span12 search" placeholder="Search" tabindex="1" data-ng-model="search" autofocus>

<ul class="nav nav-tabs">
    <li data-ng-repeat="menu in menus">
        <a title="{{menu.title}}" class="{{'tab-' + menu.title | lowercase}}" data-ng-click="setActiveMenu(menu)">{{menu.title}}</a>
    </li>
</ul>

<ul class="nav nav-list">
    <li data-ng-repeat="item in activeMenu.items | filter: search | orderBy: activeMenu.itemTitle">
        <a data-ng-click="activeMenu.setItem(item)">{{activeMenu.itemTitle(item)}}</a>
    </li>
</ul>
