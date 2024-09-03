import json
from datetime import date, timedelta
 
 #this file handle working with database and funtion in this file have been imported in telegram.py

def add_user(user_id):
    f = json.load(open("database.json",'r'))
    try:
        f["users"][user_id]
    except:
        with open("database.json","w") as data:
            
            f["users"][user_id] = {"isp": 0, "isf": 4, "dates": int(str(date.today()).replace("-","")),"datee":int(str(date.today()+timedelta(days=30)).replace("-","")), "posts": []}
            json.dump(f,data)
            
def isfirsttime(user_id):
    f = json.load(open("database.json"))
    return bool(f["users"][user_id]["isf"])

def ispremium(user_id):
    f = json.load(open("database.json"))

    if bool(f["users"][user_id]["isp"]):
        if f["users"][user_id]["datee"] < int(str(date.today()).replace("-","")):
            f["users"][user_id]["isp"] = 0
            with open("database.json","w") as data:
                json.dump(f,data)
                
            return False
        else:
            return True
    return False
    
# def add_start(user_id,msg):
#     user_id = str(user_id)
#     f = json.load(open("msg.json",'r'))

#     with open("msg.json","w") as data:
            
#             f["users"][user_id] = {msg.from_user.id}
#             json.dump(f,data)
    

def add_post(user_id,p):
    user_id = str(user_id)
    f = json.load(open("database.json"))
    t = f["users"][user_id]["posts"] 
    t.append(p)
    print(t)
    f["users"][str(user_id)]["posts"] = t
    with open("database.json","w") as data:
        json.dump(f,data)
