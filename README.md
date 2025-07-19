# Reddit Scraper

Welcome to my Reddit Scraper!  
_(It’s not the best, **YET**.)_
_(also, please make sure you have a good internet connection)_

This is a simple project with three Docker containers: **MongoDB**, **Explorer**, and **Processor**.  
Explorer finds the links needed, and Processor pulls the `.json` versions.  
To get started, just follow these three steps:

---

## 1. Setting up `docker-compose.yml`

This project uses Docker to run a MongoDB instance _(please make sure Docker is installed beforehand)_  
Set its username and password by editing **lines 9 and 10** in `docker-compose.yml`, like this:

```yaml
MONGO_INITDB_ROOT_USERNAME: uname_for_mongo # <-- line 9
MONGO_INITDB_ROOT_PASSWORD: pass_for_mongo # <-- line 10
```

## 2. Setting the .env file

Edit the .env file with the same credentials.  
 Do not change the last two lines unless you absolutely know what to do:

```yaml
MONGO_USERNAME=uname_for_mongo
MONGO_PASSWORD=pass_for_mongo
MONGO_HOST=mongodb
MONGO_PORT=27017
```

## 3. You're good to go!

Run these two commands to start with gui:

```bash
docker-compose up -d --build
python main.py

```

You can also use arguments to launch without ui:

```bash
docker-compose up -d --build
python main.py {--noui [arguments: (-s or --search and -n or --number) or (-u or --url)]} or {--ui}

```

## 4. Happy Scraping! 🎉

You are now scraping the happy, dark world of Reddit (≧◡≦)! Have fun!

⚠️ Warning: This project is still under development — so watch your steps, and please send some feedback!  
Thank you!
