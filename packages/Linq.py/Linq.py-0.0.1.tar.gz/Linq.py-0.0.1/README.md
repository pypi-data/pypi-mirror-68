# What is this?
Linq.py is a simple py engine used mostly for file writing and as a game engine. It is not intended for commercial use but for personal use.
# Commands
## Fs
### fs.write(content, path, filename) 
This will write the content to a file specified in the path!
### fs.read(path, log)
This will read from the specified path + file (./data/test.txt) and will print it if the log is True.

For printing single content:
fs.read(path, True)

Output: Hey (example)

For printing with own words:

fs.read(path, 'i said')
Output: I said Hey!

## Game (NOT DONE YET)

### Player
#### Player.setusername(name)
This will write the users name to a Data folder

#### Player.username()
This will print the players username
