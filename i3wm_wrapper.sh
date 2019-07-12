#!/bin/bash

source ~/.zshrc

i3status -c /etc/i3status.conf | while :
do
    read line
    echo $line | python -u ~/git/i3status-provider/i3wm_wrapper.py || exit 1
done
