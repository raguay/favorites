#
# Load the libraries that are used in these commands.
#
from core.quicksearch_matchers import contains_chars
from fman import DirectoryPaneCommand, DirectoryPaneListener, show_alert, load_json, DATA_DIRECTORY, show_prompt, show_quicksearch, QuicksearchItem, show_status_message, clear_status_message
import os, stat, re

#
# I'm using two globals because it is faster for checking
# the directories. I also have an Alfred workflow that makes
# use of this information. These globals point to the list
# of favaorite directories and shortener directories.
#
FAVORITELIST = os.path.expanduser("~") + "/.favoritedirs"
SHORTENERLIST = os.path.expanduser("~") + "/.shortenerdirs"

#
# Function:    GoToFavaorite
#
# Description: This class performs the operation of going
#              to a favorite directory that the user
#              selects.
#
class GoToFavorite(DirectoryPaneCommand):
    #
    # This directory command is for selecting a project
    # and going to that directory.
    #
    def __call__(self):
        show_status_message('Favorite Selection')
        result = show_quicksearch(self._suggest_directory)
        if result:
            query, dirName = result
            directories = ["Home|~"]
            if os.path.isfile(FAVORITELIST):
                with open(FAVORITELIST, "r") as f:
                    directories = f.readlines()
            for dirTuple in directories:
                if dirTuple.find("|") > 0:
                    favName, favPath = dirTuple.strip().split('|')
                    if favName == dirName:
                        self.pane.set_path(expandDirPath(favPath + os.sep))
        clear_status_message()

    def _suggest_directory(self, query):
        directories = ["Home|~"]
        if os.path.isfile(FAVORITELIST):
            with open(FAVORITELIST, "r") as f:
                directories = f.readlines()
        for dirTuple in directories:
            if dirTuple.strip() != "":
                dirName = dirTuple.split('|')[0]
                match = contains_chars(dirName.lower(), query.lower())
                if match or not query:
                    yield QuicksearchItem(dirName, highlight=match)

#
# Function:    RemoveFavoriteDirectory
#
# Description: This class performs the function of
#              removing a favorite directory.
#
class RemoveFavoriteDirectory(DirectoryPaneCommand):
    #
    # This directory command is for selecting a favorite
    # and deleting it.
    #
    def __call__(self):
        show_status_message('Remove Favorite Directory')
        result = show_quicksearch(self._suggest_favorite)
        if result:
            query, dirName = result
            if os.path.isfile(FAVORITELIST):
                with open(FAVORITELIST, "r") as f:
                    directories = f.readlines()
                with open(FAVORITELIST, "w") as f:
                    for dirTuple in directories:
                        favName = dirTuple.split('|')[0]
                        if favName != dirName:
                            f.write(dirTuple)
        clear_status_message()

    def _suggest_favorite(self, query):
        favorites = [""]
        if os.path.isfile(FAVORITELIST):
            with open(FAVORITELIST, "r") as f:
                favorites = f.readlines()
        for favTuple in favorites:
            if favTuple.strip() != "":
                favName = favTuple.split('|')[0]
                match = contains_chars(favName.lower(), query.lower())
                if match or not query:
                    yield QuicksearchItem(favName, highlight=match)
#
# Function:    RemoveShortenerDirectory
#
# Description: This class performs the function of
#              removing a shortener directory.
#
class RemoveShortenerDirectory(DirectoryPaneCommand):
    #
    # This directory command is for selecting a favorite
    # and deleting it.
    #
    def __call__(self):
        show_status_message('Remove Shortener Directory')
        result = show_quicksearch(self._suggest_shortener)
        if result:
            #
            # Remove the shortener from the list of
            # shorteners.
            #
            query, shortName = result
            shortenDir = ''
            if os.path.isfile(SHORTENERLIST):
                with open(SHORTENERLIST, "r") as f:
                    directories = f.readlines()
                with open(SHORTENERLIST, "w") as f:
                    for dirTuple in directories:
                        if dirTuple.find("|") > 0:
                            shortenerName, shortDir = dirTuple.strip().split('|')
                            if shortenerName != shortName:
                                f.write(dirTuple)
                            else:
                                shortenDir = shortDir
            #
            # Remove the shortener from all favorites.
            #
            if os.path.isfile(FAVORITELIST):
                favorties = ["Home|~"]
                with open(FAVORITELIST,"r") as f:
                    favorties = f.readlines()
                pattern = re.compile("\{\{" + shortName + "\}\}(.*)$")
                with open(FAVORITELIST,"w") as f:
                    for fav in favorties:
                        if fav.find("|") > 0:
                            favName, favPath = fav.strip().split('|')
                            match = pattern.search(favPath)
                            if match:
                                favPath = shortenDir + match.group(1)
                            f.write(favName + "|" + favPath + "\n")
        clear_status_message()

    def _suggest_shortener(self, query):
        shorteners = ["No shorteners are setup."]
        if os.path.isfile(SHORTENERLIST):
            with open(SHORTENERLIST, "r") as f:
                shorteners = f.readlines()
        for shortTuple in shorteners:
            if shortTuple.strip() != "":
                shortName = shortTuple.split('|')[0]
                match = contains_chars(shortName.lower(), query.lower())
                if match or not query:
                    yield QuicksearchItem(shortName, highlight=match)

