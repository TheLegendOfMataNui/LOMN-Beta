The Legend of Mata Nui
======================

This repo contains everything needed to build the game.

Prerequisites
-------------

To build LOMN, you need:
 - [sage-js](https://github.com/TheLegendOfMataNui/sage-js) on your `PATH` for compiling the scripts (get it by installing [NodeJS](https://nodejs.org/en/download/) and using `npm install -g @sage-js/cli`)
 - [Python 2 (Not 3!)](https://www.python.org/downloads/) on your `PATH` for packaging the blockfiles

Building
--------

Open a command prompt in the base directory and run `make`. It will take a long time the first time, but it won't need your input while it's building, so you can go do whatever.  
The built game will be created in the `build/` directory, and you can run it by opening `LEGOBionicle.exe`.

You can also run `make clean` to delete the `build/` folder, `make rebuild` to `clean` and then build, or `make run` to `build` and then launch the game.

When using `make`, you can use ` COMPRESSION=compressed` with a `make` command (e.g. `make COMPRESSION=compressed`) to compress the blockfiles, but be warned: they will not be rebuilt even if they are up-to-date but not compressed, and compression will slow the process down significantly.

**NOTE**
If you modify or add a file in a blockfile, running `make` will rebuild that blockfile. However, deleting a file in a blockfile will not be detected by `make`, so you will need to manually trigger the rebuild by either deleting the corresponding `.blk` file in the `build/data/` directories, or running `make clean` to rebuild the whole game. (Again, this takes a long time!)

Script Development
------------------

If you are working frequently on the `.osas` script files, you probably want the VS-OSI Visual Studio extension that adds code folding, syntax coloring, autocomplete suggestions, and more.  
You can find VS-OSI [here](https://github.com/TheLegendOfMataNui/VS-OSI).