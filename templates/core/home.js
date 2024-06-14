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
			searchOpen: false,
			searchedShows: [],
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
		//var storageEpisodes = ''
		//var storageShows = ''

		// Load Shows & Episodes from Storage if exist, and end mounted 
		if(storageShows && storageEpisodes){
			this.loadShowsAndEpisodes(storageShows, storageEpisodes);
			this.removeLoading();
			return;
		}

		// Get Shows & Episodes from Spotify API, save to storage 
		this.getFollowedShowsAndEpisodes()
			.then(result => {
				var shows = result.data.shows;
				var episodes = result.data.episodes;
				this.loadShowsAndEpisodes(shows, episodes);
				this.saveAllToStorage(shows, episodes);
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

		getFollowedShowsAndEpisodes(){
			return new Promise((resolve, reject) => {
				axios.defaults.headers.common['X-CSRFToken'] = this.csrf;
			    axios.post('{% url 'shows-episodes' %}')
				.then(response => {
					resolve(response);
				})
				.catch(error => {
					console.log(error)
					reject(error.response.data.error);
			 		reject('Failed to get shows and episodes. Please try again.');
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

		handleSelectedShowClick(show){
			this.selectedShowId = show.id
			this.filterEpisodesByShow(show)
		},

		isMyShow(showId){
			if(this.showIds.includes(showId)) return true;
				else return false;
		},

		loadNewEpisodes(episodes){
			this.episodes = JSON.parse(episodes)
			this.filteredEpisodes = JSON.parse(episodes)
		},

		loadSearchedShows(shows){
			this.searchedShows = JSON.parse(shows);
		},

		loadShowEpisodes(episodes){
			episodes.forEach(episode => {
				this.episodes.push(episode)
			});
		},

		loadShowsAndEpisodes(shows, episodes){
			this.shows = JSON.parse(shows);
			this.episodes = JSON.parse(episodes);
			this.filteredEpisodes = JSON.parse(episodes);
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

		saveAllToStorage(shows, episodes){
			localStorage.setItem('shows', shows);
			localStorage.setItem('episodes', episodes);
		},

		saveEpisodesToStorage(){
			localStorage.setItem('episodes', JSON.stringify(this.episodes));
		},

		saveShowsToStorage(){
			localStorage.setItem('shows', JSON.stringify(this.shows));
		},

		selectedShow(){
			return this.shows.find(obj => obj.id == this.selectedShowId);
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
		showIds() {
	  		return this.shows.map(show => show.id);
		}
	}
	
})
app.mount('#app');