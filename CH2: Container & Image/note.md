## Docker Fundamentals Study Guide

### Lecture 1: Introduction to Docker Architecture

Docker provides a way to run applications in isolated environments called containers. Unlike Virtual Machines (VMs), which virtualize hardware, containers virtualize at the operating system level, making them significantly more lightweight.

**Core Concepts**

  * **Containerization**: A method of OS-level virtualization used to deploy and run applications without needing an entire VM for each app.
  * **Isolation**: Each container operates in its own isolated environment and filesystem, though they share the underlying host OS.
  * **Namespaces**: The technology used by Docker to securely share resources while maintaining isolation between containers.

**Deep Explanation: Containers vs. Virtual Machines**
While VMs include a full copy of an operating system and virtual hardware, Docker containers share the host's operating system kernel. This means containers start faster and use far less memory and CPU than traditional VMs.

**Key Takeaways**

  * Containers are lightweight because they share the host OS.
  * Isolation is maintained through namespaces.

**Summary Notes**
Docker revolutionizes deployment by allowing many isolated processes to run on a single host efficiently.


-----

### Lecture 2: Images vs. Containers

Understanding the difference between an image and a container is fundamental to mastering Docker.

**Core Concepts**

  * **Image**: A read-only definition or "blueprint" of a container.
  * **Container**: A running instance of an image; a virtualized read-write environment.

**Syntax & Examples**

``` bash
# Download an image from a registry to your local machine
docker pull docker/getting-started

# List all images currently saved on your local machine
docker images

```

**Deep Explanation: The Class-Object Analogy**
A helpful way to think about this is the relationship between **classes** and **objects** in programming:

  * An **Image** is like a **Class**: It defines the properties and environment but doesn't "do" anything on its own.
  * A **Container** is like an **Instance (Object)**: It is the living, breathing execution of that class. You can create many separate containers from a single image.

**Key Takeaways**

  * Images are read-only; containers add a read-write layer on top.
  * Use `docker pull` to fetch images and `docker images` to view them.

**Summary Notes**
Images serve as the static definitions used to boot up active, running containers.


-----

### Lecture 3: Running Your First Container

The `docker run` command is the primary way to turn an image into a functioning container.

**Core Concepts**

  * **Detached Mode**: Running a container in the background so it doesn't occupy your terminal.
  * **Port Forwarding**: Mapping a port on your local machine (host) to a port inside the container.

**Syntax & Examples**

``` bash
# Standard run syntax
# docker run -d -p [hostport]:[containerport] [image_name]

# Example: Running the getting-started image
docker run -d -p 8965:80 docker/getting-started:latest

```

  * `-d`: Detached mode.
  * `-p 8965:80`: Maps your machine's port 8965 to the container's port 80.
  * `docker/getting-started:latest`: The image name and specific version (tag).

**Deep Explanation: Port Mapping**
When you see `0.0.0.0:8965->80/tcp` in your process list, it means traffic hitting your computer at port 8965 is being "forwarded" to port 80 inside the container. Since web servers conventionally use port 80, this allows you to view the containerized website at `http://localhost:8965`.

**Key Takeaways**

  * Use `docker ps` to see all currently running containers and their port mappings.
  * Detached mode (`-d`) is preferred for background services like web servers.

**Summary Notes**
Starting a container involves defining how it communicates with the outside world via ports.


-----

### Lecture 4: Managing Multiple Containers

Docker's efficiency allows you to run dozens or even hundreds of containers on a single host machine.

**Core Concepts**

  * **Scalability**: Running multiple instances of the same image to handle more load or different environments.
  * **Isolation of Processes**: Even if containers come from the same image, they remain completely separate entities.

**Syntax & Examples**
To run multiple instances of the same web server, you must use different **host ports** because two processes cannot bind to the same port on the same OS.

``` bash
docker run -d -p 8965:80 docker/getting-started
docker run -d -p 8966:80 docker/getting-started
docker run -d -p 8967:80 docker/getting-started

```

**Common Mistakes**

  * **Port Conflicts**: Attempting to run two containers using the same host port (e.g., trying to map both to `8965`) will result in an error. Note that the *container port* (80) can remain the same because each container has its own internal networking.

**Key Takeaways**

  * Containers are lightweight enough that running multiple instances is standard practice.
  * Each container is a separate instance with its own state.

**Summary Notes**
Real-world engineering involves managing "fleets" of containers, all isolated from one another while sharing host resources.


-----

### Lecture 5: Stopping Containers

Managing the lifecycle of a container includes knowing how to shut it down gracefully or forcefully.

**Core Concepts**

  * **SIGTERM**: A signal sent to a process to request a graceful shutdown, allowing it to save state or close connections.
  * **SIGKILL**: A signal that immediately terminates a process; it is forceful and should be a last resort.

**Syntax & Examples**

``` bash
# 1. List running containers to find the CONTAINER_ID
docker ps

# 2. Stop a container gracefully (Recommended)
docker stop [CONTAINER_ID]

# 3. Stop a container forcefully (Last resort)
docker kill [CONTAINER_ID]

```

**Key Takeaways**

  * Always try `docker stop` first to allow the application to exit cleanly.
  * Stopping a container makes its services (like a web server) immediately inaccessible.

**Summary Notes**
Proper container management requires identifying the container via `docker ps` before issuing stop commands.


-----

### Final Docker Cheat Sheet

| Command                          | Description                                            |
| :------------------------------- | :----------------------------------------------------- |
| `docker pull [image]`            | Downloads an image from a registry.                    |
| `docker images`                  | Lists all locally stored images.                       |
| `docker run -d -p [h]:[c] [img]` | Starts a container in detached mode with port mapping. |
| `docker ps`                      | Lists all currently running containers.                |
| `docker stop [id]`               | Gracefully stops a running container.                  |
| `docker kill [id]`               | Forcefully stops a running container.                  |

**Key Terms to Remember**

  * **Image**: The static blueprint (Read-only).
  * **Container**: The running instance (Read-write).
  * **Host Port**: The port on *your* machine.
  * **Container Port**: The port *inside* the Docker environment.
