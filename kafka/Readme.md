# Scripts showing how to install and use Kafka

## use
This software requires Ansible to be installed on your host system and public
key ssh root access to a Centos machine you want to install Kafka on. See the
sparkcluster directory of this repo for more information about setting those up.

After installing Ansible and provisioning a Centos system, the install script
in this directory takes one argument which is the IP address of the system you
want to install Kafka on.

    ./install.sh <ip of target>

The provision scripts will install dependencies and Kafka. Upon completion
ssh into the machine and example commands are shown in the file /root/kafkaexamples.txt
