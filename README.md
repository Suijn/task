## Contributing
### Set up dev environment
This project uses **Poetry** for dependencies and project environment.

To set up the local environment:
1. Install poetry (https://python-poetry.org/docs/#installing-manually)
2. Refer to poetry basic usage for more instructions (https://python-poetry.org/docs/basic-usage/)

### Commands
The preferred way to run commands/interact with the app is through the **Makefile** interface. \
This reduces possible issues that you might run into while trying to do it on your own.

#### Commands: Makefile approach (preferred)

#### Run app
1. Make sure you're in the root directory.

```bash
make server
# OR
sudo make server
```

#### Run integration tests
```bash
make integration_tests
# OR
sudo make integration_tests
```

#### Check style
We use **black**, **flake8** and **isort** to keep the style consistent across the codebase.

To check the codebase for any styling issues do:
1. Set up dev environment
2. Run
    ```bash
    make style
    ```


#### Fix style
This will automatically fix styling.

1. Set up dev environment
2. Run
    ```bash
    make reformat
    ```
**Note**: flake8 issues need to be addressed manually.

#### Default Admin User
You can create an admin user with:

```bash
make admin
# OR
sudo make admin
```

This creates an admin with:
- **Admin username**: admin 
- **Admin password**: admin

#### Clean up docker containers/infra
```bash
make down
# OR
sudo make down
```
**Disclaimer**: This does **NOT** remove Postgres docker volume!\
To remove Postgres docker volume run additionally:
```bash
make down_vol
# OR
sudo make down_vol
```

#### Commands: Traditional approach
You can go the traditional way:

1. Make sure you're in the root directory.
2. Set up poetry environment.
3. Export required environment variables.
4. Run postgres (in a container)
5. Run command.

#### Django commands
```bash
python manage.py ${COMMAND}
```

#### Docker & Compose
```bash
docker ${COMMAND}
```

```bash
docker compose up --build ${TARGET} 
```

### Required environment variables
If you decide to run the app in a traditional approach, you need to make sure to set up required env variables. 

**Variables**:
- SECRET_KEY
- WORKING_MODE

**Example**:
```bash
export SECRET_KEY=top_secret
```

#### WORKING_MODE
Options: {dev}