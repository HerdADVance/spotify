const app = Vue.createApp({
	delimiters: ['[[', ']]'],
	
	data() {
		return {
			addRemoveShowError: '',
			csrf: '{{ csrf_token }}',
			displayName: '{{ display_name }}',
			episodes: null,
			errorMessage: null,
			filteredEpisodes: [],
			loading: true,
			numEpisodesToGet: 10,
			numEpisodesToGetOptions: [5,10,20],
			playlists: [],
			playlistsSearchError: '',
			playlistsSearchQuery: '',
			searchOpen: false,
			searchedPlaylists: [],
			searchedShows: [],
			selectedPanel: 'playlists',
			selectedPlaylistId: null,
			selectedShowId: null,
			shows: [],
			showsGridView: true,
			showsSearchError: '',
			showsSearchQuery: ''
		};
	},

	mounted() {

		// Set or get Spotify display name
		this.handleDisplayName();
		
		// Check local storage for shows and episodes
		var storageShows = localStorage.getItem('shows');
		var storageEpisodes = localStorage.getItem('episodes');
		var storagePlaylists = localStorage.getItem('playlists');

		// Load Shows & Episodes from Storage if exist, and end mounted 
		if(storageShows && storageEpisodes && storagePlaylists){
			console.log('load from local')
			this.loadAll(storageShows, storageEpisodes, storagePlaylists);
			this.removeLoading();
			return;
		}

		// Get Shows & Episodes from Spotify API, save to storage 
		this.getAllFollowed()
			.then(result => {
				var shows = result.data.shows;
				var episodes = result.data.episodes;
				var playlists = result.data.playlists;
				console.log(result.data)
				this.loadAll(shows, episodes, playlists);
				this.saveAllToStorage(shows, episodes, playlists);
				this.removeLoading();
			})
			.catch(error => {
				this.displayErrorMessage(error);
			})

	},

	methods: {
		addOrRemoveShow(action, show){
			const ff = new FormData();
			ff.append('show_id', show.id);
			ff.append('action', action == 'remove' ? 'remove' : 'add');
		
			axios.defaults.headers.common['X-CSRFToken'] = this.csrf;
			this.loading = true;
			axios.post('{% url 'add-remove-show' %}', ff)
				.then(response => {
					if(response.data.action == 'remove'){
						this.deleteRemovedShow(show);
						this.deleteShowEpisodes(show);
						this.saveEpisodesToStorage();
					}
					else{
						this.saveAddedShow(show);
					}
					this.saveShowsToStorage();
					this.removeLoading();
	        	})
		        .catch(error => {
					this.displayErrorMessage(error.response.data.error);
				})

	        return false
		},

		deleteRemovedShow(show){
			this.shows = this.shows.filter(item => item.id !== show.id);
		},

		deleteShowEpisodes(show){
			this.episodes = this.episodes.filter(item => item.podcast_id !== show.id);
			this.filteredEpisodes = this.episodes;
		},

		displayErrorMessage(error){
			this.errorMessage = error;
		},

		filterEpisodesByShow(show){
			this.filteredEpisodes = [];
			this.episodes.forEach((episode) => {
				if(episode.podcast_id == show.id){
					this.filteredEpisodes.push(episode);
				}
			})
		},

		gatherShowsInfo(){
			showsInfo = []
			this.shows.forEach((show) => {
				var showInfo = {
					'id': show.id,
					'name': show.name,
					'uri': show.uri,
					'image': show.image
				};
				showsInfo.push(showInfo);
			})
			return showsInfo;
		},

		getAllFollowed(){
			return new Promise((resolve, reject) => {
				axios.defaults.headers.common['X-CSRFToken'] = this.csrf;
			    axios.post('{% url 'get-all-followed' %}')
				.then(response => {
					resolve(response);
				})
				.catch(error => {
					console.log(error)
					reject(error.response.data.error);
			 		reject('Failed to get data. Please try again.');
  				})
  			});
		},

		getNewEpisodes(){
			const fd = new FormData();
			fd.append('num_episodes', this.numEpisodesToGet);
			fd.append('shows', JSON.stringify(this.gatherShowsInfo()));

			axios.defaults.headers.common['X-CSRFToken'] = this.csrf;
			this.loading = true;
			axios.post('{% url 'new-episodes' %}', fd)
				.then(response => {
					this.loadNewEpisodes(response.data.episodes);
					this.saveEpisodesToStorage();
					this.removeLoading();
	        	})
		        .catch(error => {
					this.displayErrorMessage(error.response.data.error);
				});

	        return false
		},

		getSearchedPlaylists(){
			if(!this.playlistsSearchQuery){
				this.playlistsSearchError = "Search query can't be empty. Please try again.";
				return false;
			}
			
			const ff = new FormData();
			ff.append('query', this.playlistsSearchQuery);
		
			axios.defaults.headers.common['X-CSRFToken'] = this.csrf;
			this.loading = true;
			axios.post('{% url 'search-playlists' %}', ff)
				.then(response => {
					this.loadSearchedPlaylists(response.data.playlists);
					this.removeLoading();
	        	})
		        .catch(error => {
					this.displayErrorMessage(error.response.data.error);
				});
			
			return false
		},

		getSearchedShows(){
			if(!this.showsSearchQuery){
				this.showsSearchError = "Search query can't be empty. Please try again.";
				return false;
			}
			
			const ff = new FormData();
			ff.append('query', this.showsSearchQuery);
		
			axios.defaults.headers.common['X-CSRFToken'] = this.csrf;
			this.loading = true;
			axios.post('{% url 'search-shows' %}', ff)
				.then(response => {
					this.loadSearchedShows(response.data.shows);
					this.removeLoading();
	        	})
		        .catch(error => {
					this.displayErrorMessage(error.response.data.error);
				});

			return false
		},

		getShowEpisodes(){
			if(!this.selectedShowId){
				this.displayErrorMessage('No show has been selected. Please select a show and try again.')
				return false;
			}
			
			const ff = new FormData();
			var show = this.selectedShow();
			ff.append('show', JSON.stringify(show));
		
			axios.defaults.headers.common['X-CSRFToken'] = this.csrf;
			this.loading = true;
			axios.post('{% url 'show-episodes' %}', ff)
				.then(response => {
					this.loadShowEpisodes(JSON.parse(response.data.episodes));
					this.sortEpisodesByDate()
					this.filterEpisodesByShow(show)
					this.removeLoading();
	        	})
		        .catch(error => {
		        	console.log(error)
					this.displayErrorMessage(error.response.data.error);
				});

	        return false
		},

		handleAllShowsClick(){
			this.filteredEpisodes = this.episodes
		},

		handleDisplayName(){
			if(this.displayName != ''){
				localStorage.setItem('displayName', this.displayName);
			} else{
				this.displayName = localStorage.getItem('displayName');
			}
		},

		handleSelectedPlaylistClick(playlist){
			//this.selectedPlaylistId = playlist.id
			window.location.href = playlist.uri;
		},

		handleSelectedShowClick(show){
			this.selectedShowId = show.id
			this.filterEpisodesByShow(show)
		},

		isMyPlaylist(playlistId){
			if(this.playlistIds.includes(playlistId)) return true;
				else return false;
		},

		isMyShow(showId){
			if(this.showIds.includes(showId)) return true;
				else return false;
		},

		loadAll(shows, episodes, playlists){
			this.shows = JSON.parse(shows);
			this.episodes = JSON.parse(episodes);
			this.playlists = JSON.parse(playlists);
			this.filteredEpisodes = JSON.parse(episodes);
		},

		loadNewEpisodes(episodes){
			this.episodes = JSON.parse(episodes)
			this.filteredEpisodes = JSON.parse(episodes)
		},

		loadSearchedPlaylists(playlists){
			this.searchedPlaylists = JSON.parse(playlists);
		},

		loadSearchedShows(shows){
			this.searchedShows = JSON.parse(shows);
		},

		loadShowEpisodes(episodes){
			episodes.forEach(episode => {
				this.episodes.push(episode)
			});
		},

		removeLoading(){
			this.loading = false;
			this.errorMessage = null;
		},

		saveAddedShow(show){
			this.shows.push({
				'id': show.id,
				'name': show.name,
				'uri': show.uri,
				'image': show.image
			});
		},

		saveAllToStorage(shows, episodes, playlists){
			localStorage.setItem('shows', shows);
			localStorage.setItem('episodes', episodes);
			localStorage.setItem('playlists', playlists);
		},

		saveEpisodesToStorage(){
			localStorage.setItem('episodes', JSON.stringify(this.episodes));
		},

		savePlaylistsToStorage(){
			localStorage.setItem('playlists', JSON.stringify(this.playlists));
		},

		saveShowsToStorage(){
			localStorage.setItem('shows', JSON.stringify(this.shows));
		},

		selectedShow(){
			return this.shows.find(obj => obj.id == this.selectedShowId);
		},

		setSelectedPanel(panel){
			this.selectedPanel = panel;
		},

		sortEpisodesByDate(){
			this.episodes.sort((a, b) => {
			  const [aMonth, aDay, aYear] = a.release_date.split("/");
			  const [bMonth, bDay, bYear] = b.release_date.split("/");
			  const aDate = new Date(`20${aYear}`, aMonth - 1, aDay);
			  const bDate = new Date(`20${bYear}`, bMonth - 1, bDay);
			  return bDate - aDate;
			});
			this.filteredEpisodes = this.episodes
		},

		toggleNumEpisodesToGet(num){
			this.numEpisodesToGet = num;
		},

		toggleSearchOpen(){
			this.searchOpen = !this.searchOpen;
		},

		toggleShowsGridView(grid){
			this.showsGridView = grid;
		}
	},
	computed: {
		playlistIds() {
	  		return this.playlists.map(playlist => playlist.id);
		},
		showIds() {
	  		return this.shows.map(show => show.id);
		}
	}
	
})
app.mount('#app');