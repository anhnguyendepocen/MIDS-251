# Hadoop and Spark Cluster Creation #

These scripts are based completely on Eric Whyne's (benchmark-tools)[https://github.com/ericwhyne/benchmark-tools] repository - thanks, Eric!

The intent is to create a cluster from a chosen hadoop and spark binary installation. In the case of W251 the SoftLayer Swift Object store requires a patch and custom build of hadoop, which is used by the Ansible playbook. More information can be found on this (blog)[https://www.ibm.com/developerworks/community/blogs/e90753c6-a6f1-4ae2-81d4-86eb33cf313c/entry/apache_spark_integrartion_with_softlayer_object_store?lang=en]. I recommend that after installation you do the simple Swift object store test at the end of the post to make sure things are working.

These scripts are a combination of bash shell scripts, SoftLayer command line, and Ansible playbooks. The intent is to create a set of machines designated as master or slave for use as a combination hadoop/spark cluster. The base configuration will create 1 master and 2 slaves, install and configure hadoop and install and configure Apache Spark.

## How to use these scripts ##
### Prerequisites ###
#### Linux or Mac OS X ####
Sorry Windows folks - these scripts as well as Ansible execute on a Linux-based OS. You'll need to use a virtual machine running Linux to use these.

#### SoftLayer CLI ####
You must have the SoftLayer command line interface installed which relies on Python 2.7. It is assumed that the `slcli` commands function correctly and have the correct API KEY configuration for your SoftLayer account.

#### Ansible ####
If you are on Mac OS X then I recommend installing Ansible via Homebrew with a simple `brew install ansible`. However, other options are available. For more installation information consult the (instructions)[http://docs.ansible.com/ansible/intro_installation.html] on the Ansible site.

### Setup ###
You'll need to edit the `hadoop-core-site.xml.template` and `spark-core-site.xml.template` files to add your SoftLayer API key and Object Store user id. Save them as `hadoop-core-site.xml` and `spark-core-site.xml` respectively.

The `softlayer-provision-and-create-ansible-hosts.sh` invokes the SoftLayer CLI to create the virtual machines. To add mode machines or change the configuration, this is where to do that. The Ansible playbook will deal with the additional nodes as long as the names are in the expected pattern (unless you're happy tinkering with the scripts and playbooks).

### Execution ###
Start with `softlayer-provision-and-create-ansible-hosts.sh`.

     ./softlayer-provision-and-create-ansible-hosts.sh

This script will provision the softlayer virtual machines and create a local file called `sl.hosts` which is used for the Ansible scripts. 

Once the machines are provisioned execute:

     ansible-playbook -i sl.hosts -u root playbook-install-hadoop-centos.yml

This will prep, install and configure the hadoop and spark instances.
A `hadoop` user is created and both hadoop and spark will run under that user. Now you can `ssh` to the `master` and start the hadoop and spark clusters, something like this:

     my-imac$ ssh root@169.45.50.123
     # su - hadoop
     $ $HADOOP_HOME/sbin/start-master.sh
     $ $SPARK_HOME/sbin/start-master.sh

This is an example - you'll need to format and start the HDFS file system, or maybe you'd like yarn as well.
