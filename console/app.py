from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
from fabric.api import *

application = Flask(__name__)

client = MongoClient('localhost:27017')
db = client.ProjectileData

print "Initialized"

@application.route("/addProjectile",methods=['POST'])
def addProjectile():
    print "Add Projectile"
    try:
        json_data = request.json['info']
        objectName = json_data['objectname']
        altitude = json_data['altitude']
        rightascension = json_data['rightascension']
        inclination = json_data['inclination']
        anomaly = json_data['anomaly']

        db.Projectiles.insert_one({
            'objectname':objectName,'altitude':altitude,'inclination':inclination,'rightascension':rightascension,'anomaly':anomaly
            })
        return jsonify(status='OK',message='inserted successfully')

    except Exception,e:
        return jsonify(status='ERROR',message=str(e))

@application.route('/')
def showProjectileList():
    return render_template('list.html')

@application.route('/getProjectile',methods=['POST'])
def getProjectile():
    print "Get projectile"
    try:
        projectileId = request.json['id']
        projectile = db.Projectiles.find_one({'_id':ObjectId(projectileId)})
        projectileDetail = {
                'objectname':projectile['objectname'],
                'altitude':projectile['altitude'],
                'inclination':projectile['inclination'],
                'rightascension':projectile['rightascension'],
                'anomaly':projectile['anomaly'],
                'id':str(projectile['_id'])
                }
        return json.dumps(projectileDetail)
    except Exception, e:
        return str(e)

@application.route('/updateProjectile',methods=['POST'])
def updateProjectile():
    print "Update projectile"
    try:
        projectileInfo = request.json['info']
        projectileId = projectileInfo['id']
        objectname = projectileInfo['objectname']
        altitude = projectileInfo['altitude']
        inclination = projectileInfo['inclination']
        rightascension = projectileInfo['rightascension']
        anomaly = projectileInfo['anomaly']

        db.Projectiles.update_one({'_id':ObjectId(projectileId)},{'$set':{'objectname':objectname,'altitude':altitude,'inclination':inclination,'rightascension':rightascension,'anomaly':anomaly}})
        return jsonify(status='OK',message='updated successfully')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@application.route("/getProjectileList",methods=['POST'])
def getProjectileList():
    print "Get projectile List"
    try:
        projectiles = db.Projectiles.find()
        print "Get Projectile List 2"
        projectileList = []
        for projectile in projectiles:
            print "For loop"
            projectileItem = {
                    'objectname':projectile['objectname'],
                    'altitude':projectile['altitude'],
                    'inclination':projectile['inclination'],
                    'rightascension':projectile['rightascension'],
                    'anomaly':projectile['anomaly'],
                    'id': str(projectile['_id'])
                    }
            print (projectileItem)
            projectileList.append(projectileItem)
    except Exception,e:
        return str(e)
    return json.dumps(projectileList)

@application.route("/execute",methods=['POST'])
def execute():
    print "Execute command"
    try:
        projectileInfo = request.json['info']
        altitude = projectileInfo['altitude']
        inclination = projectileInfo['inclination']
        rightascension = projectileInfo['rightascension']
        anomaly = projectileInfo['anomaly']
        isRoot = projectileInfo['isRoot']
        print "Execute command 2"
        env.host_string = username + '@' + ip
        env.password = password
        resp = ''
        with settings(warn_only=True):
            if isRoot:
                resp = sudo(command)
            else:
                resp = run(command)

        return jsonify(status='OK',message=resp)
    except Exception, e:
        print 'Error is ' + str(e)
        return jsonify(status='ERROR',message=str(e))

@application.route("/deleteProjectile",methods=['POST'])
def deleteProjectile():
    print "Delete projectile"
    try:
        projectileId = request.json['id']
        db.Projectiles.remove({'_id':ObjectId(projectileId)})
        return jsonify(status='OK',message='deletion successful')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

if __name__ == "__main__":
    application.run(host='0.0.0.0')

