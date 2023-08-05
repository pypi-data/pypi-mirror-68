<center><h1>digital-camera-photo-geolocation CLI</h1></center>

# What is CLI (Command-line Interface)
A command-line interface (CLI) processes commands to a computer program in the form of lines of text. The program which handles the interface is called a command-line interpreter or command-line processor. Operating systems implement a command-line interface in a shell for interactive access to operating system functions or services. Such access was primarily provided to users by computer terminals starting in the mid-1960s, and continued to be used throughout the 1970s and 1980s on VAX/VMS, Unix systems and personal computer systems including DOS, CP/M and Apple DOS.

# What is Shell

A [shell](<https://en.wikipedia.org/wiki/Shell_(computing)>) is a program that lets you type a command, possibly followed by some parameters, and press the `Enter`/`Return` key to execute that command. The shell processes the command and returns output. You can then type a new command. A shell supports many advanced features such as running script files, running commands in the background, chaining commands together, etc.

One of the most widely used shell for Unix-like operating systems is [`bash`](<https://en.wikipedia.org/wiki/Bash_(Unix_shell)>). Besides `bash`, there are [other shell programs](https://en.wikipedia.org/wiki/Comparison_of_command_shells) that can be installed in your operating system.

The problem is that shells may use different interpreters, different command syntax and levels of programmability. For instance, if you want to list the files of a directory, you have to type the command `dir` with `Command Prompt` (Windows), while you have to type the command `ls` with `bash` (Unix-like).

# Requirement
+ Python 3.*
+ pipenv

# Usage
+ Install all the requirement packages in Pipfile:
```
> pipenv install
```

+ Run the CLI:
```
> dslgtool
```

# Changelog

+ 1.0.0
    + Initial release


# Lisence
```
MIT License

Copyright (c) 2020 Lam Duc Long - Le Quang Nhat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```