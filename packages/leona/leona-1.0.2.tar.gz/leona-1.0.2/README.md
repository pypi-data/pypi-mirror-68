![banner](https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/237/lion-face_1f981.png)

# Leona

CLI for DevOps Integration

## Install

```
$ pip install leona
```

## Initial Setup

1.- Run the command `leona`

```
$ leona
```

The first time you run the command `leona`, It will create a config file named `leona_config.yml` in your home folder.

2.- Open the config file.

```
$ code ~/leona_config.yml
```

OR

```
vi ~/leona_config.yml
```

3.- Fill in your credentials

```yaml
---
bitbucket:
  username: your_username
  password: your_password
jira:
  username: your_username
  token: your_token
teams:
  webhook: your_webhook
```

4.- You are good to go

```
$ leona

Usage: leona [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  build
  build-prod
  commitslog
  getissues
  getprojects
  jiralogs
  pr
  push
  sendmessage
  test
```
