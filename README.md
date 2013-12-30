twanalyze
=========

Twanalyze downloads account information and up to 3200 of the most recent tweets for the specified screen_name. The downloaded tweets are analyzed and a report is generated that includes the top 20 hashtags, mentions, links, tweet times, locations, and phrases used in each tweet.

Prerequisites
-------------
Twanalyze is dependent on the [requests](http://docs.python-requests.org/en/latest/index.html), [simplekml](http://simplekml.readthedocs.org/en/latest/), and [nltk](http://nltk.org/) libraries.
* `pip install requests`
* `pip install simplekml`
* `pip install nltk`

Twanalyze also needs a Twitter API key. You can get an API key by signing in to https://dev.twitter.com/apps with your Twitter username and password. Once you are signed in, click Create a new application.

Configuration
-------------
Once you have obtained the Twitter API key, you will need to add the consumer key, consumer secret, token, and token_secret to the twanalyze.config.template file and rename the file to twanalyze.config.

Usage
-----
To use twanalyze, provide a Twitter screen_name, a report file name, and a report format.

`python twanalyze.py screen_name filename html|kml|md|raw|all`

Report Formats
--------------
Twanalyze supports four report formats, which are described below. A report format must be specified when launching the script. If an invalid report format is given then a Markdown report will be generated.

* Markdown - Creates a Markdown formatted report with user details and the analysis results.
* HTML - Creates an HTML formatted report with user details and the analysis results.
* KML - Creates a KML file with lat and lon coordinates and timestamp for any tweets that contain location data.
* Raw - Creates a JSON file with all of the downloaded user data and tweets. This could be a very large file.
* All - Creates reports in Markdown, HTML, and KML formats.

Sample Markdown Report
----------------------
	Twanalyze Report
	================
	averagesecguy
	-------------
	Name: Stephen Haywood
	Description: I have worked professionally as a programmer, school teacher, computer teacher, sysadmin and now as an information security auditor.
	Location: 
	Time Zone: Eastern Time (US & Canada)
	UTC Offset: -5
	Tweets: 4916
	Favorites: 612
	Listed: 40
	Followers: 920
	Following: 392

	Hashtags
	--------
	#dc423 - 15
	##dc423 - 8
	#derbycon - 8
	#cispa - 7
	#secchat - 7
	#ff - 5
	#python - 5
	#cha - 4
	#chabiz - 4
	#dc865 - 4
	#derbycon. - 4
	#infosec - 3
	#latenighthacking - 3
	#metasploit - 3
	#shodan - 3
	#cfaa - 2
	#cha. - 2
	#dc423. - 2
	#dc865. - 2
	#fivewordtechhorror - 2

	Mentions
	--------
	@sawaba - 100
	@tothehilt - 100
	@jakx_ - 83
	@jgamblin - 75
	@synackpwn - 69
	@adamcaudill - 68
	@tatanus - 57
	@jimmyvo - 50
	@itsecurity - 43
	@erickolb - 42
	@gepeto42 - 38
	@carlos_perez - 36
	@hrbrmstr - 35
	@jadedsecurity - 35
	@jodieswafford - 35
	@dave_rel1k - 34
	@gattaca - 33
	@netpwn - 30
	@mubix - 27
	@0xabad1dea - 26

	Links
	-----
	https://t.co/pYTSa5dkkV - 4
	http://t.co/fuClE544f2 - 3
	https://t.co/o31LqifFFf - 3
	https://t.co/t8v9VZytw7 - 3
	http://t.co/0fSolBwg - 2
	http://t.co/4sWv7a3J - 2
	http://t.co/8XeKy5KGzD - 2
	http://t.co/CdLRaji0ZZ - 2
	http://t.co/DX41GkciCH - 2
	http://t.co/Fb0L6GJh - 2
	http://t.co/G3Dasqn3 - 2
	http://t.co/Ir549YJc - 2
	http://t.co/J15cxqJYX8 - 2
	http://t.co/Jqqi0uFFsq - 2
	http://t.co/L2a42NuF0K - 2
	http://t.co/Q3sfeINBKM - 2
	http://t.co/bRK3c8u2 - 2
	http://t.co/bmfySo3D - 2
	http://t.co/dhkwMb79w5 - 2
	http://t.co/fkCqdyPlKn - 2

	3-word Phrases
	--------------
	thanks for the - 34
	a lot of - 25
	if you are - 21
	let me know - 20
	i have to - 17
	if you have - 15
	me know if - 14
	be able to - 13
	i want to - 13
	looking forward to - 13
	i need to - 12
	know if you - 12
	how do you - 11
	i have a - 11
	let me know. - 11
	you have to - 11
	a couple of - 9
	is there a - 9
	what is the - 9
	how do i - 8

	4-word Phrases
	--------------
	let me know if - 14
	me know if you - 10
	may be able to - 7
	[at] averagesecurityguy [dot] info - 6
	know if you have - 6
	stephen [at] averagesecurityguy [dot] - 6
	thanks for the help. - 6
	if you are a - 5
	if you have any - 5
	this looks like a - 5
	but i don't think - 4
	is one of the - 4
	not the same as - 4
	thanks for the offer. - 4
	@jodieswafford @jakx_ @erickolb @sawaba - 3
	@tatanus @jodieswafford @jakx_ @erickolb - 3
	a good way to - 3
	a lot of good - 3
	anyone know of a - 3
	can anyone recommend a - 3

	5-word Phrases
	--------------
	let me know if you - 10
	stephen [at] averagesecurityguy [dot] info - 6
	me know if you have - 5
	know if you have any - 4
	@tatanus @jodieswafford @jakx_ @erickolb @sawaba - 3
	if you have any questions. - 3
	is it just me or - 3
	is not the same as - 3
	let me know if there - 3
	wish i could have been - 3
	14. if you are a - 2
	@csoandy @gisellis so wim, which - 2
	@csoandy that is the biggest - 2
	@gisellis so wim, which ones - 2
	@hrbrmstr @jaredpfost @jayjacobs added a - 2
	@isaiahmc yes, i have the - 2
	@jadedsecurity @thegrugq @chort0 @amazingant @dakami - 2
	@jaredpfost @jayjacobs added a better - 2
	@jayjacobs added a better explanation. - 2
	@jimmyvo i'll never be bought - 2

	Timestamps
	----------
	15:00:00 +0000 - 281
	14:00:00 +0000 - 269
	19:00:00 +0000 - 255
	17:00:00 +0000 - 235
	18:00:00 +0000 - 223
	16:00:00 +0000 - 201
	20:00:00 +0000 - 191
	01:00:00 +0000 - 150
	13:00:00 +0000 - 145
	03:00:00 +0000 - 144
	02:00:00 +0000 - 133
	21:00:00 +0000 - 117
	00:00:00 +0000 - 114
	23:00:00 +0000 - 111
	22:00:00 +0000 - 96
	04:00:00 +0000 - 75
	05:00:00 +0000 - 54
	12:00:00 +0000 - 36
	06:00:00 +0000 - 12
	07:00:00 +0000 - 4

