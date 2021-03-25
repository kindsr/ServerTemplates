# file name : nailpod.py
# pwd : /testMariaDB/app/main/nailpod.py

from flask import Blueprint, Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from datetime import datetime

from app.module import dbModule


resource_fields = {
    'machine_id': fields.Integer,
    'place_id': fields.Integer,
    'mac_accr': fields.String,
    'ip_addr': fields.String,
    'card_reader_product_id': fields.String,
    'epson_printer_product_id': fields.String,
    'receipt_printer_product_id': fields.String,
    'cpu': fields.String,
    'hdd': fields.String,
    'ram': fields.String,
    'usb_yn': fields.String,
    'scanner_yn': fields.String,
    'machine_status': fields.String,
    'mf_loc': fields.String,
    'mf_dt': fields.DateTime,
    'use_yn': fields.String,
    'del_yn': fields.String,
    'reg_dt': fields.DateTime,
    'upd_dt': fields.DateTime
}

resource_payment_fields = {
    'payment_id': fields.Integer,
    'machine_id': fields.Integer,
    'price': fields.Float,
    'approval_no': fields.String,
    'card_owner': fields.String,
    'card_type': fields.String,
    'card_comp': fields.String,
    'payment_dt': fields.DateTime,
    'cancel_yn': fields.String,
    'cancel_approval_no': fields.String,
    'error_cd': fields.String,
    'error_msg': fields.String,
    'reg_dt': fields.DateTime,
    'upd_dt': fields.DateTime
}

resource_error_info_fields = {
    'machine_id': fields.Integer,
    'seq': fields.Integer,
    'error_cd': fields.String,
    'error_msg': fields.String,
    'fix_yn': fields.String,
    'reg_dt': fields.DateTime,
    'upd_dt': fields.DateTime
}

resource_print_fields = {
    'machine_id': fields.Integer,
    'seq': fields.Integer,
    'design_type': fields.Integer,
    'file_name_1': fields.String,
    'file_name_2': fields.String,
    'file_name_3': fields.String,
    'file_name_4': fields.String,
    'file_name_5': fields.String,
    'file_name_6': fields.String,
    'file_name_7': fields.String,
    'file_name_8': fields.String,
    'file_name_9': fields.String,
    'file_name_10': fields.String,
    'reg_dt': fields.DateTime,
    'upd_dt': fields.DateTime
}

resource_monitoring_fields = {
    'machine_id': fields.Integer,
    'prog_status': fields.String,
    'uv_status': fields.String,
    'ink_status': fields.String,
    'motor_status': fields.String,
    'epson_printer_status': fields.String,
    'receipt_printer_status': fields.String,
    'print_cnt': fields.Integer,
    'ink_remain_c': fields.String,
    'ink_remain_m': fields.String,
    'ink_remain_y': fields.String,
    'ink_remain_k': fields.String,
    'ink_remain_w': fields.String,
    'hdd_used': fields.String,
    'ram_used': fields.String,
    'remark': fields.String,
    'reg_dt': fields.DateTime,
    'upd_dt': fields.DateTime
}


class UpsertMonitoringInfo(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('o_result', type=int)
            parser.add_argument('o_msg', type=str)
            parser.add_argument('p_machine_id', type=int)
            args = parser.parse_args()

            _result = args['o_result']
            _msg = args['o_msg']
            _machine_id = args['p_machine_id']

            db_class = dbModule.Database()
            data = db_class.executeSp('sp_upsert_monitoring_info', (_result, _msg, _machine_id))
            print(data)

            if data[0]['O_RESULT'] is 0:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}
            else:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}

        except Exception as e:
            return {'o_result': 99, 'o_msg': str(e)}


class CreateErrorInfo(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('o_result', type=int)
            parser.add_argument('o_msg', type=str)
            parser.add_argument('p_machine_id', type=int)
            parser.add_argument('p_error_cd', type=str)
            parser.add_argument('p_error_msg', type=str)
            parser.add_argument('p_fix_yn', type=str)
            args = parser.parse_args()

            _result = args['o_result']
            _msg = args['o_msg']
            _machine_id = args['p_machine_id']
            _error_cd = args['p_error_cd']
            _error_msg = args['p_error_msg']
            _fix_yn = args['p_fix_yn']

            db_class = dbModule.Database()
            data = db_class.executeSp('sp_insert_errer_info', (_result, _msg, _machine_id, _error_cd, _error_msg,
                                                               _fix_yn))
            print(data)

            if data[0]['O_RESULT'] is 0:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}
            else:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}

        except Exception as e:
            return {'o_result': 99, 'o_msg': str(e)}


