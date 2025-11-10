# Simple scraper

This is the repository for simple e-commerce portal web scraping to extract product information.

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
```

## Design

The overall architecture relies on two main components: the product model and the product handler, where the business logic is encapsulated to process given webpages and extract relevant information, the model maps this information between the transient dataclass and the persisted entity on the database.

For each target webpage received by the application entry point, a handler is created and process the basic metadata (product name, price, brand, etc.) and handles the iteractive process required to access shipping providers available, it's important to notice that while the application in it's current form is not able to handle generic e-commerce portals, it can be extended to process particular portals by abstracting ProductHandler and adjusting the workflow to portals of interest in extended classes, for example, by implementing specific `get_basic_metadata` and `get_shipping_suppliers`.

One relevatn point in this discussion is that, when extending the project to support more data sources, portals with different currency format (use of '.' instead of ',' for decimals may need adusting) and while a somewhat "generic" handler can be structured, each source might have varying degrees of complexity to retrieve similar data.

## Follow-ups

- Ship application in container;
- Skip products already processed or schedule;
- More fields extracted;
- Abstraction of ProductHandler to support more data sources;
- Handle different locale sources gracefully;
- Optimize shipping supplier extraction;
- Parallelize scraping;
