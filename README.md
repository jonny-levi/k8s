# k8s cluster deployment

#########################   Creating virtual machines  #########################

Download Ubuntu iso and create at least 3 virtual-machines.
Assign 3 different IP address for each vm.
Name the vm machines accordingly (ansible, worker-node-xxxx, master-node-xxxx)

#########################   Installing Ansible server   #########################
sudo apt update
sudo apt install ansible

#########################   Downloading the repo to Ansible server    #########################

git clone https://github.com/jonny-levi/k8s.git


#########################
Initialize K8s cluster
#########################

Fullfil the hosts.yaml in the k8s directory.

