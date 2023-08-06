# methinks

## Features
A vain attempt to make myself a bit more organized and supervisable.

* Create a **markdown** diary entry per day.
* Entries support **TODO**s and general **note-taking** sections which track history across days.
* **Configure** your own sections - see [config](config/config.yaml) for config options.
* If remote server is installed, files can be synced across computers.

This is still work in progress: first week of trial and error started on *Sun 2020-04-26 21:53*.

## Installation

### Install with local support only (persist files in local folder)

Need to pip install as **--user** so that scripts get added to user path
```bash
pip install --user methinks
```

Install methinks [config](config/config.yaml) locally by running:
```bash
methinks-env
```
*(Optional): Modify [config](config/config.yaml) file, which has been installed under your home directory: `$HOME/.config/methinks/config.yaml`.*

Generate your first diary entry:
```bash
cd mydiaryfolder
today
```

That's you set up locally.

Use `today` whenever you want to update or view your current entry. If a previous entry is found, information will be propagated into a fresh entry for today.

### To persist files across computers, follow instructions below

#### Setup server (needs to be accessible from other machines)
```bash
git clone https://github.com/andreasgrv/methinks
python3.7 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
pip install -e .

# You'll need to setup up a postgres database to match settings below
export METHINKS_DB_PORT="5432"
export METHINKS_DB_USER="methinks"
export METHINKS_DB_NAME="methinks"

export METHINKS_DB_PASSWD="mypass"
export METHINKS_TOKEN="My server token"

cd server
./run.sh
```

#### Update client config to support sync with server

Open `$HOME/.config/methinks/config.yaml`, uncomment the remote section and adapt to your server setup carried out in the previous section.

## Todos

- [x] Add a blueprint to serve the files from a flask app
- [x] Make template configurable
- [ ] Make entries visible on my website
- [ ] Implement search functionality
