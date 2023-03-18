#!/bin/bash
cd /your_path/scrap_bs/manga_bot
gnome-terminal --wait --command="pip install -r requirements.txt"
gnome-terminal --wait --command="./create_config.sh"
gnome-terminal --command "python3.10 main.py"
exit 1
