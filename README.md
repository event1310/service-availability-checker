# Project Overview
CLI that allows you to check statuses of one or more websites asynchronously.\
Project made using Python and PostgreSQL.

# Functionalities
  - Checking single website status.
  - Checking multiple websites status passed to the CLI.
  - Checking multiple websites status from txt file.
  - Sending results to PostgreSQL database or displaying them in the command line.

# Running the tool
Below examples present the way of running commands with different arguments.\
To run the checker tool for a single website use *-site*:
  ```python
python runchecker.py -site google.com
```

To check multiple websites passed to CLI directly, use *-l* argument instead:
```python
python runchecker.py -l google.com http://facebook.com https://youtube.com
```

Using *-f* allows you to process multiple websites from *.txt* file
```python
python runchecker.py -f top50sites.txt
```

Adding *-db* sends the statuses of websites into our PostgreSQL database.
```python
python runchecker.py -f top50sites.txt -db
```

Will send current statuses of top 50 valid websites based on popularity into the database.


# Running the tool
Unit tests were made using pytest framework.\
Command below runs test cases and generates test report in *report.html* file:
```python
pytest runtests.py --html=report.html
```


# Setting up the PostgreSQL database
to start the database, run docker-compose.yml file located in db/ folder

