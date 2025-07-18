Welcome to my Reddit Scraper!
_(its not the best, **YET**)_

This project is a really simple project with three docker instances: MongoDB, Explorer and Processor. Explorer finds the links needed and Processor pulls the .json versions. However, you need to apply these three steps to get going.

1. Setting up the docker-compose.yml

This project uses docker to run a mongodb instance _(please make sure you installed docker beforehand)_. So you should set its username and password from the docker-compose.yml by editing the lines **9 and 10** like so:

MONGO_INITDB_ROOT_USERNAME: uname_for_mongo #<-- 9th line
MONGO_INITDB_ROOT_PASSWORD: pass_for_mongo #<-- 10th line

2. Setting the .env file

Add them to the .env file you will create like in the example below, without changing the last two lines:

MONGO_USERNAME=admin
MONGO_PASSWORD=password
MONGO_HOST=mongodb
MONGO_PORT=27017

3. You're good to go!

You just need to hit these two commands to get going:

docker-compose up -d --build
python main.py

4. Happy Scraping!

You are now scraping the happy, dark world of reddit (≧◡≦)! Have fun!

WARNING! This project is still under development, so watch your steps, and make some feedback people!
Thank you!
