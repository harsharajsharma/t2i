# Python Program Setup

This Python program can be run directly or within a Docker container.

## Run it Directly:

1. Copy this repo/folder to your Local Machine, which already has Python installed.
2. Edit the path of the Access log in line 10 of the `stats.py` file.
3. Go to Terminal and run the following command:
    ```bash
    python3 stats.py
    ```
4. Open any browser and go to [http://localhost:8080/stats](http://localhost:8080/stats).

## Run in Docker Container:

1. Copy this folder to your Local Machine, which has Python3 installed and Docker daemon running.
2. Open Terminal and enter the following commands:

    ```bash
    cd T2I
    docker build -t log-stats-server .  # Building the Docker Image
    docker run -d -p 8080:8080 -v /path/to/logs:/app -e LOG_FILE_PATH=/app/access.log log-stats-server  # Run the Docker Container
    ```
3. Open any browser and go to [http://localhost:8080/stats](http://localhost:8080/stats).
This will render your content properly with syntax highlighting for the terminal commands and proper link formatting.








