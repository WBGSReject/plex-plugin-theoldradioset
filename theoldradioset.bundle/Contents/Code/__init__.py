#############
## credit to DiegoV in New Zealand for some nice simple code to work from
#############
ART      = 'art-default.jpg'
ICON     = 'icon-default.png'

PREFIX = '/music/theoldradioset'

####################################################################################################

# This function is initially called by the PMS framework to initialize the plugin. This includes
# setting up the Plugin static instance along with the displayed artwork.
def Start():
    # Initialize the plugin
    Plugin.AddViewGroup('the_view_group', viewMode = 'List', mediaType = 'items')

    # Setup the artwork associated with the plugin
    ObjectContainer.title1 = 'The Old Radio Set'
    ObjectContainer.art = R(ART)
    ObjectContainer.view_group = 'the_view_group'

    #DirectoryObject.thumb = R(ICON)

    TrackObject.thumb = R(ICON)
    TrackObject.art = R(ART)

####################################################################################################

@handler(PREFIX, 'The Old Radio Set')
def MainMenu():

    # Would love to call this periodically to update the channel background art, but not possible
    # oc.art = HTTP.Request('http://radioparadise.com/readtxt.php').content

	PLAYLIST_URL_MP3 = Prefs['mp3_url']
	PLAYLIST_TITLE = Prefs['stream_title']

	oc = ObjectContainer()
	oc.add(CreateTrackObject(url=PLAYLIST_URL_MP3, title=PLAYLIST_TITLE, fmt='mp3'))
	
	#AAC audio playback does not appear to work at the moment

	return oc


####################################################################################################
def CreateTrackObject(url, title, fmt, include_container=False):

	if fmt == 'mp3':
		container = Container.MP3
		audio_codec = AudioCodec.MP3
	elif fmt == 'aac':
		container = Container.MP4
		audio_codec = AudioCodec.AAC

	track_object = TrackObject(
		key = Callback(CreateTrackObject, url=url, title=title, fmt=fmt, include_container=True),
		rating_key = url,
		title = title,
		items = [
			MediaObject(
				parts = [
					PartObject(key=Callback(PlayAudio, url=url, ext=fmt))
				],
				container = container,
				audio_codec = audio_codec,
				audio_channels = 2
			)
		]
	)

	if include_container:
		return ObjectContainer(objects=[track_object])
	else:
		return track_object

####################################################################################################
def PlayAudio(url):

	return Redirect(url)
