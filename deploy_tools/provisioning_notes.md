Provisioning a new site 
======================= 

## Required packages:
* nginx
* Python 3.6
* virtualenv + pip
* Git

 eg, on Ubuntu:
 
     sudo add-apt-repository ppa:deadsnakes/ppa
     sudo apt update
     sudo apt install nginx git python36 python3.6-venv
 
 ## Nginx Virtual Host config
 * see nginx.template.conf
 * replace DOMAIN with, e.g., staging.my-domain.com
 
 ## Systemd service
 * see gunicorn-systemd.template.service
 * replace DOMAIN with, e.g., staging.my-domain.com
 
 ## Folder structure:
 Assume we have a user account at /home/username
 /home/username
 └── sites
    ├── DOMAIN1
    │ ├── .env
    │ ├── db.sqlite3
    │ ├── manage.py etc
    │ ├── static
    │ └── virtualenv
    └── DOMAIN2
    ├── .env
    ├── db.sqlite3
    ├── etc 
 
 
 # Example of provisioning scripts
 cat ./deploy_tools/nginx.template.conf | sed "s/DOMAIN/lists.kelytica.com/g" | sudo tee /etc/nginx/sites-available/lists.kelytica.com
 
 sudo ln -s /etc/nginx/sites-available/lists.kelytica.com /etc/nginx/sites-enabled/lists.kelytica.com 
 
 cat ./deploy_tools/gunicorn-systemd.template.service| sed "s/DOMAIN/lists.kelytica.com/g" | sudo tee /etc/systemd/system/gunicorn-lists.kelytica.com.service 