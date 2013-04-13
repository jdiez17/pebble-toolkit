pebble-toolkit
==============

A Python script that helps you manage and compile Pebble projects. 

Installation
============

Clone the repository:

    $ git clone git@github.com:jdiez17/pebble-toolkit.git

Install the dependencies:

    $ pip install requests docopt 

Cloud compilation
==================

The main feature of pebble-toolkit is the fact that it can offload the compilation of Pebble apps to a remote server.
I've set up my own build server and the script is configured to send files to it by default, but you can write your own backend.

When the compilation is finished, a web browser is opened with a 500x500 QR Code. Scan it with your phone and the file will be downloaded to your Pebble.
