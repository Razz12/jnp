(function ($) {
	$(start);
	var contentDiv = '#content'
	function start() {
		$(window).bind('hashchange', processUrl);
		setEventListeners();
		processUrl();
	}

	function processUrl() {
		hash = getHash();
		if(hash.length > 0) {
			rest = hash.slice(1);
			switch(hash[0]) {
				case 'i':
					loadSingleImage(rest); 
				break;
				case 'b':
					loadBest(rest); 
				break;
				case 'n':
					loadNewest(rest);
				break;
				case 't':
					rest = split(rest, ',');
					loadTag(rest[0], rest.length > 1 ? rest[1] : '');
			}
		} else {
			loadDefault();
		}
	}

	function search(txt) {
		loadPictures('/search/' + txt);
	}

	function getHash() {
		hash = window.location.hash;
		if(hash.length > 0) {
			hash = hash.slice(2);
		}
		return hash;
	}

	function getUrl() {
		return window.location.href.split('#!')[0];
	}

	function setHash(hash) {
		window.location.hash = hash;
	}

	function setEventListeners() {
		$('#menu_best')		.click(loadBest);
		$('#menu_newest')	.click(loadNewest);
		$('#search_button')	.click(function(){
			search($('#menu_search').val());
		})
		$('#menu_send')		.click(loadSendImage);
	}
 
	function showSendImageForm() {
		$(contentDiv).html(sendImageTemplate());
		$('#sendImage').click(sendImage);
	}

	function loadDefault() {
		loadBest();
	}

	function loadBest(page) {
		if(typeof page == 'undefined')
			page = '';
		setHash("#!b" + page)
		loadPictures('best/' + page);
	}

	function loadTag(tag, page) {
		setHash("#!t" + tag + "," + page);
		loadPictures('tag/' + tag + '/' + page);
	}

	function loadNewest(from_time) {
		if(typeof from_time == 'undefined')
			from_time = '';
		loadPictures('newest/' + from_time);
	}

	function loadPictures(url) {
		$.ajax(url,
			{
				success: pictureLoader,
				type: 'GET',
			});
	}

	function loadSendImage() {
		$(contentDiv).empty();
		console.log(sendImageTemplate());
		$(contentDiv).append(sendImageTemplate());
		$('#sendImageForm').submit(sendImage);
	}

	function pictureLoader(responseData) {
		$(contentDiv).empty();
		for(var i = 0; i < responseData.images.length; ++i) {
				$(contentDiv).append(
					imageTemplate(responseData.images[i]
						))
		}
	}

	function singlePictureLoader(responseData) {
		$(contentDiv).empty();
		$(contentDiv).append(singleImageTemplate(responseData));
		$('head').append('<meta property="og:title" content="'+ responseData.title +'" />');
	}

	function sendImage(e) {
		e.preventDefault();
		$.post('/image/',
			$('#sendImageForm').serialize(),
			loadDefault)
	}

	function imageTemplate(image) {
		return '<div id="img' + image.id 
			+ '"><a href="#i' + image.id + '">'
			+ '<h3>' + image.title + '</h3>'
			+'<img src="' + image.url + '" alt="'
			+ image.title + '"/></a></div>'
			+ facebookLikerTemplate('#!i' + image.id);
	}

	function loadSingleImage(id) {
		$.ajax('image/' + id,
			{
				success: singlePictureLoader,
				type: 'GET'
			});
	}

	function singleImageTemplate(image) {
		return imageTemplate(image);
	}

	function sendImageTemplate() {
		return '<div>'
		+'<form id="sendImageForm" method="post" target="#!"><table>'
		+'<tr><td>Tytuł</td><td><input class="form-control" type="text" name="title" /></td></tr>'
		+'<tr><td>Plik obrazka</td><td><input class="form-control" type="file" name="image" /></td></tr>'
		+'<tr><td>Tagi (oddzielone przecinkami)</td><td><input class="form-control" type="text" name="tags" /></td></tr>'
		+'<tr><td><input value="Wyślij" type="submit" class="form-control" /></td><td></td></tr>'
		+'</table></form></div>';
	}

	function tagTemplate(tag) {
		return '<a href="'
			+ '#!t' + tag + '">' 
			+ tag
			+ "</a>";
	}

	function tagsTemplate(tags) {
		var tagTemp = [];
		for(var i = 0; i < tags.length; ++i) {
			tagTemp[i] = tagTemplate(tags[i])
		}
		return tagTemp.join(', ');
	}

	function facebookLikerTemplate(hash) {
		return '<div class="fb-like"' 
			+'data-href="' + getUrl() + hash + '" '
			+'data-layout="standard" '
			+'data-action="like" '
			+'data-show-faces="true" '
			+'data-share="true">'
		+'</div>'
	}

}) ($);
 