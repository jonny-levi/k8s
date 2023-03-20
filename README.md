# k8s cluster deployment

*************************
Creating virtual machines  
*************************

1. Download Ubuntu iso and create at least 3 virtual-machines.
2. Assign 3 different IP address for each vm.
3. Name the vm machines accordingly (ansible, worker-node-xxxx, master-node-xxxx)

*************************   
Installing Ansible server
*************************

1. sudo apt update
2. sudo apt install ansible

*************************   
Downloading the repo to Ansible server    
*************************

1. git clone https://github.com/jonny-levi/k8s.git


*************************
Initialize K8s cluster
*************************

1. Fullfil the hosts.yaml in the k8s directory.