#
# Function:    SetFavoriteDirectory
#
# Description: This class performs the command to set
#              a favorite directory. If the directory
#              path contains a directory specified as a
#              shortener, then the path is shortened to that
#              shortener. Otherwise, it will shorten the path
#              to the home directory.
#
class SetFavoriteDirectory(DirectoryPaneCommand):
    #
    # This dirctory command is for setting up a new project
    # directory. It will add to the list of project directories
    # and set the current project directory to the directory.     #
    def __call__(self):
        #
        # Get the directory path.
        #
        selected_files = self.pane.get_selected_files()
        if len(selected_files) >= 1 or (len(selected_files) == 0 and self.get_chosen_files()):
            if len(selected_files) == 0 and self.get_chosen_files():
                selected_files.append(self.get_chosen_files()[0])
            dirName = selected_files[0]
            if os.path.isfile(dirName):
                #
                # It's a file, not a directory. Get the directory
                # name for this file's parent directory.
                #
                dirName = os.path.dirname(dirName)
            #
            # Add to the list of projects. Get a name
            # from the user.
            #
            dirName = shortenDirPath(dirName)
            favName, checked = show_prompt("Name this Favorite:")
            favEntry = favName + "|" + dirName
            writeappend = 'w'
            if os.path.isfile(FAVORITELIST):
                writeappend = 'a'
            with open(FAVORITELIST,writeappend) as f:
                f.write(favEntry+"\n")

#
# Function:    SetShortenDirectory
#
# Description: This class will set a new shortener directory. It
#              will ask the user for a name for the shortener.
#
class SetShortenDirectory(DirectoryPaneCommand):
    #
    # This dirctory command is for setting up a new project
    # directory. It will add to the list of project directories
    # and set the current project directory to the directory.     #
    def __call__(self):
        #
        # Get the directory path.
        #
        selected_files = self.pane.get_selected_files()
        if len(selected_files) >= 1 or (len(selected_files) == 0 and self.get_chosen_files()):
            if len(selected_files) == 0 and self.get_chosen_files():
                selected_files.append(self.get_chosen_files()[0])
            dirName = selected_files[0]
            if os.path.isfile(dirName):
                #
                # It's a file, not a directory. Get the directory
                # name for this file's parent directory.
                #
                dirName = os.path.dirname(dirName)
            #
            # Add to the list of projects. Get a name
            # from the user.
            #
            shortener, checked = show_prompt("Name this Directory Shortener:")
            shortEntry = shortener + "|" + dirName
            writeappend = 'w'
            if os.path.isfile(SHORTENERLIST):
                writeappend = 'a'
            with open(SHORTENERLIST,writeappend) as f:
                f.write(shortEntry+"\n")

#
# Function:    expandDirPath
#
# Description: This function takes a shortened path. If first
#              checks for a shortener in the path. If there is,
#              it expands to that path. Otherwise, it tries to
#              take a home directory relative path and make it
#              an absolute path.
#
def expandDirPath(dir):
    dirName = dir
    pattern = re.compile("\{\{(.*)\}\}")
    match = pattern.search(dir)
    if match:
        if os.path.isfile(SHORTENERLIST):
          with open(SHORTENERLIST,"r") as f:
            shorteners = f.readlines()
            for shortener in shorteners:
                shortName, shortPath = shortener.strip().split('|')
                if match.group(1) == shortName:
                    dirName = shortPath + dir[match.end(1)+2:]
    return os.path.expanduser(dirName)

#
# Function:    shortenDirPath
#
# Description: This function takes a diretory path. It looks for
#              that path to be a shortener directory. If it is, it
#              shortens it to that directory. Otherwise, it makes
#              the path relative to the Home directory if it is
#              a child directory of the home directory.
#
def shortenDirPath(dir):
    dirName = dir
    if os.path.isfile(SHORTENERLIST):
        with open(SHORTENERLIST,"r") as f:
            shorteners = f.readlines()
            for shortener in shorteners:
                pathName,path = shortener.strip().split('|')
                if path_is_parent(path,dirName):
                    dirName = "{{" + pathName + "}}/" + os.path.relpath(dirName,path)
    if path_is_parent(os.path.expanduser("~"),dirName):
        dirName = '~/' + os.path.relpath(dirName,os.path.expanduser("~"))
    return dirName

#
# The following function was taken from [StackOverflow](https://stackoverflow.com/questions/3812849/how-to-check-whether-a-directory-is-a-sub-directory-of-another-directory)
#
def path_is_parent(parent_path, child_path):
    # Smooth out relative path names, note: if you are concerned about symbolic links, you should use os.path.realpath too
    parent_path = os.path.abspath(parent_path)
    child_path = os.path.abspath(child_path)

    # Compare the common path of the parent and child path with the common path of just the parent path. Using the commonpath method on just the parent path will regularise the path name in the same way as the comparison that deals with both paths, removing any trailing path separator
    return os.path.commonpath([parent_path]) == os.path.commonpath([parent_path, child_path])