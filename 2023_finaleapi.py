from flask import Flask, jsonify, request
from flask_restful import Resource, Api
app=Flask(__name__)
api=Api(app)

#массив групп
groups=[]

group_id_counter=1
participant_id_counter=1
class Group(Resource):
    def get(self):
        return jsonify(groups)
    def post(self):
        data=request.get_json()
        name=data['name']
        description=data.get('description')
        group={'id': group_id_counter,'name':name,'description':description, 'participants':[]}
        groups.append(group)
        group_id_counter+=1
        return jsonify({'id':group_id_counter-1}),201
class GroupDetails(Resource):
    def get(self,group_id):
        for group in groups:
            if group['id']==group_id:
                return jsonify(group)
        return {'error':'Group not found'},404
    def put(self, group_id):
        data=request.get_json()
        name=data.get('name')
        description=data.get('description')
        for group in groups:
            if group['id']==group_id:
                if name:
                    group['name']=name
                if description:
                    group['description']=description 
                    return 204
        return {'error': 'Group not found'},404
    def delete (self,group_id):
        for i,group in enumerate(groups):
            if group['id']==group_id:
                groups.pop(i)
                return 204
        return {'error':'Group not found'}, 404
class Participant(Resource):
    def post(self,group_id):
        data=request.get_json()
        name=data['name']
        wish=data['wish']
        for group in groups:
            if group['id']==group_id:
                participant={'id':participant_id_counter, 'name':name,'recipient':None}
                group['participants'].append(participant)
                participant_id_counter+=1
                return 201
        return {'error': 'Group not found'},404
api.add_resource(Group, '/group')
api.add_resource(GroupDetails,'/group/<int:group_id>')
api.add_resource(Participant,'/group/<int:group_id>/participant')
if __name__=='__main__':
    app.run(port=8080, debug=True)
    