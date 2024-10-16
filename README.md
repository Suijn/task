### Contributing
There's a Makefile available with a few basic commands.

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

