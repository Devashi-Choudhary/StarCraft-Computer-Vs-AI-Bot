# What are Real Time Strategy(RTS) games?

Real Time Strategy(RTS) games are kind of video
games which are emerging as a strong domain in
Artificial Intelligence. When we analyze these
games ,strong human minds are able to defeat artificial
agents. The structure of most of the RTS games like Age
of Empires, Warcrafts, starcraft and many more is very
complex and consist of many modules like Build
Orders, Collecting Resources, Managing Army etc for
unit control and strategy selection. These modules
implement different AI mechanisms and interact with
each other. Thus, the aim of current project is to build AI Bot for starcraft game,  where our AI bot plays against other players, or computers, where we start with a "base," which allows us to build basic units that collect resources. From here, we can build more buildings that unlock new units, like combat units, and then we can do things like purchase/research upgrades for units or for even better units. Eventually, our objective is to amass an army to take out your opponents.

**Note :** In the current project we are using **StarCraft II**. In mid 2017 the DeepMind and Blizzard (the creators of StarCraft II) developed starcraft II API for interacting with the strategy game. In StarCraft II, there are 3 "races:" Terran, Protoss, and Zerg. The Protoss are more technology/robotics-based, so we have used that.

![gif](https://github.com/Devashi-Choudhary/StarCraft-Computer-Vs-AI-Bot/blob/master/ReadMe_Images/giphy.gif)

# Installation and Dependencies

1. First, you need to download the [StarCraft II](https://www.blizzard.com/en-us/download) game. You need to signup for an account then you can download it and install the game. If you installed StarCraft II to a custom directory/drive, then you need to go to sc2/paths.py, and change the basedir value to match yours. 
2. Make sure you have the correct version of [Python](https://www.python.org/downloads/windows/) installed on your machine. This code runs on Python 3.6 above.
3. Now you need to install [python-sc2](https://github.com/Dentosal/python-sc2), which is an easy-to-use library for writing AI Bots for StarCraft II in Python 3. There's also [pysc2](https://github.com/deepmind/pysc2#:~:text=Get%20StarCraft%20II,the%20API%2C%20which%20is%203.16.), which is [DeepMind's](https://deepmind.com/) Python library, but it is more suitable most likely for deep-learning bots. We have used sc2 for our project. You can install by running the following command on terminal.

`pip install sc2`

4. Now, you need to download the Maps from [Map Packs section of the Blizzard s2client ](https://github.com/Blizzard/s2client-proto#map-packs). Once, you have downloaded the maps, extract them to a Maps directory from within your StarCraft II directory. Each set of maps should be in a *subdirectory* of the Maps directory. For example, the file structure should be something like:

> StarCraft II

> -Maps

> --Ladder2017Season1

> ---AbyssalReefLE.SC2Map

5. Now, you have all the required dependencies. You have to download the repository and then extract the contents into a folder and run the following command in your Terminal/Command Prompt.

`python starcraft.py`

# Results


# Contributors

[Neha Goyal](https://github.com/Neha-16)

[Trisha Dutta](https://github.com/Trisha73)

# Acknowledgement

The project was done as a part of Artificial Intelligence subject for understanding the working of AI Bots and it is inspired by the [StarCraft II AI python sc2 Tutorial](https://pythonprogramming.net/starcraft-ii-ai-python-sc2-tutorial/) 
