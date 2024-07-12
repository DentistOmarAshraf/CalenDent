CALEN_STORAGE_TYPE=db CALEN_USR=calen_dev CALEN_PWD=calen_dev_pwd CALEN_DB=calen_dev_db CALEN_HOST=localhost tmux new-session -d 'gunicorn --bind 0.0.0.0:5001 api.v1.app:app'
