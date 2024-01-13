# chalkgrades
Chalk is an online examination software that offers real-time monitoring of student's work. It's simple, easy to use, and not hard to host.

## 0.1: About

Chalk was started with one of my teachers asking me to produce a simple web application that allows real-time monitoring of exams. 

Of course, you could just walk around in the classroom, looking at one exam at a time, but that would produce some common issues, especially with the exam itself:

- it wastes paper and ink
- someone would not have a functioning pen
- someone else would have bad handwriting
- the same person would crumple the paper to unusable quality
- people would not know what format to write their name, date/time, etc. in
- it's very exhausting to look at a sheet of white paper for 40 minutes
- you might even have to collect the exams at the end of the class

Chalk attempts to fix these issues, by provding a simple and easy layout that anyone can learn, and it also totally eliminates the challenges that paper provides, such as bad handwriting. The background color is dark and free of blue color, so students don't get exhausted that easily from looking at a vivid page for extended periods of time.

## 0.2: Chalk, running locally

It is not possible to use Chalk without an internet connection, even if it's running locally. The database it's built with is Supabase's PostgreSQL, with the Python PostgREST API.

1. First, clone or download the repository, and make sure you have at least Python 3.12.0 and Git installed. You can use the command:

```
py --version
git clone github.com/pvcsoftware/chalkgrades.git
```

2. Install all the dependencies! Navigate to the directory where the code is in, and run the command below to install Flask, supabase-py, and all the other packages:

```
py -m pip install -r requirements.txt
```

3. Get a Supabase account. You can register a free plan at [supabase.com](<https://supabase.com>)

4. Copy the database settings. You can view it at db_config.sql.

5. Set up environment variables. Make a .env file in the main directory and enter these details:

```
supabase_url
supabase_key
password_salt
password_salt_2
user_key
work_key
```

The first 2 you can find in your Supabase settings, and the last 4 you can just come up yourself.

The `user_key` variable is the access key to making a user account, and the `work_key` is the value you can later give to teachers, which will be used to create classes (aka. workspaces).

6. Navigate to the src/js directory, and run the command below to set the request location to localhost:3000

```
py prod.py
```

In the CLI tool, you want to enter the string "dev" for "Development". It should return something like this:

```
Updated URLs in (file path) \chalkgrades\src\js\home.js
Updated URLs in (file path) \chalkgrades\src\js\landing.js
etc.
```

7. Finally, to start it up, go back to the directory of the project and start up the Python file `index.py`.

```
py index.py
```

Phew! That was quite a journey- hopefully it works for you as well.