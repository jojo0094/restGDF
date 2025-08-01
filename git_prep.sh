#!/bin/bash
eval "$(ssh-agent -s)"
ssh-add /home/codespace/.ssh/mpdc3
git remote set-url origin git@github.com:jojo0094/restGDF.git
git config --global user.name "jojo0094"
git config --global user.email "aungkyawkyaw0094@gmail.com"