class SelectMaster(Resource):
    @marshal_with(resource_fields)
    def get(self):
        db_class = dbModule.Database()
        data = db_class.executeAll('''
        select * from master
        ''')
        return data

    @marshal_with(resource_fields)
    def post(self):
        db_class = dbModule.Database()
        data = db_class.executeAll('''
        select * from master
        ''')
        return data


class SelectPayment(Resource):
    @marshal_with(resource_payment_fields)
    def get(self, machine_id):
        db_class = dbModule.Database()
        data = db_class.executeAll('''
        select * from payment_info where machine_id = %d order by payment_id desc limit 20
        ''' % machine_id)
        return data

    @marshal_with(resource_payment_fields)
    def post(self, machine_id):
        db_class = dbModule.Database()
        data = db_class.executeAll('''
        select * from payment_info where machine_id = %d order by payment_id desc limit 20
        ''' % machine_id)
        return data


class SelectErrorInfo(Resource):
    @marshal_with(resource_error_info_fields)
    def get(self, machine_id):
        db_class = dbModule.Database()
        data = db_class.executeAll('''
        select * from error_info where machine_id = %d order by seq desc limit 20
        ''' % machine_id)
        return data

    @marshal_with(resource_error_info_fields)
    def post(self, machine_id):
        db_class = dbModule.Database()
        data = db_class.executeAll('''
        select * from error_info where machine_id = %d order by seq desc limit 20
        ''' % machine_id)
        return data


class CreatePrintInfo(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('o_result', type=int)
            parser.add_argument('o_msg', type=str)
            parser.add_argument('p_machine_id', type=int)
            parser.add_argument('p_design_type', type=int)
            parser.add_argument('p_total_print_cnt', type=int)
            parser.add_argument('p_print_cnt', type=int)
            parser.add_argument('p_print_file_name', type=str)
            parser.add_argument('p_file_name_1', type=str)
            parser.add_argument('p_file_name_2', type=str)
            parser.add_argument('p_file_name_3', type=str)
            parser.add_argument('p_file_name_4', type=str)
            parser.add_argument('p_file_name_5', type=str)
            parser.add_argument('p_file_name_6', type=str)
            parser.add_argument('p_file_name_7', type=str)
            parser.add_argument('p_file_name_8', type=str)
            parser.add_argument('p_file_name_9', type=str)
            parser.add_argument('p_file_name_10', type=str)
            args = parser.parse_args()

            _result = args['o_result']
            _msg = args['o_msg']
            _machine_id = args['p_machine_id']
            _design_type = args['p_design_type']
            _total_print_cnt = args['p_total_print_cnt']
            _print_cnt = args['p_print_cnt']
            _print_file_name = args['p_print_file_name']
            _file_name_1 = args['p_file_name_1']
            _file_name_2 = args['p_file_name_2']
            _file_name_3 = args['p_file_name_3']
            _file_name_4 = args['p_file_name_4']
            _file_name_5 = args['p_file_name_5']
            _file_name_6 = args['p_file_name_6']
            _file_name_7 = args['p_file_name_7']
            _file_name_8 = args['p_file_name_8']
            _file_name_9 = args['p_file_name_9']
            _file_name_10 = args['p_file_name_10']

            db_class = dbModule.Database()
            data = db_class.executeSp('sp_insert_print_info', (_result, _msg, _machine_id, _design_type,
                                                               _total_print_cnt, _print_cnt, _print_file_name,
                                                               _file_name_1, _file_name_2, _file_name_3, _file_name_4,
                                                               _file_name_5, _file_name_6, _file_name_7, _file_name_8,
                                                               _file_name_9, _file_name_10))
            print(data)

            if data[0]['O_RESULT'] is 0:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}
            else:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}

        except Exception as e:
            return {'o_result': 99, 'o_msg': str(e)}


class SelectMonitoringInfo(Resource):
    @marshal_with(resource_monitoring_fields)
    def get(self, machine_id):
        db_class = dbModule.Database()
        data = db_class.executeOne('''
        select * from monitoring_info where machine_id = %d
        ''' % machine_id)
        return data

    @marshal_with(resource_monitoring_fields)
    def post(self, machine_id):
        db_class = dbModule.Database()
        data = db_class.executeOne('''
        select * from monitoring_info where machine_id = %d
        ''' % machine_id)
        return data


class UpdateMachineStatus(Resource):
    def get(self, machine_id, status):
        db_class = dbModule.Database()

        db_class.execute('''
        update master set machine_status = "%s", upd_dt = now() where machine_id = %d
        ''' % (status, machine_id))

        db_class.commit()

    def post(self, machine_id, status):
        db_class = dbModule.Database()

        db_class.execute('''
        update master set machine_status = "%s", upd_dt = now() where machine_id = %d
        ''' % (status, machine_id))

        db_class.commit()