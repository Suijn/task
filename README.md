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
Project root directory: **/task**

1. cd into the **root directory**.
2. Run command.

#### Run app
```commandline
make server
// OR
sudo make server
```

#### Run integration tests
```commandline
make integration_tests
// OR
sudo make integration_tests
```

#### Check style
We use **black**, **flake8** and **isort** to keep the style consistent across the codebase.

To check the codebase for any styling issues run:
```commandline
make style
```

#### Fix style
This will automatically fix styling.

**Note**: flake8 issues need to be addressed manually.
```commandline
make reformat
```

#### Default Admin User
You can create an admin user with:

```commandline
make admin
// OR
sudo make admin
```

This creates an admin with:
- **Admin username**: admin 
- **Admin password**: admin

#### Clean up docker containers/infra
```commandline
make down
// OR
sudo make down
```
**Disclaimer**: This does **NOT** remove Postgres docker volume!\
To remove Postgres docker volume run additionally:
```commandline
make down_vol
// OR
sudo make down_vol
```

#### Commands: Traditional approach
You can go the traditional way:

Project root directory: **/task**

1. cd into the **root directory**.
2. Set up poetry environment.
2. Run command.

#### Django commands
```commandline
python manage.py ${COMMAND}
```

#### Docker & Compose
```commandline
docker ${COMMAND}
```

```commandline
docker compose up --build ${TARGET} 
```


