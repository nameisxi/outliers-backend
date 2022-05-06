# Outliers-backend

Outliers helps startups find engineering leads using openly available data from websites like Github. These leads are scored and ranked based on candidates open source work experience among other metrics.

# Requirements

Python >= 3.6

# Setup

Install dependencies:
```
> pip3 install -r requirements.txt
```

Create a .env file and add configurations to it:
```
> touch .env
```

Run Django DB migrations:
```
> python3 manage.py makemigrations
> python3 manage.py migrate
```

# Run

Run the backend in localhost:8000/:
```
> python3 manage.py runserver
```

# Testing

Run tests:
```
> python3 manage.py test
```

The command automatically generates an HTML coverage report that can be found in `cover/`
