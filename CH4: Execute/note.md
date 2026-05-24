# Docker: Executing Commands and Container Interaction

This guide covers how to interact with running Docker containers, use the built-in help system, and execute commands or start interactive shell sessions for debugging and administration.

-----

## Lecture 1: Navigating Docker Help

The first step in mastering Docker is knowing how to find information about its extensive command set directly from the command line.

### Core Concepts

  - **CLI Self-Documentation**: Like most professional command-line tools, Docker includes a built-in manual for every command.
  - **Command Discovery**: You can view a high-level list of all available commands to understand the scope of Docker's capabilities.

### Syntax & Examples

To view the main help menu:

``` bash
docker --help
# OR
docker help

```

### Deep Explanation

The help menu organizes commands into categories such as management commands (for images, containers, networks, and volumes) and general commands (like `run`, `build`, and `ps`).

  * **`docker build`**: Specifically used to create an image from a `Dockerfile`.
  * **`docker run`**: Creates and starts a new container from an image.
  * **`docker ps`**: Lists running containers.

### Key Takeaways

  - Use `--help` whenever you are unsure of a command's specific flags or arguments.
  - Focus on the most relevant commands (run, build, ps, exec) first before diving into advanced management.

### Summary Notes

The help menu is your primary reference for command descriptions and syntax rules within the terminal environment.

-----

## Lecture 2: Executing Commands with `docker exec`

Once a container is running, you often need to perform administrative tasks or inspect its internal state without stopping it.

### Core Concepts

  - **`docker exec`**: A tool that runs a *new* command inside an *already running* container.
  - **Runtime Interaction**: Unlike `docker run`, which starts a new environment, `exec` lets you "step inside" an active process.

### Syntax & Examples

**Basic Execution:**

``` bash
# List files inside a container
docker exec [CONTAINER_ID] ls

```

**Creating Files:**

``` bash
# Create a log file inside the container's working directory
docker exec [CONTAINER_ID] touch hacker.log

```

### Deep Explanation

**The House Analogy:**

  - **`docker run`**: Builds a brand new house and turns on the power.
  - **`docker exec`**: Walks through the front door of an existing house to check the plumbing or perform maintenance.

> **Critical Constraint:** `docker exec` only works if the container is currently running. If the container is stopped or has crashed, you cannot "exec" into it.

### Key Takeaways

  - `docker exec` is the primary tool for debugging and live administration.
  - It allows you to verify changes (like file creation) in real-time within the container's isolated filesystem.

### Common Mistakes

  - **Running `exec` on stopped containers**: This will result in an error; always check `docker ps` first to ensure the container is active.

### Summary Notes

Use `exec` to interact with the internal filesystem and processes of your active application environments.

-----

## Lecture 3: Interactive Shell Sessions

Sometimes running one-off commands isn't enough, and you need a full, interactive terminal session inside the container.

### Core Concepts

  - **Interactive Mode (`-i`)**: Keeps the standard input (STDIN) open so you can type commands.
  - **TTY Allocation (`-t`)**: Provides a pseudo-terminal interface, making the output look and feel like a standard terminal with prompts and colors.
  - **Shell Binaries**: Most containers include a basic shell like `/bin/sh` or `/bin/bash`.

### Syntax & Examples

**Starting a Live Shell:**

``` bash
docker exec -it [CONTAINER_ID] /bin/sh

```

  - `-i`: Interactive mode.
  - `-t`: Allocates a TTY.
  - `/bin/sh`: The command being "exec'd" is the shell itself.

### Deep Explanation

Combining `-i` and `-t` (often written as `-it`) tricks the container into treating your local terminal as its own. This allows you to navigate the container's directories (`cd`), edit files, or run diagnostic tools like `netstat` to see which programs are serving traffic (e.g., verifying that **nginx** is serving a webpage on port 80).

### Key Takeaways

  - Use `-it /bin/sh` to manually inspect or "hack" files inside a container (e.g., overwriting a website's `index.html`).
  - Exit the session simply by typing `exit`.


-----

## Overall Docker Interaction Cheat Sheet

| Command                        | Purpose                                                                        |
| :----------------------------- | :----------------------------------------------------------------------------- |
| `docker help`                  | View the main help menu and all available commands.                            |
| `docker [command] --help`      | Get specific help for a single command (e.g., `docker run --help`).            |
| `docker ps`                    | List all currently running containers to find IDs.                             |
| `docker exec [ID] [CMD]`       | Run a single command (like `ls` or `touch`) inside a running container.        |
| `docker exec -it [ID] /bin/sh` | Open a live, interactive terminal inside a running container.                  |
| `netstat -ltnp`                | (Inside container) Check which program is bound to which port (e.g., port 80). |
