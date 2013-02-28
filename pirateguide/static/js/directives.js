angular.module('pirateguide.directives', [])

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
