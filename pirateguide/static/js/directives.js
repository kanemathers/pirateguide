angular.module('pirateguide.directives', [
    'pirateguide.services'
])

.directive('sidebar', [
    'Sidebar',

    function(Sidebar)
    {
        return {
            restrict:    'A',
            templateUrl: '/partials/sidebar.html',
            link: function(scope, element, attrs)
            {
                scope.$watch(function() { return Sidebar.length; }, function(sz)
                {
                    if (!sz)
                        return;

                    scope.menus = Sidebar;
                    scope.setActiveMenu(Sidebar[0]);
                });

                scope.setActiveMenu = function(menu)
                {
                    scope.activeMenu = menu;
                };
            }
        };
    }
])

.directive('bgChanger', [
    function()
    {
        return {
            restrict: 'A',
            link: function(scope, element, attrs)
            {
                scope.$on('bg:change', function(event, url)
                {
                    element.css('background-image', 'url(' + url + ')');
                });
            }
        };
    }
]);
