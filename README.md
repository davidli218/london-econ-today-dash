<h3 align="center">London Economic Today Dash</h3>
<p align="center">
    <br/>
    <a href="https://www.python.org"
    ><img
            src="https://img.shields.io/badge/Python-v3.12-blue.svg?longCache=true&logo=python&style=for-the-badge&logoColor=white&colorB=5e81ac&colorA=4c566a"
            alt="Python"
    /></a>
    <a href="https://dash.plotly.com/"
    ><img
            src="https://img.shields.io/badge/Dash-v2.17-blue.svg?longCache=true&logo=plotly&style=for-the-badge&logoColor=white&colorB=5e81ac&colorA=4c566a"
            alt="Dash"
    /></a>
    <a href="https://gunicorn.org"
    ><img
            src="https://img.shields.io/badge/Gunicorn-v21.2.0-blue.svg?longCache=true&logo=gunicorn&style=for-the-badge&logoColor=white&colorB=a3be8c&colorA=4c566a"
            alt="Gunicorn"
    /></a>
    <br/>
</p>

## Getting Started

1. Deploying the back-end API server: https://github.com/davidli218/london-econ-today-api

2. Create & Activate a virtual environment and install dependencies

   ```
   conda create -n london_eco_today_dash python=3.12
   conda activate london_eco_today_dash
   pip install -r requirements.txt
   ```

3. Modify the `app_config.toml` file

   ```toml
   api_server = "http://your_server:port"
   ```

4. Run the **development server**

   ```
   python -m app.main
   ```



## Deploying to Production

### Docker Compose

```yaml
services:

  api_server:
    container_name: london_eco_today_api
    image: "teiiri/london_eco_today_api"
    restart: always

  web:
    container_name: london_eco_today_web
    image: "teiiri/london_eco_today_dash"
    restart: always
    ports:
      - "28050:8050"
    environment:
      - BACKEND_SERVER_URL=http://api_server:8000
    depends_on:
      - api_server
```

