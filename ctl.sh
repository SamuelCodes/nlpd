#!/bin/bash

buildapp() {
  docker build -t samuelcodes/nlp .
}

runapp(){
  docker run --rm -it -v /Users/samc/Projects/NLP:/training-data --volumes-from nlp_data samuelcodes/nlp $1
}

create_data_container(){
  docker run -d --name nlp_data -v /mnt/pg-data:/app/data ubuntu echo "NLP Data Container"
}

case $1 in
  build)
    buildapp
    ;;
  server)
    runapp server
    ;;
  console)
    runapp console
    ;;
  bash)
    runapp bash
    ;;
  create_data_container)
    create_data_container
    ;;
  *)
    runapp $*
    ;;
  esac
