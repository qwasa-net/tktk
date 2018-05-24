tea: env db demodb collectstatic run

env:
	python3 -m venv .env
	.env/bin/pip install -U -r requirements.txt

db:
	.env/bin/python pw/manage.py migrate --settings=pw.settings

demodb:
	bash tools/task-builders/build_all.sh --reset --save

collectstatic:
	.env/bin/python pw/manage.py collectstatic --clear --noinput --verbosity 2 --settings=pw.settings

run:
	.env/bin/python pw/manage.py runserver --settings=pw.settings

deploy_install:
	ANSIBLE_CONFIG=deploy/ansible/ansible.cfg ansible-playbook -v deploy/ansible/install.yml

deploy_update:
	ANSIBLE_CONFIG=deploy/ansible/ansible.cfg ansible-playbook -v deploy/ansible/install.yml --tags update
