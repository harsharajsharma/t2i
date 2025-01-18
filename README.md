This Python program can be run directly or within a Docker container.

##Run it Directly:

1) Copy this repo/folder to your Local Machine, which already has Python installed.
2) Edit the relative path of Access log in line 10 of `stats.py` file.
3) Go to Terminal and run following command
    `python3 stats.py`
4) Open any Browser and go to `http://localhost:8080/stats`

##Run in Docker Container.

1) Copy this folder to your Local Machine, which has Pyhton3 installed and Docker daemon running.
2) Open Terminal enter following commands

    `cd T2I`
    `docker build -t log-stats-server .` # Building the Docker Image
    `docker run -d -p 8080:8080 -v /path/to/logs:/app -e LOG_FILE_PATH=/app/access.log log-stats-server` #Run the Docker Container
3) Open any Browser and go to `http://localhost:8080/stats`

