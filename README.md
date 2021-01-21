## Favorites

Plugin for [fman.io](https://fman.io) that gives you the ability to setup a list of favorite directories to go to.

You can install this plugin by pressing `<shift+cmd+p>` to open the command pallet. Then type `install plugin`. Look for the `favorite` plugin and select it.

After restarting **fman**, you will have the ability to set favorite directories, go to them, set path shorteners, remove path shorteners, remove favorites, and set/go to four directory locations kept in memory.

### Usage

#### HotKeys Set

<Shift+f>  - Set a new Favorite directory. This makes the current directory in the active pane a favorite directory.

<Ctrl+f> - Remove a Favorite Directory.

<Ctrl+0> - Go to a Favorite Directory.

<Ctrl+1> - Pop up first previous directory.

<Ctrl+2> - Pop up second previous directory.

<Ctrl+3> - Pop up third previous directory.

<Ctrl+4> - Pop up fourth previous directory.

<Ctrl+5> - Pop up fifth previous directory.

<Ctrl+6> - Pop up sixth previous directory.

<Ctrl+7> - Pop up seventh previous directory.

<Ctrl+8> - Pop up the eighth previous directory.

<Cmd+1> - Set the first directory memory to the current panel's directory.

<Cmd+2> - Set the second directory memory to the current panel's directory.

<Cmd+3> - Set the third directory memory to the current panel's directory.

<Cmd+4> - Set the fourth directory memory to the current panel's directory.

<Alt+1> - Set the current panel to go to the first directory memory location.

<Alt+2> - Set the current panel to go to the second directory memory location.

<Alt+3> - Set the current panel to go to the third directory memory location.

<Alt+4> - Set the current panel to go to the fourth directory memory location.

#### Commands

`Go To Favorite` - This command will display a list of favorites by their assigned names for the user to choose from. As you type letters in the name, the list is shortened. Once one is selected, the current panel is moved to that directory.

`Go To Favorite Pair` - This command will display a list of favorite directory pairs by their assigned name. When the user selects one, the left and right directories will be set as saved.

`Remove Favorite Directory` - This command will remove the selected favorite directory.

`Remove Favorite Directory Pair` - This command will remove the selected favorite directory pair.

`Set Favorite Directory` - This command sets the currently highlighted directory as a favorite. If the path contains a shortener's path, then it will be shortened to that shorener's name in double brackets.

`Set Favorite Dirctory Pair` - This command sets a left and right directory structure to save.

`Set Shorten Directory` - This command asks the user for a shortener name and creates a new shortener to that directory.

`Remove Shortener Directory` - This command removes a shortener directory from the shortener list. It then expands the shortener in all the favorites that had that shortener.

`Go to hot dir` - This command set the current panel to the directory store in the memory location specified in the dirNum argument. The default is 0.

`Set hot dir` - This command set the current panel to the directory store in the memory location 1 specified in the dirNum argument. The default is 0.

`pop directory` - This command pops to the previous directory.

#### Files Created and Used

`~/.favoritedirs` - This file contains all of your favorite directories. Each line is the assigned name, a "|" symbol, and the path to the directory. If the path contains a directory in the `~/.shorenerdirs` file, then the path is removed and a placeholder is inserted instead.

`~/.shortenerdirs` - This file contains all the shortener directories and their names. It is in the same format as the `~/.favoritedirs` file. Once you create this file, copy it to your Dropbox location and link it back to this location. Now you can share your favorites between systems.

#### Suggested Usage

Once you install the plugin, set up your shortener directories. I setup one for each of my Dropbox locations. Then, create your favorites in the shorteners subdirectories. Once you have the favorites setup, move your `~/.favoritedirs` to your Dropbox location you want and  link to the original location and name. On the second system, setup the same shortener file using the same names and link the synced favoritedirs file to the normal location. Now you can go to the favorite directories inside these shortener directories easily! They also automatically update when you add new ones.

You can also save and restore directory locations in the internal memory. There are four memory locations set aside to use. Very useful for saving a location, going somewhere else, and then popping right back to the previous location. These locations are lost when exiting fman.

### Features

- The ability to set a favorite directory.
- The ability to go to a favorite directory.
- The ability to set a favorite directory pair.
- The ability to go to a favorite directory pair.
- Remove a favorite directory.
- Remove a favorite directory pair.
- Set up directories as shorteners with a name. Then all paths under that directory will be set to the shortener's name and expanded to that path when going to it. This gives the ability to share favorites between system just using the paths in common.
- There are four memory locations to set directory values that can be easily recalled as well. Store from any panel and restore to any panel.
- The ability to backtrack previously visited directories. Not panel specific.

