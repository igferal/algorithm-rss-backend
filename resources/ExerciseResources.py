import datetime
import traceback
import random
from exercises.knap_sack import Item, knapsack_resolver
from flask_restful import Resource, reqparse
from models.exercise import Exercise
from models.resolution import Resolution
from models.user import UserModel
from flask_jwt_extended import (jwt_required,
                                get_jwt_identity, )


class InitExerciseResolution(Resource):
    @jwt_required
    def put(self):

        parser = reqparse.RequestParser()
        parser.add_argument('exercise_id', help='Send Exerccise id', required=True)
        parser.add_argument('difficulty', help='Send difficulty', required=False)
        data = parser.parse_args()
        exercise = Exercise.find_by_id(data["exercise_id"])
        current_user = get_jwt_identity()

        user = UserModel.find_by_username(current_user)

        new_resolution = Resolution(
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now(),
            ended=False,
            difficulty=data["difficulty"],
            final_time=0,
            user_id=user.id,
            exercise_id=exercise.id
        )
        new_resolution.save_to_db()

        try:
            return {'resolution': Resolution.to_json(new_resolution)}
        except:
            traceback.print_exc()
            return {'message': 'Error sending request'}


class EndResolution(Resource):
    @jwt_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('resolution_id', help='Send resolution id', required=True)
        data = parser.parse_args()

        try:
            resolution = Resolution.end_resolution(data["resolution_id"])
            if resolution is not False:
                return {'resolution': Resolution.to_json(resolution)}
            else:
                return {'resolution': False}
        except:
            traceback.print_exc()
            return {'message': 'Error sending request'}


class GetMyResolutions(Resource):
    @jwt_required
    def get(self):
        try:
            current_user = get_jwt_identity()
            exercises_list = Exercise.return_all()["exercises"]
            user = UserModel.find_by_username(current_user)
            return {"resolutions": Resolution.get_all_my_resolutions(user.id, exercises_list)}
        except:
            traceback.print_exc()
            return {'Token': False}


class GetBestResolutionsByExercise(Resource):
    @jwt_required
    def get(self, exercise_id):
        try:
            return {"resolutions": Resolution.get_best_times_at_exercise(exercise_id)}

        except:
            traceback.print_exc()
            return {'Token': False}


class GetAllExercises(Resource):
    @jwt_required
    def get(self):
        try:
            return Exercise.return_all()
        except:
            return {'Token': False}


class SendKnapsackExercise(Resource):
    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('difficulty', type=bool, help='please send exercise difficulty', required=True)
        isInHardMode = parser.parse_args()["difficulty"]

        if isInHardMode:
            limit = random.randint(7, 8)
        else:
            limit = random.randint(4, 5)

        items = []
        icons = ["\uf083", "\uf1ec", "\uf219", "\uf0f5", "\uf000", "\uf06b", "\uf254", "\uf076", "\uf10b"]

        for i in range(limit):
            items.append({
                "icon": random.choice(icons),
                "benefit": random.randint(2, 16),
                "weight": random.randint(1, 18)
            })
        return {'items': items, "bagSize": random.randint(limit * 5, limit * 8)}

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('resolution', help='resolution', required=True, action='append')
        parser.add_argument('elements', help='resolution', required=True, action='append')
        parser.add_argument('bagWeight', help='resolution', required=True)
        parser.add_argument('resolution_id', help='Send resolution id', required=True)

        data = parser.parse_args()

        resolution = data["resolution"]
        elements = data["elements"],
        bag_weight = int(data["bagWeight"])

        items_resolution = []
        elements_resolution = []
        resolution_benefit = 0

        for res in resolution:
            values = res.replace("}", "").split(",")
            items_resolution.append(
                Item(values[0].split(":")[1], int(values[1].split(":")[1]), int(values[2].split(":")[1])))
            resolution_benefit += int(values[2].split(":")[1])

        for res in elements[0]:
            values = res.replace("}", "").split(",")
            elements_resolution.append(
                Item(values[0].split(":")[1], int(values[1].split(":")[1]), int(values[2].split(":")[1])))

        max_sum = knapsack_resolver(0, bag_weight, elements_resolution)

        resolution = Resolution.end_resolution(data["resolution_id"], bag_weight - resolution_benefit)
        if resolution is not False:
            return {'resolution': Resolution.to_json(resolution), "resolution_value": int(max_sum)}
        else:
            return {'resolution': False}


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
