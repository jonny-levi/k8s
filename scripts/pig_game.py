import os

try:
    os.system("kubectl delete -f k8s/pigGame/pig_game_deploy.yaml")
    os.system("kubectl delete -f k8s/pigGame/pig_game_service.yaml")
except:
    os.system("kubectl create -f k8s/pigGame/pig_game_deploy.yaml")
    os.system("kubectl create -f k8s/pigGame/pig_game_service.yaml") 