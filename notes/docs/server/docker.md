# Docker

### The "Restart" Policy (Standard)

In Docker Compose, the `restart` policy is used to define how a container should behave when it exits. However, there is a common point of confusion: **standard Docker restart policies do not have a "max retry" setting.**

The `restart: always` or `restart: on-failure` options will technically retry indefinitely. If you want to limit retries, you have to use the **Deployment** configuration (specifically designed for Docker Swarm but supported by Compose in newer versions).

These are the basic options you usually see in a `docker-compose.yml`. They do **not** support a retry limit.

* `no`: The default. Containers won't restart.
* `always`: Always restarts the container regardless of the exit code.
* `on-failure`: Restarts only if the container exits with a non-zero exit code.
* `unless-stopped`: Restarts unless the user manually stops it.

### How to set Max Retries (The "Deploy" Method)

To actually limit the number of attempts, you must use the `deploy` key. Even if you aren't using Docker Swarm, modern Docker Compose (V2) respects these settings.

```yaml
services:
	app:
		image: my-app:latest
		deploy:
			restart_policy:
				condition: on-failure
				delay: 5s
				max_attempts: 3
				window: 120s

```

#### Breakdown of Parameters:

| Parameter | Description |
| --- | --- |
| **`condition`** | When to restart (`none`, `on-failure`, or `any`). |
| **`delay`** | How long to wait between restart attempts (e.g., `5s`). |
| **`max_attempts`** | **The "Max Retry" limit.** How many times to try before giving up. |
| **`window`** | How long to wait before deciding if a restart was successful. |

---

### Important: Why `restart` and `deploy` are different

If you define both `restart: always` and a `deploy.restart_policy` in the same file, Docker Compose will prioritize the `deploy` settings.


---
