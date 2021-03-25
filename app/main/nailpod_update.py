# file name : nailpod_update.py
# pwd : /nailpod/app/main/nailpod_update.py

from flask import Blueprint, Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from datetime import datetime
import json

from app.module import dbModule


resource_appversion_fields = {
    'version': fields.String
}

resource_update_process_fields = {
    'machine_id': fields.Integer,
    'seq': fields.Integer,
    'file_name': fields.String,
    'file_type': fields.String,
    'last_upd_dt': fields.DateTime,
    'version_info': fields.String,
    'reg_dt': fields.DateTime
}


class SelectAppVersion(Resource):
    @marshal_with(resource_appversion_fields)
    def get(self):
        db_class = dbModule.Database()
        data = db_class.executeOne('''
        select * from AppVersion
        ''')
        return data

    @marshal_with(resource_appversion_fields)
    def post(self):
        db_class = dbModule.Database()
        data = db_class.executeOne('''
        select * from AppVersion
        ''')
        return data


class UpdateAppVersion(Resource):
    def get(self, version):
        db_class = dbModule.Database()
        db_class.execute('''
        update AppVersion set version = %s
        ''' % version)
        db_class.commit()

    def post(self, version):
        db_class = dbModule.Database()
        db_class.execute('''
        update AppVersion set version = %s
        ''' % version)
        db_class.commit()


class SelectDeleteContents(Resource):
    @marshal_with(resource_update_process_fields)
    def get(self, version):
        db_class = dbModule.Database()
        data = db_class.executeAll('''
        select 0 as machine_id, seq, file_name, file_type, last_upd_dt, version_info, reg_dt from update_contents where del_yn = "Y" and CAST(SUBSTRING_INDEX(version_info, ".",-1) AS INT) >= CAST(SUBSTRING_INDEX("%s", ".",-1) AS INT)
        ''' % version)
        return data

    @marshal_with(resource_update_process_fields)
    def post(self, version):
        db_class = dbModule.Database()
        data = db_class.executeAll('''
        select 0 as machine_id, seq, file_name, file_type, last_upd_dt, version_info, reg_dt from update_contents where del_yn = "Y" and CAST(SUBSTRING_INDEX(version_info, ".",-1) AS INT) >= CAST(SUBSTRING_INDEX("%s", ".",-1) AS INT)
        ''' % version)
        return data


class DeleteUpdateProcess(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('o_result', type=int)
            parser.add_argument('o_msg', type=str)
            parser.add_argument('p_machine_id', type=int)
            parser.add_argument('p_file_name', type=str)
            args = parser.parse_args()

            _result = args['o_result']
            _msg = args['o_msg']
            _machine_id = args['p_machine_id']
            _file_name = args['p_file_name']

            db_class = dbModule.Database()
            data = db_class.executeSp('sp_delete_update_process', (_result, _msg, _machine_id, _file_name))
            print(data)

            if data[0]['O_RESULT'] is 0:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}
            else:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}

        except Exception as e:
            return {'o_result': 99, 'o_msg': str(e)}


class SelectUpdateProcess(Resource):
    @marshal_with(resource_update_process_fields)
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('o_result', type=int)
            parser.add_argument('o_msg', type=str)
            parser.add_argument('p_machine_id', type=int)
            parser.add_argument('p_version_info', type=str)
            args = parser.parse_args()

            _result = args['o_result']
            _msg = args['o_msg']
            _machine_id = args['p_machine_id']
            _version_info = args['p_version_info']

            db_class = dbModule.Database()
            data = db_class.executeSp('sp_select_update_process', (_result, _msg, _machine_id, _version_info))
            print(data)

            if len(data) > 0:
                return data
            else:
                return [{'machine_id': -1}]

        except Exception as e:
            return {'o_result': 99, 'o_msg': str(e)}


class UpdateUpdateYN(Resource):
    def get(self, machine_id, update_yn):
        db_class = dbModule.Database()

        if float(machine_id) > -1:
            db_class.execute('''
            update master set update_yn = "%s", upd_dt = now() where machine_id = %s
            ''' % (update_yn, machine_id))
        else:
            db_class.execute('''
            update master set update_yn = "%s", upd_dt = now()
            ''' % update_yn)

        db_class.commit()

    def post(self, machine_id, update_yn):
        db_class = dbModule.Database()

        if float(machine_id) > -1:
            db_class.execute('''
            update master set update_yn = "%s", upd_dt = now() where machine_id = %s
            ''' % (update_yn, machine_id))
        else:
            db_class.execute('''
            update master set update_yn = "%s", upd_dt = now()
            ''' % update_yn)

        db_class.commit()


class UpsertUpdateContents(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('o_result', type=int)
            parser.add_argument('o_msg', type=str)
            parser.add_argument('p_file_info_list', type=str)
            parser.add_argument('p_version_info', type=str)
            args = parser.parse_args()

            _result = args['o_result']
            _msg = args['o_msg']
            _file_info_list = args['p_file_info_list']
            _version_info = args['p_version_info']

            db_class = dbModule.Database()

            json_data = json.loads(_file_info_list)

            for item in json_data:
                print(item)
                data = db_class.executeSp('sp_upsert_update_contents', (_result, _msg, item['filename'], item['type'], _version_info))

            if data[0]['O_RESULT'] is 0:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}
            else:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}

        except Exception as e:
            return {'o_result': 99, 'o_msg': str(e)}


class UpdateDelYN(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('o_result', type=int)
            parser.add_argument('o_msg', type=str)
            parser.add_argument('p_file_info_list', type=str)
            args = parser.parse_args()

            _result = args['o_result']
            _msg = args['o_msg']
            _file_info_list = args['p_file_info_list']

            db_class = dbModule.Database()

            json_data = json.loads(_file_info_list)

            for item in json_data:
                print(item)
                data = db_class.executeSp('sp_update_del_yn', (_result, _msg, item['filename'], 'Y'))

            if data[0]['O_RESULT'] is 0:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}
            else:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}

        except Exception as e:
            return {'o_result': 99, 'o_msg': str(e)}
