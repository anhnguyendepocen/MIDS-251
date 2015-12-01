#!/bin/bash

# DO NOT SET >9 slaves
let num_slaves=8

# create the master
slcli -y vs create --datacenter=sjc03 --hostname=master --domain=w251.rlc --billing=hourly --key=rcordell --cpu=4 --memory=8192 --disk=100 --network=1000 --os=CENTOS_LATEST_64
sleep 5

# create the slaves
for (( i=1;  i<=$num_slaves; i++ ))
do
	slcli -y vs create --datacenter=sjc03 --hostname=slave${i} --domain=w251.rlc --billing=hourly --key=rcordell --cpu=4 --memory=8192 --disk=100 --network=1000 --os=CENTOS_LATEST_64
	sleep 30
done


# Wait for softlayer to issue ips to the servers we just created
sleep 300

# Grab the ip addresses
masterip=`slcli vs list | grep master | awk '{print $3}'`

SLAVES=()
for (( i=1;  i<=$num_slaves; i++ ))
do
	slaveip=`slcli vs list | grep "slave${i}" | awk '{print $3}'`
	SLAVES=("${SLAVES[@]}" $slaveip)
done

# SLAVES=($slave1ip $slave2ip $slave3ip $slave4ip $slave5ip $slave6ip $slave7ip $slave8ip $slave9ip)
ALLNODES=($masterip ${SLAVES[@]})

echo $ALLNODES
# cloud image specific configuration
user=root

# Generate ansible hosts file ##################################################
# NOTE: this works as long as there are 9 slaves or less
hostsfile=sl.hosts
echo "[master]" > $hostsfile
echo "$masterip host_alias=master" >> $hostsfile
hostnum=1
echo "[slaves]" >> $hostsfile
for slaveip in "${SLAVES[@]}"
do
  echo "$slaveip host_alias=slave$hostnum"  >> $hostsfile
  let hostnum+=1
done

ansible -i sl.hosts all -u root -m ping

# Generate an /etc/hosts file ##################################################
#moved to ansible
#etchostsfile=etc.hosts
#echo "$masterip benchmaster" > $etchostsfile
#hostnum=1
#for slaveip in "${SLAVES[@]}"
#do
#  echo "$slaveip benchslave$hostnum" >> $etchostsfile
#  let hostnum+=1
#done

# Send update to the /etc/hosts file
#for nodeip in "${ALLNODES[@]}"
#do
#  cat $etchostsfile | ssh $user@$nodeip "cat >> /etc/hosts"
#done

# Set up the hosts to be able to communicate with each other ###################
# Note: this has been moved to the ansible playbook
#keyfilename=`cat /dev/urandom | base64 | head -c 8`
#ssh-keygen -t rsa -q -f temp-$keyfilename.key -N ''
#for nodeip in "${ALLNODES[@]}"
#do
#  ssh $user@$nodeip "mkdir -p ~/.ssh"
#  cat temp-$keyfilename.key | ssh $user@$nodeip "cat > ~/.ssh/id_rsa"
#  ssh $user@$nodeip "chmod 600 ~/.ssh/id_rsa"
#  cat temp-$keyfilename.key.pub | ssh $user@$nodeip "cat >> ~/.ssh/authorized_keys"
#done
#rm temp-$keyfilename.key
#rm temp-$keyfilename.key.pub
