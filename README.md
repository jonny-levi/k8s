

<h1> Hey there! I'm Jonathan 👋 </h1>
<h2> A Passionate DevOps From Israel 🇮🇳 </h2>
<img align="right" alt="GIF" src="https://camo.githubusercontent.com/61491d59e71fec5c794945fed916a4a682b6c0404fc31f30b08a0d919c558404/68747470733a2f2f696d616765732e73717561726573706163652d63646e2e636f6d2f636f6e74656e742f76312f3537363966633430316236333162616231616464623261622f313534313538303631313632342d5445363451474b524a4738535741495553374e532f6b6531375a77644742546f6464493870446d34386b506f73776c7a6a53564d4d2d53784f703743563539425a772d7a505067646e346a557756634a45315a7657515578776b6d794578676c4e714770304976544a5a616d574c49327a76595748384b332d735f3479737a63703272795449304871544f6161556f68724938504936465879386339505774426c7141566c555335697a7064634958445a71445976707252715a32395077306f2f636f64696e672d667265616b2e676966" width="500"/>
<h3> 👨🏻‍💻 About Me </h3>

- 🔭 &nbsp; I’m currently learning kubernetes for DevOps
- 🤔 &nbsp; Exploring new technologies.
- 🎓 &nbsp; Studying DevOps and programing languages.
- 💼 &nbsp; Support Engineer in NSO.
- 🌱 &nbsp; Enthusiast in DevOps and Artificial Intelligence .
- 😴 &nbsp; I belive, a perfect nap can be the ultimate solution for any stress. 

<h3>🛠 Tech Stack</h3>

- 💻 &nbsp; Python | JavaScript | JAVA | Bash  
- 🌐 &nbsp;  HTML | CSS | JavaScript 
- 🛢 &nbsp; K8s | Jenkins | Terraform | Ansible | Puppet | Chef
- 🔧 &nbsp;  Pycharm | Visual Studio code  | Git






<h3> 🤝🏻 Connect with Me </h3>

<p align="center">
&nbsp; <a href="https://twitter.com/Jonatha65071911" target="_blank" rel="noopener noreferrer"><img src="https://img.icons8.com/plasticine/100/000000/twitter.png" width="50" /></a>  
&nbsp; <a href="https://www.linkedin.com/in/jonathan-levi-101567173/" target="_blank" rel="noopener noreferrer"><img src="https://img.icons8.com/plasticine/100/000000/linkedin.png" width="50" /></a>
&nbsp; <a href="mailto:yonilevi0013@gmail.com" target="_blank" rel="noopener noreferrer"><img src="https://img.icons8.com/plasticine/100/000000/gmail.png"  width="50" /></a>
</p>








# k8s cluster deployment

*************************
Creating virtual machines  
*************************

Currently this Ansible automation is tested on Ubuntu 18.04 and Ubuntu 22.04.

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



Author: Jonathan Levi
