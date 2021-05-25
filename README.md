# SIMULATION OF AUDIO SERVER
## Implenting CRUD API with Flask Python Framework
### Simulating the behavior of an audio file server
## Features
consummers can send
- get request
- send post request
- send update request
- delete audio request

## API CONSUMPTION

<P><b>WEB URL </b>
    https://filedaudioserver.herokuapp.com/</P>

    <h3>API ENDPOINTS FORMAT</h3>
<p>for all audio:  https://filedaudioserver.herokuapp.com/api/v1/resources/audiotype
    
for single audio: https://filedaudioserver.herokuapp.com/api/v1/resources/audiotype/id
	<br>
	where id = 1,2,3,.....</p>

<h3>GET REQUEST</h3>
<p> https://filedaudioserver.herokuapp.com/api/v1/resources/song<br>
	return all song<br>
https://filedaudioserver.herokuapp.com/api/v1/resources/podcast<br>
	return all podcast<br>
https://filedaudioserver.herokuapp.com/api/v1/resources/audiobook<br>
	return all audiobook<br>

https://filedaudioserver.herokuapp.com/api/v1/resources/song/id<br>
	return single song<br>
	where id = 1,2,3,.....<br>
	same for podcast and audiobook just change the song in the url to podcast and audiobook respectively
</p>

<h3>FOR POST REQUEST</h3>
<p>
url = https://filedaudioserver.herokuapp.com/api/v1/resources/audiotype<br>
where audiotype at the end of the url be replaced with "song" or "podcast" or "audiobook"<br>
and the body of the request for each adiotype are:<br>

<b>for song audiotype, use this format</b><br>
	{
	</br>
        "name_of_song": "I'm the name",<br>
        "duration": 36,      <br>
    }
    </br>

<b> for podcast audiotype use this format</b><br>
	{
	</br>
        "name_of_podcast": "I'm the name",<br>
	"duration": 36,<br>
        "host": "Brian",<br>
        "participants": "Brian, Mumeen Updated"<br>
    }
    </br>

<b>for audiobook audiotype use this format</b><br>
	{
        "title_of_audiobook": "I'm the title",<br>
        "duration": 36,<br>
        "narrator": "Abdlazeez",<br>
        "author": "Brian, Mumeen"<br>
           
    }
</p>

<h3>FOR UPDATE AND DELETE REQUEST</h3>
<p>
use the same request body format as post request except adding the id of the audio to be deleted to the end of the url
</br>
url  = https://filedaudioserver.herokuapp.com/api/v1/resources/audiotype/id
</p>
