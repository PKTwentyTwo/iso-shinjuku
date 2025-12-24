# iso-shinjuku
A database system for glider syntheses and components, along with a related suite of supporting programs, that can work with arbitrary INT rules. 
## Introduction
In Conway's Game of Life (and related cellular automata), glider synthesis is the act of colliding a number of copies of the glider (which is usually one of, if not the smallest spaceship in the rule) to produce a target object.

For standard Life, a database already exists to store and make glider syntheses: Jeremy Tan's [Shinjuku](https://gitlab.com/parclytaxel/Shinjuku), named after [the busiest train station in the world](https://en.wikipedia.org/wiki/Shinjuku_Station).

However, while it is very efficient, it only works for one rule out of the 2<sup>82</sup> (roughly 4.84 septillion) rules where the glider exists, and many of these rules have enough long-term investigation that storing glider syntheses is useful.
Examples include:
- Pedestrian Life (B38/S23)
- EightLife (B3/S238)
- LeapLife (B2n3/S23-q)
- Travelling Ts (B3/S23-a5)

Previous attempts at finding and documenting syntheses in these rules have often been inefficient and disorganised, which is why I created this database system.

## System, not database
As there are 2<sup>82</sup> rules that might need to be kept track of, a database for all of them would require millions of yottabytes. Instead, the project is a database system; peoople investigating rules can fork this repository, add the contributers to the rule as contributers to their fork, then keep the database updated through merge/push requests.

## Setup
The requirements to run the software can be found in [/doc](doc). Alternatively, on Linux and WSL, you can run [setup.sh](setup.sh), which will install all necessary dependencies.

## Command line interface
To interact with a locally cloned copy of the database, run [syncmd.py](syncmd.py). It is a command line interface with commands suited for uploading components and compiling syntheses. Documentation of commands can be found in /doc/cmd, or by running the command 'help'.

A graphical user interface is being developed as an alternative to the CLI.

## Utility software
iso-shinjuku also comes with a range of utility programs for finding glider syntheses/components, located in [/util](util). Separate documentation can be found in /util/doc.
These programs include:
- getstarted.py - Randomly searches 12000 collisions with 2-5 gliders, then collides one glider with all of the results, saving the results of both searches to a text file.
- downloadsynth.py - Can download syntheses from a Catagolue stdin symmetry, which is created by someone piping glider collisions into apgmera. More information can be found [here](https://conwaylife.com/wiki/Tutorials/Catagolue_stdin_symmetry).
