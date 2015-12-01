#!/bin/bash
# First remove the ips from our known hosts in case we get these again in the future
let num_slaves=8

masterip=`slcli vs list | grep master | awk '{print $3}'`
ssh-keygen -f "/Users/rcordell/.ssh/known_hosts" -R "${masterip}"

for (( i=1;  i<=$num_slaves; i++ ))
do
	slaveip=`slcli vs list | grep "slave${i}" | awk '{print $3}'`
	ssh-keygen -f "/Users/rcordell/.ssh/known_hosts" -R "${slaveip}"
done

# Then cancel the vms
masterid=`slcli vs list | grep master | awk '{print $1}'`
[[ ! -z "${masterid// }" ]] && slcli -y vs cancel "${masterid}"

for (( i=1;  i<=$num_slaves; i++ ))
do
	slaveid=`slcli vs list | grep "slave${i}" | awk '{print $1}'`
	[[ ! -z "${slaveid// }" ]] && slcli -y vs cancel "${slaveid}"
done

