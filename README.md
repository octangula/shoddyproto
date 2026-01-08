# shoddyproto
rika's protojson, not exactly rfc compliant. i have not touched this in a year or two(long enough that i specified windows-1252 encoding) but i still use it regularly when gathering data(even if just to make sure i stick to consistent naming conventions for keys) so may as well archive somewhere..<br><br>
here is an example youtube.channel schema<br>
```
{
	"exists": 0,
	"metadata": {
		"title": 1,
		"blocked_countries": 2,
		"id": 3,
	},
	"videos": [
		4,
		"youtube.video"
	]
}

```
you would then have a matching youtube.video schema, ie:<br>
```
{
  "id": 0,
  "time_created_seconds": 1,
}
```
you want to put your schemas somewhere to match the path in the get_schema function, ie. shoddyproto/youtube/channel.json<br><br>
one day this will be complete with a binary conversion when i need it, until then this is probably a useless feat for most people..
