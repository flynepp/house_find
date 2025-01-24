#!/bin/bash

PROJECT="home_find"

help() {
    echo "Usage: $0 [option]"
    echo "Options:"
    echo "  help            -> display this help message"
    echo "  update_pip      -> update pip requirements.txt"
    echo "  install_pip     -> install pip requirements.txt"
    echo "  migrate         -> run migrations"
    echo "  find_house      -> find houses"
    echo "  black           -> run black code formatter"
}

case "$1" in
    help)
        help
        ;;
    update_pip)
        pipreqs . --encoding=utf-8 --force
        ;;
    install_pip)
        pip install -r requirements.txt
        ;;
    migrate)
        rm -rf /$PROJECT/migrations
        python manage.py makemigrations $PROJECT
        python manage.py migrate $PROJECT zero
        python manage.py migrate $PROJECT
        ;;
    find_house)
        python manage.py find_house
        ;;
    black)
        black .
        ;;
    up)
        docker build -t $PROJECT .
        docker run -d -p 50000:80 --name $PROJECT $PROJECT
        ;;
    down)
        docker stop $PROJECT
        docker rm $PROJECT
        ;;
    *)
        help
        ;;
esac
