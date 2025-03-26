Py!OsuAuto V2
=============

**DISCLAIMERS:**

- This bot is made for educational purposes only. I do not recommend using it on your account, log off before doing so.  

- **THIS BOT DOES NOT AUTOMATICALLY CLICK. IT ONLY _AIMS_. THIS IS DONE TO DISCOURAGE CHEATERS.**

Py!OsuAuto V2 is like [Py!OsuAuto](https://github.com/victorborneo/Py-OsuAuto), but _better_!

See the showcase [here](https://youtu.be/NljNioZ1FOk)!

1. [About this project and me](#about-this-project-and-me)
2. [What V2 does better than V1](#v2-vs-v1)
3. [What is Osu!](#what-is-osu)
4. [Requirements](#requirements)
5. [How to use](#how-to-use)
6. [Osu! Lazer support](#lazer-support)

# About this project and me <h1>
This bot is _actually_ what I intended to make when I was getting into coding (5-7 years ago), and the result was the mess seen in the first version.
This new version shows my progression not just as a developer, but as a person overall, since it neede patience, research and persistence that I did not have back then

# V2 vs V1 <h1>
Here's a list of what this version does better than the first:
1. It automatically loads the map currently in play. No need to manually load the right file browsing through Osu!'s folder. That was a pretty annoying step.
2. The bot doesn't just teleport from one circle to another anymore, it actually moves smoothly from one object to the other, making it much more enhoyable to watch.
    - I didn't implement it in the first version of the bot because I was having issues with the bot getting delayed in relation to the gameplay.
    - Initally I thought the only way to make the bot move smoothly without suffering from delay would be by reading the game's memory. Fortunately, I proved myself wrong.
    - I fixed it by giving literally every single point the bot moves a time value, which the bot keeps track of and only moves when the time is right.
    - This involves some complicated maths around Bezier curves and trigonometry.
3. The sliders are actually precise now.
    - The previous version used some spaghetti code for calculating slider paths, which resulted in inconsistent speed whilst going through sliders, causing misses.
    - Now, the bot makes sures every point in a slider path is equidistant, with a much more readable code as well.
4. Stacking actually works.
    - Stacking is whenever to objects are really close to each other in a small time frame, putting the slightly to the right or left, up or down, depending on some conditions.
    - This caused the previous version to complete miss entire streams of stacked objects (Like in `Everything Will Freeze [Time Freeze]`)
    - Also, this specific step had many edge cases and was overall a pain to do. Shout out to (idMysteries)[https://github.com/idMysteries/osuAutoBot/blob/fe45335697bc5200163be162c39ba595868b7c1b/main.cpp#L502].
5. It uses Shift as a modifier for the commands. No more accidentally turning mods on and off while typing the name of the map you want it to play.

# What is "Osu!"? <h1>
Check it out [here](https://osu.ppy.sh/home)! It's awesome!

_**TL;DR:**_
Osu! is a rhythm game where your objective is to click circles, sliders, and spinners to the beat of the song at the most precise timing possible.
The "beatmaps" are what players play. They are made by the community itself so the replayability is infinite!

# Requirements <h1>
- Python 3
- Windows

Yeah, that's it. This bot only using built-in Python libraries :)

# How to use <h1>
1. Be on Windows;
2. Have Python 3 installed;
3. Run `main.py`;
4. Follow the instructions given by the program.

P.S.: This bot doesn't use memory reading (mostly because it is a pain to do), so you need to manually start the bot by pressing Shift+P (be sure to be really precise with that first circle), and Shift+D/Shift+H/Shift+R/Shift+E for Double Time/Half Time/Hard Rock/Easy mod respectively.

# Lazer support <h1>
This bot works by reading the `.osu` beatmap files. Lazer does not have those.

However, it still kind of works if you have both Lazer and Standard downloaded, as well as the beatmap you want to play downloaded on both versions.

Native Lazer support is possible but that would require unhashing Lazer beatmap files, which is not something I am particularly interested right now.
