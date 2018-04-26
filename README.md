## Fragile Families Metadata

This application provides a GUI for searching and browsing metadata on FFCWS variables.

### Installation

1. Ensure Docker is installed and running.
2. `git clone https://github.com/fragilefamilieschallenge/metadata_app.git`
3. `cd metadata_app/`
4. Ensure gui.config.cfg (private keys file) exists in current directory.
5. `docker build -t metadata_app .`
6. `docker run -p 5000:5000 metadata_app` You may need to change the second port number if you're running multiple Flask apps in Docker containers (e.g. if you're running `metadata_api` simultaneously)
