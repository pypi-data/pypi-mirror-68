tc
==

A robot that does the boring bits of playing Time Clickers for you using
Selenium and the WebGL version of the game, recommended for people who
have already time warped a bunch of times.

What it doesn’t do
------------------

-  Manipulate the game internally at all
-  Spend Time Cubes or Weapon Cubes for you

What it does
------------

-  Click in the centre of the screen a hundred times
-  Click the upgrade buttons for each of your team members in sequence
-  Click ‘Activate All’
-  Click Dimension Shift
-  Click Cooldown
-  Repeat

How to use it
-------------

Requirements
~~~~~~~~~~~~

-  A Time Gamers account with a Time Clickers save synced to it
-  Python 3 & pip
-  chromedriver (probably in your system’s package manager)

Installation
~~~~~~~~~~~~

-  ``pip install tc-player``

Usage
~~~~~

-  Run
   ``TC_USERNAME=[your time gamers username] TC_PASSWORD=[your time gamers password] tc``.
-  Use the
   `leaderboards <http://www.timegamers.com/TimeClickers/LiveLeaderboard/>`__
   or your profile page to check your progress.

The game uploads a cloud save every minute or so, so you can interrupt
with ``^c`` whenever you like.

But I want to see what’s going on as it happens!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Add ``TC_VISIBLE=1`` to the environment.
-  Wait.
-  After a minute or so, the settings page will appear for a moment to
   disable screen shake and post effects, and then the automation will
   begin.
-  Leave it running until you want to time warp or spend Weapon Cubes,
   at which point you should interrupt the process in your terminal and
   do so in another instance of the game.

Once it’s up and running, it’ll just keep going. Be careful when mousing
over the window, since the mouse will be clicking constantly while
you’re there.
