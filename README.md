# ***lazy-tables***

## Scripted Builder
Run `./app/scripts/image-manager.sh` to perform all the functions listed below.
 * Run with the ***--help*** flag to see available options.

---
## Setup Environment
Run from the top level directory to create image from Dockerfile. 
 * `docker build -t lazy-tables .`

Create a *named volume* to persist **.xlsx** files.
 * `docker volume create persist-xlsx`

*Remove named volume with the following command.*
 * `docker volume rm persist-xlsx`

---
### Run the ***lazy-tables*** container.
```bash
docker run -it \
    -v persist-xlsx:/usr/src \
    --name uci-tables lazy-tables
```

### Verify the **.xlsx** files were written to the *named volume*.
```bash 
docker run -it --rm \
    --volume persist-xlsx:/usr/src \
    alpine ls /usr/src/app/docs/xlsx
```

### Copy files from *named volume* to your host machine.
```bash 
HOST_SAVE_PATH='/path/to/save/files/on/host/machine'
docker run -it --rm \
    --volume logs:/logs \
    --volume $HOST_SAVE_PATH:/tmp \
    alpine cp -r /usr/src/app/docs/xlsx /tmp
```
