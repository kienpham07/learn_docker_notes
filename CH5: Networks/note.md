# Docker Networking & Load Balancing Study Guide

This guide covers advanced Docker networking concepts, including isolating containers for security, creating custom bridge networks, and setting up a professional-grade load-balanced architecture.

-----

## Lecture 1: Network Isolation and "Offline" Mode

While we often use Docker to expose services, sometimes the most secure configuration is to remove network access entirely.

### Core Concepts

  * **Network Isolation**: Preventing a container from communicating with any external networks or even its own internal localhost.
  * **Security Use Cases**:
      * **Untrusted Code**: Running third-party code that shouldn't have internet access.
      * **E-learning Environments**: Allowing students to execute code safely without risking the host network.
      * **Malware Auditing**: Quarantining a container suspected of having a virus to perform a safe audit.

### Syntax & Examples

To force a container into "offline" mode, use the `--network none` flag:

``` bash
# Start a container with no network access
docker run -d --network none docker/getting-started

# Verify the isolation by attempting to ping an external site
docker exec [CONTAINER_ID] ping google.com -W 2

```

  * **`-W 2`**: Sets a timeout of 2 seconds for the ping.
  * **Expected Error**: `ping: bad address` or similar, indicating no network route exists.

### Deep Explanation

Using `--network none` effectively "unplugs" the virtual ethernet cable from the container. It stops the container from connecting to the host's filesystem (via network), its own internal localhost, and all external networks.

### Key Takeaways

  * **`--network none`** is the ultimate quarantine tool for Docker containers.
  * It is essential for running high-risk or untrusted workloads securely.

-----

## Lecture 2: Custom Bridge Networks

Custom networks allow containers to communicate with each other using container names while remaining isolated from the host machine.

### Core Concepts

  * **Bridge Network**: A private network created by Docker that allows containers connected to it to communicate.
  * **Name Resolution**: Docker automatically resolves container names (e.g., `caddy1`) to their internal IP addresses for any container on the same custom network.
  * **Service Hiding**: A best practice where application servers are hidden in a private network, and only a load balancer is exposed to the public internet.

### Syntax & Examples

``` bash
# 1. Create a custom bridge network
docker network create caddytest

# 2. List networks to verify creation
docker network ls

# 3. Run a container attached to the custom network (without exposing ports)
docker run -d --name caddy1 --network caddytest -v $PWD/index1.html:/usr/share/caddy/index.html caddy

```

### Deep Explanation

In a standard backend architecture, you don't want your database or application servers directly accessible from the internet. By using a custom network and *not* using the `-p` (port mapping) flag, these containers are only reachable by other containers on the same `caddytest` network.

### Key Takeaways

  * Custom networks provide **automatic DNS** (name resolution) between containers.
  * This setup mimics real-world production environments where internal services are isolated for security.

-----

## Lecture 3: Implementing a Load Balancer

A load balancer distributes incoming network traffic across multiple backend servers to ensure no single server is overwhelmed.

### Core Concepts

  * **Load Balancer**: A central server that receives client requests and forwards them to various backend "application servers".
  * **Round Robin Strategy**: A simple balancing method where requests are routed sequentially (Server 1, then Server 2, then Server 3, then back to Server 1).
  * **Resource Optimization**: High-quality load balancers track CPU and memory usage to send traffic to the least busy server.

### Syntax & Examples

To configure **Caddy** as a load balancer, you use a `Caddyfile`:

**Caddyfile configuration:**

``` text
localhost:80
reverse_proxy caddy1:80 caddy2:80 {
    lb_policy round_robin
}

```

**Running the Load Balancer:**

``` bash
# Run the load balancer on the custom network and expose port 8880
docker run -d --network caddytest -p 8880:80 -v $PWD/Caddyfile:/etc/caddy/Caddyfile caddy

```

  * **`-p 8880:80`**: Maps the host's port 8880 to the load balancer's port 80.
  * **`-v $PWD/Caddyfile...`**: Mounts your custom configuration into the container.

### Deep Explanation

When a user hits `http://localhost:8880`, the load balancer container receives the request. It looks at its `Caddyfile` and sees it should forward traffic to `caddy1` or `caddy2`. Because all three containers are on the `caddytest` network, the load balancer can find the application servers by their names.

### Common Mistakes

  * **Forgetting the Network**: If the load balancer and application servers aren't on the *same* custom network, name resolution will fail.
  * **Port Conflicts**: Ensure port 8880 is free on your host machine before running the load balancer.

-----

## Final Docker Networking Cheat Sheet

| Command                        | Description                                                       |
| :----------------------------- | :---------------------------------------------------------------- |
| `docker network create [name]` | Creates a new custom bridge network.                              |
| `docker network ls`            | Lists all available Docker networks.                              |
| `docker run --network none`    | Runs a container with no network connectivity.                    |
| `docker run --network [name]`  | Attaches a container to a specific custom network.                |
| `docker run --name [name]`     | Assigns a name to a container for easy DNS resolution.            |
| `curl [container_name]`        | (Inside a container) Communicates with another container by name. |

**Key Takeaway**: For a secure application, hide your servers in a custom network and only use `-p` for the load balancer.
