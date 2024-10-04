# Telegram Bot Project

This project is a Telegram bot that interacts with the `memeapi` to generate memes based on user input. The bot handles commands, inline queries, and sends images to users.

## Request
    1. python 3, for example `conda create -n meme python=3.9`
    2. `pip install -r requirements`, get the dependcies for this proj
    3. get mongo db, for exampel `sudo docker run --name some-mongo -d mongo:latest`
    4. Firstly, start the memeapi, with the command `cd memeapi; python main.py`, which listen in 8000 port and nginxed with the port 443. We recommand you to confiure your own nginx config
    5. Then, start the telegram robot, with the commadn `cd imbot; python main.py`. you will get an error on the cmd, if you do not export the evn_variable API_URL(the https url of the api service started in 4) and the env_variable TOKEN(your telegram robot token)
With above configuration, you will get your own bot and enjoy. 
## Features

- **Meme Generation**: Generates memes based on user input using `memeapi`.
- **Command Handlers**: Handles `/meme`, and more commands.
- **Inline Query Support**: Allows users to generate memes via inline queries.
- **Menu Navigation**: Provides interactive menus with inline buttons.

