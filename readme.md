# MCB80x VO Tool

A simple Sublime Text plugin for helping with voice-over recording workflow.

## Dependencies

* SoX --- Sound Exchange Project ([sox.sourceforge.net])

	`brew install sox`

* Sublime Text 2

* Mac OS X

* iTerm2


## Installation

The file `recaudio.py` file should go in 

	`~/Library/Application Support/SublimeText2/Packages/User/`

Additionally, lines like this:


	{ "keys": ["ctrl+alt+a"], "command": "record_audio" },
	{ "keys": ["ctrl+alt+l"], "command": "add_vo_line_numbers" }


should be added to the keymap file (accessible from the preferences menu)

## Usage

`ctl+alt+l` will number the lines in a script file (e.g. add `[00010]` style
numbering).

`ctl+alt+a` will record the current line, and store it in `~/Desktop/recordings/` with
a name derived from the line number and line content