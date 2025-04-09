# { farm-twin } #

{ farm-twin } is a Digital Twin designed to provide a functional digital replica of an operational agricultural farm.

# Installation and Dependencies #

{ farm-twin } is built using Python 3.11. To install the required Python dependencies,  run:

```bash
pip install -r requirements.txt
```

{ farm-twin } also uses Docker containers, primarily to deploy MongoDB. We provide an example `docker-compose.yml` to assist:

```bash
docker compose -f deploy/docker-compose.yml up -d
```

This uses a set of default credentials in `deploy/.env`. Do not use this in production.

# Testing # 

{ farm-twin } includes a test suite. To ensure the digital twin is installed and running correctly, use:

```bash
pytest
```

# Getting Started #

The API utilises [FastAPI](https://fastapi.tiangolo.com/). To run, use:

```bash
fastapi run
```

By default, further API documentation can be found at: http://localhost:8000/docs.

# Versioning # 

The project uses [Semantic Versioning](https://semver.org/) across all components, including the API.

# License # 

This software is licensed under the [Foo License](http://foo.com).

# Contact #

For any questions or queries, please contact [Matt Broadbent](https://pure.sruc.ac.uk/en/persons/matt-broadbent) in the first instance.

# Development Roadmap # 

Further details on planned features within { farm-twin } can be found in the TODO.md file.

# Development Team #

+ [Mazdak Salavati](https://pure.sruc.ac.uk/en/persons/mazdak-salavati)
+ [Ross Muers](https://pure.sruc.ac.uk/en/persons/ross-muers)
+ [Matt Broadbent](https://pure.sruc.ac.uk/en/persons/matt-broadbent)

# Contributions #

We are happy to accept issues and pull requests from anybody, via our official repository.

# Acknowledgments # 

This project is possible due to funding from the UKRI [Strength in Places Fund (SIPF)](https://www.ukri.org/what-we-do/browse-our-areas-of-investment-and-support/strength-in-places-fund/) project, [Digital Dairy Chain](https://www.digitaldairychain.co.uk/). Further funding was awarded from the [Borderlands Inclusive Growth Deal](https://www.borderlandsgrowth.com/) and [South of Scotland Enterprise](https://www.southofscotlandenterprise.com/) through the Dairy Nexus project.