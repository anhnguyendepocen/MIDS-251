#!/bin/bash
# First remove the ips from our known hosts in case we get these again in the future
masterip=`slcli vs list | grep master | awk '{print $3}'`
slave1ip=`slcli vs list | grep slave1 | awk '{print $3}'`
slave2ip=`slcli vs list | grep slave2 | awk '{print $3}'`

# Then cancel the vms
masterid=`slcli vs list | grep master | awk '{print $1}'`
slave1id=`slcli vs list | grep slave1 | awk '{print $1}'`
slave2id=`slcli vs list | grep slave2 | awk '{print $1}'`

ssh-keygen -f "/Users/rcordell/.ssh/known_hosts" -R $masterid
ssh-keygen -f "/Users/rcordell/.ssh/known_hosts" -R $slave1id
ssh-keygen -f "/Users/rcordell/.ssh/known_hosts" -R $slave2id

slcli -y vs cancel $masterid
slcli -y vs cancel $slave1id
slcli -y vs cancel $slave2id
