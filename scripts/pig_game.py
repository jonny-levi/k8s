import os

try:
    os.system("kubectl delete -f ../pigGame/pig_game_deploy.yaml")
    os.system("kubectl delete -f ../pigGame/pig_game_service.yaml")
except:
    os.system("kubectl create -f ../pigGame/pig_game_deploy.yaml")
    os.system("kubectl create -f ../pigGame/pig_game_service.yaml") 