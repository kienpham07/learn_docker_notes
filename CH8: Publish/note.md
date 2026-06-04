 # Docker Publishing & Versioning Study Guide

This comprehensive guide covers the essentials of publishing Docker images, managing versions with tags, and understanding modern deployment pipelines.

-----

## Lecture 1: Publishing to Docker Hub

Docker Hub is the industry-standard cloud service for storing and sharing Docker images. These services are technically referred to as **registries**.

### Core Concepts

  * **Registries**: Cloud platforms that host Docker images. Besides Docker Hub, other popular options include AWS ECR, GCP Artifact Registry, and GitHub Container Registry.
  * **Namespaces**: On Docker Hub, images are organized into namespaces (usually your username), which contain various **repositories**.
  * **Repositories**: A collection of different versions (tags) of the same image.

### Syntax & Examples

**Standard Publishing Workflow:**

1.  **Cross-Compile (for Go)**: Ensure the binary is compatible with the Linux environment inside the container.
    ``` bash
    GOOS=linux GOARCH=amd64 go build
    
    ```
2.  **Build with Namespace**: Tag the image with your Docker Hub username.
    ``` bash
    docker build . -t USERNAME/goserver
    
    ```
3.  **Push to Registry**: Upload the image to the cloud.
    ``` bash
    docker push USERNAME/goserver
    
    ```

### Deep Explanation: Layer-by-Layer Uploads

When you run `docker push`, Docker doesn't upload the image as one giant file. Instead, it uploads it **layer by layer**.

  * **Layer IDs**: The alphanumeric strings (e.g., `386f8636676a`) are cryptographic hashes (SHA-256) representing unique layers.
  * **Caching Superpower**: If you only change your application code, Docker recognizes that the base OS layers already exist in the registry. It will skip those and only upload the new, tiny layer containing your updated code.

### Key Takeaways

  * Docker Hub repositories contain different **tags** of the same image.
  * `docker push` uploads images incrementally, saving bandwidth through layer caching.

-----

## Lecture 2: Mastering Image Tags

Tags are labels assigned to specific versions of an image. They act like "sticky notes" that point to a specific snapshot of your code.

### Core Concepts

  * **Semantic Versioning (SemVer)**: A strict `MAJOR.MINOR.PATCH` format used to communicate the nature of changes.
      * **MAJOR**: Breaking changes.
      * **MINOR**: New backward-compatible features.
      * **PATCH**: Backward-compatible bug fixes.
  * **The "latest" Tag**: A default convention. It is **not** an automated feature that always points to the newest code; it is simply a label that must be manually updated.

### Syntax & Examples

**Industry Best Practice: Double-Tagging**
Instead of building twice, you can apply multiple tags to a single build:

``` bash
# Tagging a specific version and updating 'latest' simultaneously
docker build -t USERNAME/goserver:0.2.0 -t USERNAME/goserver:latest .

# Pushing all tags at once
docker push USERNAME/goserver --all-tags

```

### Deep Explanation: Simple vs. Shared Tags

  * **Simple Tags**: Points to a specific build for a fixed OS/Architecture (e.g., `2.11.3-alpine`). Used in **Production** for 100% control and stability.
  * **Shared Tags (Manifest Lists)**: A single name (e.g., `latest` or `2.11.3`) that points to multiple simple tags. Docker automatically pulls the version that matches your machine's architecture (Mac M1 vs. Windows Intel). Used in **Local Development** for convenience.

### Common Mistakes

  * **The "latest" Lie**: Assuming `latest` always means the newest version. If you build version `0.1.0` then `0.2.0` without explicitly moving the `latest` tag, `latest` will still point to `0.1.0`.
  * **Russian Roulette**: Using `latest` in production. If a buggy update is pushed to `latest`, your servers may automatically pull it and crash. Use specific semantic tags (e.g., `my-app:1.3.2`) for production stability.

-----

## Lecture 3: The Deployment Pipeline

Docker is a critical component of the modern Software Development Lifecycle (SDLC).

### Core Concepts

  * **Continuous Integration/Deployment (CI/CD)**: Automated scripts (like GitHub Actions) that build, test, and push images upon code merges.
  * **Orchestration**: Tools like **Kubernetes (K8s)** or Docker Swarm that manage running containers, pulling new images, and swapping old versions for new ones without downtime.

### The Standard Deployment Process

1.  **Develop & Commit**: Code is written and pushed to a branch.
2.  **Review & Merge**: Team members approve and merge code to the main branch.
3.  **Automated Build**: A script compiles the code and builds a new Docker image.
4.  **Push to Registry**: The new versioned image is pushed to Docker Hub or ECR.
5.  **Pull & Update**: The production server (K8s) pulls the new image and replaces old containers.

### Summary Notes

While Docker is used industry-wide, the specific tools (GitHub vs. GitLab, Docker Hub vs. ECR) vary by company. The fundamental logic remains: code -\> image -\> registry -\> production.

-----

## Final Docker Publishing Cheat Sheet

| Command                       | Purpose                                             |
| :---------------------------- | :-------------------------------------------------- |
| `docker login`                | Sign in to your registry account.                   |
| `docker build -t NAME:TAG .`  | Build an image with a specific version tag.         |
| `docker push NAME:TAG`        | Upload a specific version to the registry.          |
| `docker push NAME --all-tags` | Shortcut to upload all local tags for a repository. |
| `docker pull NAME:TAG`        | Download a specific version from the registry.      |
| `docker image rm NAME`        | Remove a local copy of an image.                    |

**Pro Tip**: When your Docker build seems "stuck" on old code despite saves, use `go build -o goserver` to ensure your binary is explicitly overwritten before the Docker COPY command runs.
