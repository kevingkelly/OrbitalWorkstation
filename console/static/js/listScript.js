        angular.module('myApp', [])
            .controller('HomeCtrl', function($scope, $http) {
			
				$scope.info = {};
				
				$scope.showAdd = true;
			
				$scope.showlist = function(){
					$http({
						method: 'POST',
						url: '/getProjectileList',

					}).then(function(response) {
						$scope.projectiles = response.data;
						console.log('mm',$scope.projectiles);
					}, function(error) {
						console.log(error);
					});
				}
			
                
				
				$scope.addProjectile = function(){
					
					
					
					$http({
						method: 'POST',
						url: '/addProjectile',
						data: {info:$scope.info}
					}).then(function(response) {
						$scope.showlist();
						$('#addPopUp').modal('hide')
						$scope.info = {}
					}, function(error) {
						console.log(error);
					});
				}
				
				$scope.editProjectile = function(id){
					$scope.info.id = id;
					
					$scope.showAdd = false;
					
					$http({
						method: 'POST',
						url: '/getProjectile',
						data: {id:$scope.info.id}
					}).then(function(response) {
						console.log(response);
						$scope.info = response.data;
						$('#addPopUp').modal('show')
					}, function(error) {
						console.log(error);
					});
				}
				
				$scope.updateProjectile = function(id){
				
					$http({
						method: 'POST',
						url: '/updateProjectile',
						data: {info:$scope.info}
					}).then(function(response) {
						console.log(response.data);
						$scope.showlist();
						$('#addPopUp').modal('hide')
					}, function(error) {
						console.log(error);
					});
				}
				
		
				$scope.showAddPopUp = function(){
					$scope.showAdd = true;
					$scope.info = {};
					$('#addPopUp').modal('show')
				}
				
				$scope.showAddConstellationPopUp = function(){
					$scope.showAddConstellation = true;
					$scope.info = {};
					$('#addConstellationPopUp').modal('show')
				}
				
				$scope.showRunSimulationPopUp = function(){
					$scope.showRunSimulation = true;
					$scope.info = {};
					$('#runSimulationPopUp').modal('show')
				}
				
				$scope.showRunPopUp = function(id){
				
					$scope.info.id = id;
					$scope.run = {};
					
					$http({
						method: 'POST',
						url: '/getProjectile',
						data: {id:$scope.info.id}
					}).then(function(response) {
						console.log(response);
						$scope.run = response.data;
						$scope.run.isRoot = false;
						$('#runPopUp').modal('show');
					}, function(error) {
						console.log(error);
					});
				}
				
				$scope.confirmDelete = function(id){
					$scope.deleteProjectileId = id;
					$('#deleteConfirm').modal('show');
				}
				
				$scope.deleteProjectile = function(){
					
					$http({
						method: 'POST',
						url: '/deleteProjectile',
						data: {id:$scope.deleteProjectileId}
					}).then(function(response) {
						console.log(response.data);
						$scope.deleteProjectileId = '';
						$scope.showlist();
						$('#deleteConfirm').modal('hide')
					}, function(error) {
						console.log(error);
					});
				}
				
				$scope.executeCommand = function(){
					
					console.log($scope.run);
					
					$http({
						method: 'POST',
						url: '/execute',
						data: {info:$scope.run}
					}).then(function(response) {
						console.log(response);
						$scope.run.response = response.data.message;
					}, function(error) {
						console.log(error);
					});
				}
				
				$scope.showlist();
            })
