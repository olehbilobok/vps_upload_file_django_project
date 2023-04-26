# vps_upload_file_django_project

There is the system with three servers (USA, Europe, Asia). The application allows to insert the link on the file and this file will be uploaded to the nearest server. 

As soon as file uploaded the celery task starts replication to other two servers using paramiko. User can download this file from the nearest server to local computer.

Info about uploads, downloads and replications store into postgres db, which is configured on each server.

Each user by visiting the website will be redirected to the nearest server and will be able to interact with website's features.

The project dockerized and consists with four services:  django, postgres, celery, redis. 




## Features

- upload file
- file replication to other servers using paramiko
- display information about uploads, replications and downloads
- download file


## Links

Website is accessible from following urls

For redirecting to the appropriate server can be used vpn

 - [Europe Server](http://64.226.75.193:8000)
 - [USA Server](http://68.183.108.154:8000)
 - [Asia Server](http://157.245.200.109:8000)




## Installation

Server preparation

```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo apt-get install git
```

Clone the project

```bash
git clone https://github.com/olehbilobok/vps_upload_file_django_project.git
```
Go to the directory with docker-compose.yml

```bash
cd vps_upload_file_django_project/upload_project

```
Change the environment variables for each server in docker-compose.yml and populate_vps_model.py. Regarding to the server location set: `EUROPE_DB_HOST`, `USA_DB_HOST` or `ASIA_DB_HOST`

Run the command to up the project 

```bash
nohup docker-compose up -d & 

```



    
## Environment Variables

All environment variables are into set_env.sh file and will be set automatically when docker-compose up.

Change the environment variables for each server in docker-compose.yml and populate_vps_model.py. Regarding to the server location set: `EUROPE_DB_HOST`, `USA_DB_HOST` or `ASIA_DB_HOST`
