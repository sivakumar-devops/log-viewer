# Bold BI Log Viewer Deployment Guide

## Overview

This guide explains how to deploy a **log exploration solution** for **Bold BI** application logs using a Docker container. The container provides a simple, effective interface to visualize application logs.  

You only need to specify the **path to your Bold BI application logs** in the `docker-compose.yaml` file. Deployment and integration are quick and straightforward.

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Steps

1. **Download the `docker-compose.yaml` file**:  
   Use the following command to fetch the compose file:

   ```bash
   curl -o docker-compose.yaml https://raw.githubusercontent.com/sivakumar-devops/log-viewer/refs/heads/main/deployment/docker-compose.yaml
    ```
2. Update the logs path:
Open the docker-compose.yaml file in a text editor and set the path to your Bold BI application logs. Example:
    ```bash
    volumes:
    - /path/to/boldbi/logs:/var/www/html/storage/logs-files
    ```
3. Start the container:
Run the following command to launch the container:
    ``` bash
    docker-compose up -d
    ```
2.Access the log viewer:
Once the container is running, open your browser and navigate to:

    ```bash
    http://localhost:8080/log-viewer
    ```
