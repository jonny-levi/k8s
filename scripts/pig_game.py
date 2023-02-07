import subprocess

try:
    subprocess.run(["kubectl delete -f ../k8s/pigGame/pig_game_deploy.yaml"])
except:
    subprocess.run(["kubectl create -f ../k8s/pigGame/pig_game_deploy.yaml"])
      

try:
    subprocess.run(["kubectl delete -f ../k8s/pigGame/pig_game_service.yaml"])
except:
    subprocess.run(["kubectl create -f ../k8s/pigGame/pig_game_service.yaml"]) 