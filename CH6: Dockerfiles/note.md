# Dockerfile Development & Application Packaging Study Guide

This guide covers the essentials of creating Dockerfiles to build, package, and deploy your own applications, focusing on the differences between compiled languages like Go and interpreted languages like Python.

-----

## Lecture 1: Introduction to Dockerfiles

Docker is more than just a tool for running third-party software; it is a powerful system for building and packaging your own applications using "Infrastructure as Code" (IaC) principles.

### Core Concepts

  * **Dockerfile**: A text file containing sequential commands used to assemble a Docker image, similar to a shell script.
  * **Infrastructure as Code (IaC)**: The practice of managing and provisioning infrastructure through machine-readable definition files rather than manual configuration.
  * **Automation**: Checking a Dockerfile into source control allows for automatic, repeatable image builds, eliminating manual dependency installation.

### Syntax & Examples

**Building a "Hello World" Image**

``` dockerfile
# Use a lightweight Debian OS as the base image
FROM debian:stable-slim

# Execute the 'echo "hello world"' command when the container runs
CMD ["echo", "hello world"]

```

**Terminal Commands:**

``` bash
# Build the image and tag it as 'helloworld'
# The '.' refers to the current directory
docker build . -t helloworld:latest

```

### Key Takeaways

  * Dockerfiles run commands from top to bottom.
  * The `FROM` instruction defines your starting point (base image).
  * The `CMD` instruction defines the container's default execution.

-----

## Lecture 2: Dockerizing a Compiled Go Server

Building images for compiled languages like Go is efficient because the resulting binary is standalone and does not require the language compiler to be present in the final image.

### Core Concepts

  * **Binary Executable**: A compiled program (like `goserver`) that is ready to run on a specific Operating System.
  * **Cross-Compilation**: Building a binary on one architecture (e.g., Mac/Windows) to run on another (e.g., Linux).

### Syntax & Examples

**The Go Server Dockerfile**

``` dockerfile
# 1. Start with a base OS
FROM debian:stable-slim

# 2. Copy the compiled binary from your computer into the image
# Format: COPY <source> <destination>
COPY goserver /bin/goserver

# 3. Set the default start command
CMD ["/bin/goserver"]

```

**Terminal Commands:**

``` bash
# Fix 'exec format error' by cross-compiling for Linux
GOOS=linux GOARCH=amd64 go build

# Build and run with port forwarding
docker build . -t goserver:latest
docker run -p 8010:8010 goserver

```

### Deep Explanation: COPY vs. CMD

  * **COPY (Packing)**: Think of this as packing a suitcase. You take a file from your computer (the bed) and put it into a specific pocket (path) inside the Docker image.
  * **CMD (Start Button)**: These are the instructions for a house sitter. As soon as they "walk in" (start the container), they "turn on the TV" (run the application).

### Key Takeaways

  * Go programs are easy to Dockerize because they have no runtime dependencies.
  * Use `docker run -p` to map container ports to your host machine so you can access the server in your browser.

-----

## Lecture 3: Filesystem Organization (/bin vs. /app)

While you can place files anywhere in a container, following Linux standards makes your images more professional and predictable.

### Core Concepts

  * **/bin Directory**: The standard Linux location for "Binaries" (essential executable files). It is automatically included in the system's `$PATH`.
  * **/app Directory**: A common alternative used for complex projects to keep application-specific files (templates, configs, images) isolated from system files.
  * **WORKDIR**: Sets the active directory for any following instructions (like `COPY` or `CMD`).

### Syntax & Examples

**Using a Dedicated /app Folder**

``` dockerfile
# Create and move into the /app directory
WORKDIR /app

# Copy the server into /app (implicitly uses current WORKDIR)
COPY goserver .

# Run from the /app folder
CMD ["/app/goserver"]

```

### Key Takeaways

  * If you put a binary in `/bin`, you can run it using just its name (e.g., `CMD ["goserver"]`) because it's in the system path.
  * Use `WORKDIR` to avoid cluttering system directories in multi-file projects.

-----

