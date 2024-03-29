# Outliers-backend

Outliers helps startups find engineering leads using openly available data from websites like Github. These leads are scored and ranked based on candidates open source work experience among other metrics.

# Requirements

- Python >= 3.9
- PostgreSQL


# Setup

1. Install dependencies:
```
> virtualenv env
> source env/bin/activate
> pip3 install -r requirements.txt
```

2. Create a .env file:
```
> touch .env
```

And add the configurations to it.

3. Run Django DB migrations:
```
> python3 manage.py migrate
```

4. Populate the database with data by visiting the /github/populate/ endpoint:<br>
[http://localhost:8000/github/populate](http://localhost:8000/github/populate)

5. Compute ranking scores for Candidate objects by visiting the /scores/compute/ endpoint:<br>
[http://localhost:8000/scores/compute/](http://localhost:8000/scores/compute/)


# Run

Run the backend in `localhost:8000/`:
```
> python3 manage.py runserver
```

# Testing

Run tests:
```
> python3 manage.py test
```

The command automatically generates an HTML coverage report that can be found in `cover/`

# Documentation

- [Architecture doc](https://github.com/nameisxi/outliers-backend/blob/main/documentation/architecture.md)
- [Testing doc](https://github.com/nameisxi/outliers-backend/blob/main/documentation/testing.md)
