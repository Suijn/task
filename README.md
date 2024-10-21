## Demo
To run a demo:
1. Install **App Requirements**
2. Proceed with **Demo Run Options**

### Demo Run Options
App demo can be run with one of these:
- GNU Make (preferred)
- Docker & Compose

#### With GNU Make (preferred)
```bash
$ make demo
```

This command starts the app server on http://0.0.0.0:8000/ \
Additionally this creates a default admin user. (for details see section: **Default Admin User**)


#### Docker & Compose
```bash
$ docker volume create dbvolume \ 
&& docker compose up --build demo -d \
&& docker exec task_demo bash -c ".venv/bin/poetry run python manage.py prefixes" \
&& docker attach task_demo
```
This command starts the app server on http://0.0.0.0:8000/

## App Requirements
**Minimal requirements**
- **Docker** (reference: https://docs.docker.com/engine/install/)
- **Docker Compose** (reference: https://docs.docker.com/compose/install/)

**Preferred requirements**
- **Docker** (reference: https://docs.docker.com/engine/install/)
- **Docker Compose** (reference: https://docs.docker.com/compose/install/)
- **GNU Make** (reference: https://www.gnu.org/software/make/manual/make.html#Introduction)

#### How to install GNU Make?
#### Linux
Options:
- Install with your package manager
- Install from source

#### Windows
One of the options is to use https://gnuwin32.sourceforge.net/packages/make.htm

#### MacOS
```bash
$ brew install make
```

## Contributing
1. Install **App Requirements**.
2. Set up dev environment

### Set up dev environment
This project uses **Poetry** for dependencies and project environment.

To set up the local environment:
1. Install poetry (https://python-poetry.org/docs/#installing-manually)
2. Refer to poetry basic usage for more instructions (https://python-poetry.org/docs/basic-usage/)
3. Install **App Requirements**

### Commands
The preferred way to run commands/interact with the app is through the **Makefile** interface. \
This reduces possible issues that you might run into while trying to do it on your own.

#### Commands: Makefile approach (preferred)

#### Run app
1. Make sure you're in the root directory.

```bash
$ make server
```

#### Run integration tests
```bash
$ make integration_tests
```

#### Check style
We use **black**, **flake8** and **isort** to keep the style consistent across the codebase.

To check the codebase for any styling issues do:
1. Set up dev environment
2. Run
    ```bash
    $ make style
    ```


#### Fix style
This will automatically fix styling.

1. Set up dev environment
2. Run
    ```bash
    $ make reformat
    ```
**Note**: flake8 issues need to be addressed manually.

#### Default Admin User
You can create an admin user with:

```bash
$ make admin
```

This creates an admin with:
- **Admin username**: admin 
- **Admin password**: admin

#### Clean up docker containers/infra
```bash
$ make down
```
**Disclaimer**: This does **NOT** remove Postgres docker volume!\
To remove Postgres docker volume run additionally:
```bash
$ make down_vol
```

#### Commands: Traditional approach
You can go the traditional way:

1. Make sure you're in the root directory. 
2. Export **Required Environment Variables**.
3. Run postgres (in a container)
4. Run command.

#### Django commands
```bash
$ python manage.py ${COMMAND}
```

#### Docker & Compose
```bash
$ docker ${COMMAND}
```

```bash
$ docker compose up --build ${TARGET} 
```

### Required Environment Variables
If you decide to run the app in a traditional approach, you need to make sure to set up required env variables. 

**Variables**:
- **SECRET_KEY**
- **WORKING_MODE**

**Example**:
```bash
$ export SECRET_KEY=top_secret
```

#### WORKING_MODE
Options: {dev}