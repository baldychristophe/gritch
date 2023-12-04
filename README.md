# gritch

## Installation
- Install the dependencies:
```commandline
pip install -e . -r requirements.txt
```

- For the authentication with github's API, you will need an access token 
  that can be generated [here](https://github.com/settings/tokens)

- Then declare the token as an environment variable
```commandline
export GIT_ACCESS_TOKEN=<the-token>
```

- Start the application
```commandline
gritch
```

## Ideas for improvements
- Components returning None
- Tailwind's style CSS with classes
- Passing props to child components
- Adding custom extensions to an app
- Hover don't bubble up to the parent component
- Passing arguments to an app when starting
