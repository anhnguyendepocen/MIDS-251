#!/bin/bash
echo Installing Kafka on IP: $1
ansible-playbook -i "$1," install-kafka.yml
