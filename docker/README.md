# Docker

This repository was created to learn and practice docker concepts and tools.

Other useful links:

-   Docker Home: https://www.docker.com/
-   Docker Hub: https://hub.docker.com/
-   Documentation: https://docs.docker.com/.

## Dockerfile

The Dockerfile is formed by a list of commands used to specify and configure the environment for the application that will be executed.

```docker
# FROM command uses a docker image as a basis for this one
FROM python:latest

# set the working directory to /app
WORKDIR /app/

# copy the current directory contents into the container at /app/
# the ADD command can also be used for copying and it has extra features
# for caching purposes, only requirements is used in the next step
# that way, docker can reuse previous build steps
COPY ./requirements.txt ./

# install any needed packages specified in requirements.txt
RUN pip install --requirement ./requirements.txt

# copy the rest of the files
COPY ./ ./

# tell the engine port 80 is going to be used, but does not publish it
EXPOSE 80

# define environment variable
ENV NAME World !!!

# command to run when the container launches
# the ENTRYPOINT command can be used as well, be it has different semantics from CMD when starting containers
# in some cases ENTRYPOINT and CMD can be combined together to form a single command
CMD ["python", "app.py"]
```

## Image

With the Dockerfile specification, an image can be created using the command `docker image build --tag <image-name> ./`. The path at the end (`./`) indicates the context that is going to be used to create the image, where the files are going to be copied from. The dockerfile is expected to be in the same directory and be called `Dockerfile` or `dockerfile`. A dockerfile in another directory or with another name can be specified through the `--file` flag.

The image is built based on the Dockerfile specification, it already contains the application files copied by the COPY command, but it isn't running yet.

The docker images can be listed with the command `docker image ls`.

## Container

The container is a running instance of an image. To start it the following command is used:

```shell
$ # the command flags bellow can be combined into a single command
$ # publish containers port 80 into host port 4000 <host>:<container>
$ docker container run --publish 4000:80 <image-name>
...

$ # running as a detached process
$ docker container run --detach <image-name>
...

$ # running as an interactive process
$ docker container run --interactive --tty <image-name>
...

$ # giving th container a name
$ docker container run --name <container-name> <image-name>
...

$ # immediately remove the container once it stops
$ docker container run --rm <container-name> <image-name>
...
```

Running containers info can be listed with the command `docker container ls`, `docker container ls --all` can be used as well to list all running and stopped containers.

Other operations for manipulating containers:

```shell
$ # stop a running container
$ docker container stop <container-name-or-id>
...

$ # kill a running container
$ docker container skill <container-name-or-id>
...

$ # delete the container (only works if the container is stopped)
$ docker container rm <container-name-or-id>
...
```

## Sharing images

A docker image can be shared in a registry, which is a collection of repositories containing docker images. Docker already provides a cloud registry called [Docker Hub](https://hub.docker.com/), but other providers can be used as well.

Is possible to login using the docker CLI using the command

```shell
$ docker login
...
```

### Tagging images

In order to push the image to a registry (at least on Docker Hub), the image needs a tag that contains the username.

```shell
$ docker image tag <image-name> <username>/<repository>:<tag>
$ # Examples:
$ docker image tag <image-name> pedro00dk/app:latest
$ docker image tag <image-name> pedro00dk/app:1.0.0
```

### Publishing images

The app can be published with the command `docker image push <username>/<repository>:<tag>`. If the command exists successfully, the app will be available at the docker hub.

### Pulling images

Docker images can be pulled from the registry by running `docker image pull <image-name>`. If the image is already available locally, the pull command will update the image.

```shell
$ # pulling the image we just published
$ docker image pull pedro00dk/app:1.0.0
...

$ # pulling other images available in the registry
$ # note that python:latest is the same image used in the dockerfile
$ docker image pull python:latest
...

$ # these images can be executed standalone as well
$ docker container run --interactive --tty python:latest
...
```

### Docker Compose

The `docker-compose` (in newer docker version `docker compose`) is a tool for managing a set of containers at once using a configuration file. The configuration file is usually called `docker-compose.yaml` but may have other names as well.

This file can control the behavior of multiple containers (published or local), setting their images, publishing ports, volumes, setting up the network, and even limiting the memory and CPU usage.

```yml
# configuration version, newer versions have access to more features
# reference: https://docs.docker.com/compose/compose-file/
version: '3.8'

# services are the containers that are being set up
services:
    # the service name, used as container name if `container_name` is not set
    web:
        # container_name: web
        image: pedro00dk/app:latest
        ports:
            - 80:80
```
