# Logs Explorer using log-viewer

---

## Overview of log-viewer

**log-viewer** is an **open-source** package for Laravel that lets you easily view and search your application logs right in the browser.  

It has a clean, responsive interface and helps developers quickly find errors or debug issues without needing to open log files manually on the server.  

Key features (from the official source):  
- Beautiful, responsive UI.  
- Powerful filtering and search.  
- Automatic log file discovery.  
- Support for large log files.  
- No data sent to any third-party service.

For more details, see the official repository:  
👉 [opcodesio/log-viewer on GitHub](https://github.com/opcodesio/log-viewer)

---

## License

This application is released under the **MIT License**.  

You can read the full license text here:  
👉 [MIT License - log-viewer](https://github.com/opcodesio/log-viewer/blob/main/LICENSE.md)

---

## How to Build and Deploy this Application

This section explains how to build your own Laravel-based **log-viewer** deployment using Docker.

---

### Prerequisites

Ensure you have these installed on your system:

1. **Docker**  
   - [Official installation guide](https://docs.docker.com/get-docker/)

2. **Composer**  
   - [Official download page](https://getcomposer.org/download/)

3. **PHP**  
   - [Official Windows downloads](https://windows.php.net/download)  
   - [Official PHP site for other systems](https://www.php.net/downloads)

---

### Steps to Build and Deploy the Application

1. **Clone the custom deployment repository**  
   ```bash
   git clone https://github.com/sivakumar-devops/log-viewer
   cd log-viewer
   ```
2. Create a new Laravel project
On your host machine, run:
    ```bash
    composer create-project laravel/laravel my-log-viewer-app
    cd my-log-viewer-app
    ```
3. Install the log-viewer package
    ```bash
    composer require opcodesio/log-viewer
    ```
4. Copy the docker folder, Dockerfile, and docker-compose.yaml from the cloned repository (step 1) into your new Laravel project (my-log-viewer-app).

5. Generate the application key
    ```bash
    php artisan key:generate --show
    ```
6. Copy the generated key and update it in the .env file or docker-compose.yaml as needed.

7. In docker-compose.yaml, set the volume path to your Bold BI application logs.
Example:
    ```bash
    volumes:
    - /path/to/boldbi/logs:/var/www/html/storage/logs-files
    ```

8. Build and run the container
    ```bash
    docker-compose up --build -d
    ```
9. To access the log viewer Open your browser and go to:

    ```bash
    http://localhost:8080/log-viewer
    ```

**Notes:**

- Ensure your logs directory has the appropriate read permissions for the container.

- To stop the container, use:
        ```bash
        docker-compose down 
        ```
- You can customize the Dockerfile and docker-compose settings as needed for your environment.

