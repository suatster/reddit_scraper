# Reddit Scraper

Welcome to my Reddit Scraper!  
_(It’s not the best, **YET**.)_

This is a simple project with three Docker containers: **MongoDB**, **Explorer**, and **Processor**.  
Explorer finds the links needed, and Processor pulls the `.json` versions.  
To get started, just follow these three steps:

---

## 1. Setting up `docker-compose.yml`

This project uses Docker to run a MongoDB instance _(please make sure Docker is installed beforehand)_.  
Set its username and password by editing **lines 9 and 10** in `docker-compose.yml`, like this:

```yaml
MONGO_INITDB_ROOT_USERNAME: uname_for_mongo # <-- line 9
MONGO_INITDB_ROOT_PASSWORD: pass_for_mongo # <-- line 10
```

2. Setting the .env file  
   Create a .env file with the following content.  
   Do not change the last two lines:

```yaml
MONGO_USERNAME=admin
MONGO_PASSWORD=password
MONGO_HOST=mongodb
MONGO_PORT=27017
```

3. You're good to go!  
   Run these two commands to start:

```bash
docker-compose up -d --build
python main.py

```

4. Happy Scraping! 🎉  
   You are now scraping the happy, dark world of Reddit (≧◡≦)! Have fun!

⚠️ Warning: This project is still under development — so watch your steps, and please send some feedback!  
Thank you!
