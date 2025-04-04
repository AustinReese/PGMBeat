# PGMBeat

This repo contains sample data in the context folder in case you wanna skip to the fun part and upload that data to an LLM. Skip to the end if that's te case, otherwise the sample data will be replaced once you run the script.

First things first, you gotta play one season of PGM 3. I've only tested these scripts on one season of data, the script may fail or files may be too large if you play more than one season. It's a work in progress.

PGM3 uses Realm Databases, so you'll need to download Realm Studio to download the database. You'll also need python, I think python ships with Mac's these days but have included a link below just in case.

https://docs.realm.io/sync/realm-studio
https://www.python.org/downloads/macos/

Once you've downloaded Realm Studio, you need to locate the database. You'll need to use the terminal for this, the files are not accessible in finder. Open the termianl and run the following command:

`ls /System/Volumes/Data/Users/<YOUR_USERNAME>/Library/Containers/`

You'll see a lot of com.whatever stuff, ignore all those. My folder is named 1CFF2A8B-6102-4313-BDE3-C55D6FD2D622, yours may be exactly the same or a similar combination of letters and numbers

Once you find that, run the following command:

`cp /System/Volumes/Data/Users/<YOUR_USERNAME>/Library/Containers/<YOUR-PGM-FOLDER>/Data/Documents/*.realm ~/`

If that works you'll now have the .realm files in your home directory. Open Realm Studio -> open realm file -> select X.realm where X is the number of save you want to use

Once the file opens, select the File menu from the top -> Save data -> JSON. Save this as "3.json" in the seed_data directory of this repo

Navigate to this repo in the terminal and run `python3 parse_data.py`

If the script works, you'll find the data files in the context folder. There are many cloud LLMs that accept file uploads. I've used NotebookLLM the most because it's free, but it is for research and is not creative in the slightest. 

https://notebooklm.google.com/

There's also AnythingLLM, which accepts files & allows you to use several different providers. I haven't tried it yet, but should allow you to use more creative models.

https://anythingllm.com/




