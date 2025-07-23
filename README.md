[![Dynamic DevOps Roadmap](https://img.shields.io/badge/Dynamic_DevOps_Roadmap-559e11?style=for-the-badge&logo=Vercel&logoColor=white)](https://devopsroadmap.io/getting-started/)
[![Community](https://img.shields.io/badge/Join_Community-%23FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://newsletter.devopsroadmap.io/subscribe)
[![Telegram Group](https://img.shields.io/badge/Telegram_Group-%232ca5e0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/DevOpsHive/985)
[![Fork on GitHub](https://img.shields.io/badge/Fork_On_GitHub-%2336465D?style=for-the-badge&logo=github&logoColor=white)](https://github.com/DevOpsHiveHQ/devops-hands-on-project-hivebox/fork)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com//timrob0/Handson-hivebox/badge)]([https://scorecard.dev/viewer/?uri=github.com//timrob0/Handson-hivebox](https://scorecard.dev/viewer/?uri=github.com/timrob0/Handson-hivebox))

# HiveBox - DevOps End-to-End Hands-On Project

<p align="center">
  <a href="https://devopsroadmap.io/projects/hivebox" style="display: block; padding: .5em 0; text-align: center;">
    <img alt="HiveBox - DevOps End-to-End Hands-On Project" border="0" width="90%" src="https://devopsroadmap.io/img/projects/hivebox-devops-end-to-end-project.png" />
  </a>
</p>

> [!CAUTION]
> **[Fork](https://github.com/DevOpsHiveHQ/devops-hands-on-project-hivebox/fork)** this repo, and create PRs in your fork, **NOT** in this repo!

> [!TIP]
> If you are looking for the full roadmap, including this project, go back to the [getting started](https://devopsroadmap.io/getting-started) page.

This repository is the starting point for [HiveBox](https://devopsroadmap.io/projects/hivebox/), the end-to-end hands-on project.

HiveBox project follows the same Dynamic MVP-style mindset used in the [roadmap](https://devopsroadmap.io/).

The project aims to cover the whole Software Development Life Cycle (SDLC). That means each phase will cover all aspects of DevOps, such as planning, coding, containers, testing, continuous integration, continuous delivery, infrastructure, etc.



<br/>
<p align="center">
  <a href="https://devopsroadmap.io/projects/hivebox/" imageanchor="1">
    <img src="https://img.shields.io/badge/Get_Started_Now-559e11?style=for-the-badge&logo=Vercel&logoColor=white" width="400" />
  </a><br/>
</p>

---

## Implementation

## 🚀 Phase 1 – Kickoff & Preparation
<p align="center">
  <img src="https://github.com/user-attachments/assets/2e2ca2ef-3ad7-4e74-869c-8c8949820cea" alt="phase1" width="400" />
</p>


### Kickoff

- Defined my role as part of a collaborative DevOps team (not working solo).
- Reviewed key concepts of software project management, with a focus on Agile.
- Chose **Kanban** as the preferred Agile methodology for this project.
- Committed to avoiding scope creep: *Make it work → Make it right → Make it fast*.
- Adopted a “manager of one” mindset for personal accountability and efficiency.

### Preparation

- Forked the original HiveBox repository to my GitHub account.
- Created a **GitHub Project Board** using the Kanban template to manage workflow.
- Ensured all work is submitted as pull requests — no direct pushes to `main`.
- Committed to documenting each phase clearly for future readers or collaborators.
- Selected three nearby **senseBox IDs** from [openSenseMap](https://opensensemap.org):
  - `5eba5fbad46fb8001b799786`
  - `5c21ff8f919bf8001adf2488`
  - `5ade1acf223bd80019a1011c`

## Phase 2 – Tools, Code, Containers & Testing
<p align="center">
  <img src="https://github.com/user-attachments/assets/ed7d183d-27ce-41b1-bf46-76893a700faf" alt="phase2" width="400" />
</p>


### 2.1 Tools

- Set up **Git** and **GitHub** for version control and collaboration.  
- Used **VS Code** as the primary development environment.  
- Used **Docker** to containerize the application.

### 2.2 Code

- Created a `version.txt` file containing the version string `0.0.1`.  
- Developed `main.py` with a function to read the version from `version.txt` and print it when the app runs.

```python
def main():
    version = get_app_version()
    print(f"Version: {version}")

def get_app_version() -> str:
    try:
        with open("version.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Unknown Version"
```
### 2.3 Containers

- Created a Dockerfile using the official Python 3.11 Alpine image.
- The Dockerfile sets the working directory to /app, copies main.py and version.txt into the image, and sets the entrypoint to run main.py via Python.
-	Built and ran the Docker container locally to verify it prints the correct version.

```go
FROM python:3.11-alpine

WORKDIR /app

COPY main.py .
COPY version.txt .

ENTRYPOINT ["python", "main.py"]
```
### 2.4 Testing

- To test the app, build the Docker image locally and run the container.
- When running, the container should print the version string exactly as it appears in version.txt. (Version: 0.0.1)

#### Example Commands

##### Build the Docker image and tag it as 'hivebox-app'
```console
docker build -t hivebox-app .
```

##### Run the container and see the version output
```console
docker run --rm hivebox-app
```

## Phase 3 – Laying the Base (Roadmap Module Start)
<p align="center">
  <img src="https://github.com/user-attachments/assets/38f11da8-c0ab-45c1-a809-b35f0abff99e" alt="phase3" width="400" />
</p>

This phase focused on building core app functionality, enforcing clean code practices, and setting up continuous integration for quality and reliability.

### 3.1 Tools & Setup

- Used **Hadolint** (with VS Code extension) to lint Dockerfiles.  
- Used **Pylint** (with VS Code extension) to lint Python code.  
- Adopted **Conventional Commits** for meaningful Git commit messages.  
- Explored and integrated the **openSenseMap API** for sensor data.

### 3.2 Code Implementation

Implemented FastAPI endpoints to support core functionality:

<details>
<summary>/version</summary>
<br>
  
```python
@app.get("/version")
def get_app_version() -> str:
    """
    Reads the application version from 'version.txt'.

    Returns:
        str: The version string, or 'Unknown Version' if the file is not found.
    """
    try:
        with open("version.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Unknown Version"
```
</details>

<details>
<summary>/temperature</summary>
<br>
  
```python
def extract_recent_temperature(sensor, now):
    """
    Extracts the temperature value from a sensor if the measurement is within the last hour.
    Returns the value as float or None.
    """
    if "temperatur" in sensor.get("title", "").lower():
        last = sensor.get("lastMeasurement")
        if last:
            timestamp = datetime.fromisoformat(last["createdAt"].replace("Z", "+00:00"))
            if now - timestamp <= timedelta(hours=1):
                return float(last["value"])
    return None

@app.get("/temperature")
def average_temperature():
    """
    Calculates the average temperature from a set of OpenSenseMap sensor boxes.

    Only considers temperature measurements from the last hour. If no recent data is found,
    returns a 404 error.

    Returns:
        dict: Dictionary containing the average temperature, unit, and number of sources counted.
    """
    box_ids = [
        "5ade1acf223bd80019a1011c",
        "5c21ff8f919bf8001adf2488",
        "5ade1acf223bd80019a1011c"
    ]

    temperatures = []
    now = datetime.now(timezone.utc)

    for box_id in box_ids:
        try:
            response = requests.get(f"https://api.opensensemap.org/boxes/{box_id}", timeout=10)
            response.raise_for_status()
            box = response.json()

            for sensor in box.get("sensors", []):
                temp = extract_recent_temperature(sensor, now)
                if temp is not None:
                    temperatures.append(temp)
                    break  # stop once we find the first valid temperature sensor

        except (requests.RequestException, ValueError, KeyError):
            continue  # skip any box that fails

    if not temperatures:
        raise HTTPException(status_code=404, detail="No recent temperature data found")

    avg_temp = sum(temperatures) / len(temperatures)
    return {
        "average_temperature": round(avg_temp, 2),
        "unit": "°C",
        "sources_counted": len(temperatures)
    }
```

</details>

### 3.3 Containers & Best Practices

- Lightweight base image
- defined working directory
- .dockerignore to reduce build

### 3.4 Continuous Integration

- Used GitHub Actions with pylint, hadolint, dockerbuild, pytest, and OpenSSF Scorecard.

### 3.5 Testing

- Used **pytest** and FastAPI's **TestClient** for testing.
- Verified `/version` endpoint returns the correct version or `"Unknown Version"` if `version.txt` is missing.
- Tested `extract_recent_temperature()` function to ensure it only returns temperatures within the last hour and correctly handles sensor titles.
- Mocked OpenSenseMap API responses to test `/temperature` endpoint for:
  - Correct average temperature calculation across multiple sensors.
  - Handling no recent temperature data (returns 404).
  - Partial failures in API calls without breaking the endpoint.
- Cleaned up `version.txt` after tests to maintain test isolation.
- Created a `MockResponse` class to simulate HTTP responses for reliable, controlled testing.

### 3.6 Problems faced
- Started trying to get the average of every sensor box in Opensense which crashed the program...next time I will be clearer about the requirments (You only need 3 boxes).
- Linting required a heap of docstrings to be added which I was not aware of.
- Needing to open the ports for communication with docker file and my localhost.
- Needing to add installing of packages in order to get main.py to run (import request, fastapi-cli, etc.)
- Refactoring the file structure since it was nested in other folders which was messing with linting in GitHub Actions.
- Setup OpenSSF incorrectly and had to re-read documentation.

## Module 4 - Expand - Constructing a shell (Github actions and CI)

<p align="center">
  <img src="https://github.com/user-attachments/assets/05120ba5-849a-4dc5-85a8-cdfd8af4e2df" alt="phase4" width="400" />
</p>


## **4.1 Tools**

- Installed and configured **Kind** (Kubernetes IN Docker) for local Kubernetes cluster setup.
- Installed and configured **kubectl** to manage Kubernetes resources.

## **4.2 Code Implementation**

- Developed FastAPI application with environment variable configuration for SenseBox settings.
```yaml
env: # Environment variables injected into container

- name: OPENSENSEMAP_API_URL

value: "https://api.opensensemap.org"

- name: OPENSENSEMAP_BOX_IDS

value: 5eba5fbad46fb8001b799786,5c21ff8f919bf8001adf2488,5ade1acf223bd80019a1011c

- name: VERSION_FILE

value: "v1.0.0 "
```
- _Implemented /metrics endpoint exposing default Prometheus metrics for monitoring.
configured in prometheus-deployment.yaml and below in main.py_
```yaml
@app.get("/metrics")

def metrics():

"""

Exposes Prometheus metrics.

"""

return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```
- Implemented /temperature endpoint that returns average temperature with a status field indicating:
	- **Too Cold** if average temperature < 10°C
	- **Good** if 11°C ≤ average temperature ≤ 36°C
	- **Too Hot** if average temperature > 37°C
_ - Super simple, added average calculation, added status with conditionals._

```python
avg_temp = sum(temperatures) / len(temperatures)

if avg_temp < 10:

status = "Too cold"

elif 10 < avg_temp < 36:

status = "Normal"

else:

status = "Too hot"

  

return {

"average_temperature": round(avg_temp, 2),

"unit": "°C",

"sources_counted": len(temperatures),

"status": status,

}
```
_- Wrote comprehensive integration tests for the API using pytest and FastAPI test client.
  tests in test_main.py and put into github actions._

## **4.3 Containerization and Kubernetes Manifests**

- Created KIND cluster configuration to run Kubernetes with Ingress-NGINX controller for routing.
_installed ingess-nginx onto container and mapped ports to localdevice._

- Authored Kubernetes manifests including Deployment, Service, and Ingress resources to deploy the application.
_configured in ./k8/_

## **4.4 Continuous Integration (CI)**

- Configured CI workflows to run integration tests automatically.
- _All configured in Github Actions._

- Integrated SonarQube for code quality, security, and static analysis with Quality Gate checks
- _SonarQube in Github actions._

- Added Terrascan scanning to detect Kubernetes manifest misconfigurations and vulnerabilities.
- _Terrascan seems to be unsupported. Have instead switched to Trivy._

- Applied best practices for CI including test automation and security scanning.
- _as above_

## **4.5 Continuous Delivery (CD)**

- Created GitHub Actions workflow for Continuous Delivery.
- _githubActions with pylint, hadolint, and pytest, supply-chain-scorecard,SonarQube analysis, and trivy._

- Automated release process by building and pushing versioned Docker images to GitHub Container Registry (GHCR).
- _Github aciton to auto deploy to tag :latest but if versioning tags are added it will deploy as a release._

- Enabled tagging and version management for Docker images to maintain clear versioning and rollback capability.
- _As above._
