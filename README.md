# Simple scraper

## Requirements

### Docker

Install docker by following the official documentation, for this Ubuntu is being used as a platform and and the guide can be found [here](https://docs.docker.com/engine/install/ubuntu/).

### MySQL

Install a docker container dedicated to MySQL (user:root, password:root for simplicity):

```
sudo docker run --name mysql-server -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql:9.5.0
```

### UV

If desired, the application can be ran using [UV](https://docs.astral.sh/uv/), for installing in the environment setup, run:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

And update it:
```
uv self update
```

## Running

To run the scraper with [default item]("https://www.matas.dk/urban-decay-all-nighter-vitamin-c-setting-spray-118-ml"):

```
uv run main.py
```

To scrape a specific page an url can be provided:

```
uv run main.py URL
```

To check the entries saved to the database:

```
sudo docker exec -i mysql-server mysql -uroot -ppassword  <<< "use scraper; select * from product;"
``
