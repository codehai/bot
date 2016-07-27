'use strict';

app.config(function ($stateProvider, $urlRouterProvider) {
  $stateProvider.state('default', {
    url: '',
    templateUrl: 'controllers/home/index.html',
    controller: 'HomeIndexCtrl'
  });

  $stateProvider.state('home', {
    url: '/',
    templateUrl: 'controllers/home/index.html',
    controller: 'HomeIndexCtrl'
  });

  $stateProvider.state('notFound', {
    url: '/notFound',
    templateUrl: 'controllers/home/notFound.html',
    controller: 'HomeNotFoundCtrl'
  });

  $urlRouterProvider.otherwise('/notFound');
  
  $stateProvider.state('reader',{
    url:'/reader',
    template:'<div ui-view></div>',
    abstract: true
  });
  $stateProvider.state('reader.create',{
    url:'/create',
    templateUrl: 'controllers/reader/create.html',
    controller:'ReaderCreateCtrl as vm'
  });  

});
