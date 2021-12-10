<p align="center">
    <img alt="Logo" src="static/sherlock-icon-13.jpg" width="100" />
</p>
<h1 align="center">
    Sherlock
</h1>
<p align="center">
    An aplication to sanitize and filter ids available from customers in CSV files.
</p>

### Prerequisities
You should have installed [Docker](https://docs.docker.com/get-docker/).

### Installing
```
git clone git@github.com:GuiSAlmeida/sherlock.git
cd sherlock/
```

### Start App (without Docker)
You should have installed [Python](https://www.python.org/about/gettingstarted/) as well.  

Config `.env.example` file with values and save as `.env` only:
```sh
PLAT_USER=<user>
PLAT_PASSWORD=<password>
```
Run following commands to start application:
```sh
# install requirements
pip install -r requirements.txt

# up app at http://localhost:5000/
python main.py
```

### Usage with Docker
```sh
# Create an image from project.
docker build -t <yourname>/sherlock[:tag] .

# List images
docker images

# List layers from image
docker image history <yourname>/sherlock:<tag>

# Run container with your own plat credencials,
# if you create a .env file with your credencials skip this step.
docker run -v $(pwd):/app \
-p 5000:5000 \
-e PLAT_USER='<yourUser>' \
-e PLAT_PASSWORD='<yourPass>' \
--name sherlock <yourname>/sherlock:<tag>

# Run container in http://localhost:5000/
docker container run -p 5000:5000 <yourname>/sherlock:<tag>

# Run container with volume mapped to your local repository
docker container run -v $(pwd):/app -p 5000:5000 <yourname>/sherlock:<tag>
```