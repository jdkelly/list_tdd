import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/jdkelly/list_tdd'


def provision():
    run('sudo apt update')
    run('sudo apt install python3.6 python3-venv')
    run('sudo apt install git')
    run('sudo apt install nginx')
    run('sudo rm /etc/nginx/sites-enabled/default')


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()
        _create_configs()
        _restart_services()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not exists('venv/bin/pip'):
        run(f'python3.6 -m venv venv')
    run('./venv/bin/python3.6 -m pip install -r requirements.txt')


def _create_or_update_dotenv():
    append('./superlists/.env', 'DEBUG=False')
    append('./superlists/.env', f'SITENAME={env.host}')
    current_contents = run('cat ./superlists/.env')
    if 'SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('superlists/.env', f'SECRET_KEY={new_secret}')
    run('sudo cp ./superlists/.env .env')


def _update_static_files():
    run('./venv/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./venv/bin/python manage.py migrate --noinput')


def _create_configs():
    run(f'cat ./deploy_tools/nginx.template.conf | sed "s/DOMAIN/{env.host}/g" | sudo tee /etc/nginx/sites-available/{env.host}')
    run(f'sudo ln -s /etc/nginx/sites-available/{env.host} /etc/nginx/sites-enabled/{env.host}')
    run(f'cat ./deploy_tools/gunicorn-systemd.template.service| sed "s/DOMAIN/{env.host}/g" | sudo tee /etc/systemd/system/gunicorn-{env.host}.service')


def _restart_services():
    run('sudo systemctl daemon-reload')
    run('sudo systemctl reload nginx')
    run(f'sudo systemctl enable gunicorn-{env.host}')
    run(f'sudo systemctl start gunicorn-{env.host}')
