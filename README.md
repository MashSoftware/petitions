# Mash Petitions
[![Build Status](https://travis-ci.org/MashSoftware/petitions.svg?branch=master)](https://travis-ci.org/MashSoftware/petitions)

## Getting Started

```
vagrant up
vagrant ssh
sudo su - postgres
createuser -d -E -i -l -P -r -s vagrant
exit
createdb
psql -c "CREATE EXTENSION postgis;"
export TWFY_API_KEY=<your_they_work_for_you_api_key>
export FLASK_APP=application/__init__.py
export FLASK_DEBUG=1
```

## Running
```
flask run
```
