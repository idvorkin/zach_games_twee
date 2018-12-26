# zach_games_twee

A place to store Zach's twee games

## Installation

Install tweego to \tweego
Install story formats to \tweego

### Usage

This repo contains twee.bat which calls ```\tweego\tweego.exe```

Decompile story format from twine

    twee story.html -d > story.twee

Compile twee story to something twine can import (using sugar cube format)

    twee -f sugarcube-2 -o story.exported.html story.twee --start start
