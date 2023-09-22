# NLP

Natural Language Interface for NM Tax Data

dataset: gross receipt taxes of NM
time period: 2009 - 2023 with a month missing in 2010 sometime

The project premise is to fine tune an open source LLM like Llama 2 with a specific dataset.
The goal is to train the model with natural language prompts in order to generate sql queries to our database.
We would set a "correct answers returned" success rate we would want to achieve (i.e. > 85%).
Essentially making an assistant for generating queries for the data.

This tool would enable users to quickly understand features of the data like revenue generation, sector performance, and broader economic patterns at both the state and local levels; potentially becoming an invaluable asset for revenue forecasting, policy formation, and economic analytics.

There could be some predictive statistics we could look into as well for a larger project scope.

# Setup

## Prequisites

Before running the database setup scripts, Docker must be installed. You can find installation instructions here: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

## Initial database setup

The first time you run the database, docker will need to download and build the images. And then the data will be loaded into the mysql image.
Use the following command to setup the database for the first run.

**_Make sure to run all commands from the repository root (/NLP)_**

#### Linux/Mac

    sudo ./scripts/linmac/db_setup.sh

#### Windows

    .\scripts\win\db_setup.bat

**_This will take a long time because flyway needs to insert over 1 million rows into the database tables_**

## Killing the database

To stop the database when you are done working, use this command.

#### Linux/Mac

    sudo ./scripts/linmac/db_kill.sh

#### Windows

    .\scripts\win\db_kill.bat

## Starting the database

After the first time setup command, you can start the database using this command. The data doesn't need to be reloaded when running this so it's much quicker.

#### Linux/Mac

    sudo ./scripts/linmac/db_start.sh

#### Windows

    .\scripts\win\db_start.bat

## Resetting the database

If something has gone wrong or you need a fresh database installation, use this to reset the docker container network and volume. Then you can run the setup command again.

#### Linux/Mac

    sudo ./scripts/linmac/db_clean.sh

#### Windows

    .\scripts\win\db_clean.bat

## Connecting to the database

Once the database has been set up and is running, you can use any tool you'd like to connect to it. If you're using VSCode, a good extension that I like to use is [MySQL by Weijan Chen](https://marketplace.visualstudio.com/items?itemName=cweijan.vscode-mysql-client2)

#### Connection info

    Host:       127.0.0.1
    Port:       3306
    Username:   bg
    Password:   bg_data
    Database:   bg_database
