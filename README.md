# Car Spec Database

The purpose of this project is to collect data and connect it in a way that makes sense to people who are car enthusiasts, car builders, mechanics, etc.

Initial Make/Model/Trim data was scraped using: github.com/sampsn/car-model-dropdown-scraper

#### To install and run: 

``` zsh
git clone github.com/sampsn/personal-backend-project
```

then run create a new virtual environment and install dependencies


``` zsh
python -m venv .venv
```
``` zsh
source .venv/bin/activate
```
``` zsh
pip install -r requirements.txt
```

Then run the uvicorn/fastapi server to access the project

``` zsh
uvicorn main:app --reload
```

then go to this url: 

http://127.0.0.1:8000/docs