## Lecture 4: Environment Variables & Configuration

One of Docker's greatest strengths is the ability to ship an entire environment where configuration can be changed without rebuilding the code.

### Core Concepts

  * **ENV**: Used in a Dockerfile to set environment variables that will be available to the application at runtime.
  * **Port Configuration**: Making applications bind to a `PORT` variable instead of a hard-coded value allows for flexible deployment.

### Syntax & Examples

**Configuring the Port via ENV**

``` dockerfile
FROM debian:stable-slim
COPY goserver /bin/goserver

# Set the environment variable BEFORE the CMD
ENV PORT=8991

CMD ["/bin/goserver"]

```

### Summary Notes

Using environment variables allows the same image to be used across different environments (Development, Staging, Production) simply by changing the variable values.

-----

## Lecture 5: Dockerizing Interpreted Languages (Python)

Unlike Go, languages like Python, JavaScript, and Ruby require a runtime interpreter and dependencies to be installed inside the image.

### Core Concepts

  * **Runtime Dependencies**: The extra software (like the Python interpreter) required to read and execute script files.
  * **RUN**: A Dockerfile instruction used to execute commands *during the build process*, such as installing software.

### Syntax & Examples

**The Wrong Way (Missing Interpreter)**

``` dockerfile
FROM debian:stable-slim
COPY main.py main.py
CMD ["python", "main.py"] 
# Result: Error! 'python' is not installed in debian:stable-slim

```

**The Better Way (Using Official Images)**

``` dockerfile
# Use an image that ALREADY has Python installed
FROM python:3.9-slim

COPY main.py .
COPY books/ books/

CMD ["python", "main.py"]

```

**Install manually - instead of using FROM python:3.9-slim (Avoid it as it will take a lot of storage)**
``` dockerfile
# Use an image that DOESN'T have Python installed
# Build from a slim Debian/Linux image
FROM debian:stable-slim

# Update apt
RUN apt update
RUN apt upgrade -y

# Install build tooling
RUN apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev

# Download Python interpreter code and unpack it
RUN wget https://www.python.org/ftp/python/3.10.8/Python-3.10.8.tgz
RUN tar -xf Python-3.10.*.tgz

# Build the Python interpreter
RUN cd Python-3.10.8 && ./configure --enable-optimizations && make && make altinstall

# Copy our code into the image
COPY main.py main.py

# Copy our data dependencies
COPY books/ books/

# Run our Python script
CMD ["python3.10", "main.py"]
```

### Deep Explanation: The Standalone Machine vs. The Blueprint

  * **Go (Standalone Machine)**: The `goserver` is a fully finished machine. You just put it in the room and turn it on.
  * **Python (The Blueprint)**: `main.py` is just a text file of instructions. You need to provide a "reader" (the Python interpreter) to understand and act on those instructions.

### Common Mistakes

  * **Building for the wrong architecture**: Local Go binaries often won't run in a Linux container unless cross-compiled.
  * **Missing Runtime**: Starting from a bare-bones OS like `debian:stable-slim` for a Python app without using `RUN` to install Python.

-----

## Final Dockerfile Cheat Sheet

| Instruction | Purpose                         | Example                    |
| :---------- | :------------------------------ | :------------------------- |
| `FROM`      | Sets the Base Image             | `FROM python:3.9-slim`     |
| `WORKDIR`   | Sets the working directory      | `WORKDIR /app`             |
| `COPY`      | Copies local files to the image | `COPY src/ .`              |
| `RUN`       | Runs commands during build      | `RUN apt-get update`       |
| `ENV`       | Sets environment variables      | `ENV PORT=8080`            |
| `CMD`       | Default command when starting   | `CMD ["python", "app.py"]` |

**Key CLI Commands:**

  * **Build**: `docker build -t <name> .`
  * **Build with specific file**: \`docker build -t \<name\> -f <filename> .\`
  * **Run**: `docker run -p <host_port>:<container_port> <name>`

Would you like me to create a detailed walkthrough for setting up a multi-stage build to further optimize your Docker images?
