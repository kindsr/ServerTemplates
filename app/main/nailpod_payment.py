# file name : nailpod_payment.py
# pwd : /testMariaDB/app/main/nailpod_payment.py

from flask import Blueprint, Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from datetime import datetime

from app.module import dbModule

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


class CreatePaymentInfo(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('o_result', type=int)
            parser.add_argument('o_msg', type=str)
            parser.add_argument('p_machine_id', type=int)
            parser.add_argument('p_price', type=str)
            parser.add_argument('p_approval_no', type=str)
            parser.add_argument('p_card_owner', type=str)
            parser.add_argument('p_card_type', type=str)
            parser.add_argument('p_card_comp', type=str)
            parser.add_argument('p_payment_dt', type=str)
            parser.add_argument('p_error_cd', type=str)
            parser.add_argument('p_error_msg', type=str)
            args = parser.parse_args()

            _result = args['o_result']
            _msg = args['o_msg']
            _machine_id = args['p_machine_id']
            _price = args['p_price']
            _approval_no = args['p_approval_no']
            _card_owner = args['p_card_owner']
            _card_type = args['p_card_type']
            _card_comp = args['p_card_comp']
            _payment_dt = args['p_payment_dt']
            _error_cd = args['p_error_cd']
            _error_msg = args['p_error_msg']

            db_class = dbModule.Database()
            data = db_class.executeSp('sp_insert_payment_info', (_result, _msg, _machine_id, _price,
                                                                 _approval_no, _card_owner, _card_type, _card_comp,
                                                                 _payment_dt, _error_cd, _error_msg))
            print(data)

            if data[0]['O_RESULT'] is 0:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}
            else:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}

        except Exception as e:
            return {'o_result': 99, 'o_msg': str(e)}


class UpdateCancelPayment(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('o_result', type=int)
            parser.add_argument('o_msg', type=str)
            parser.add_argument('p_machine_id', type=int)
            parser.add_argument('p_approval_no', type=str)
            parser.add_argument('p_price', type=str)
            parser.add_argument('p_payment_dt', type=str)
            parser.add_argument('p_cancel_approval_no', type=str)
            args = parser.parse_args()

            _result = args['o_result']
            _msg = args['o_msg']
            _machine_id = args['p_machine_id']
            _approval_no = args['p_approval_no']
            _price = args['p_price']
            _payment_dt = args['p_payment_dt']
            _cancel_approval_no = args['p_cancel_approval_no']

            db_class = dbModule.Database()
            data = db_class.executeSp('sp_update_cancel_payment', (_result, _msg, _machine_id, _approval_no,
                                                               _price, _payment_dt, _cancel_approval_no))
            print(data)

            if data[0]['O_RESULT'] is 0:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}
            else:
                return {'o_result': str(data[0]['O_RESULT']), 'o_msg': str(data[0]['O_MESSAGE'])}

        except Exception as e:
            return {'o_result': 99, 'o_msg': str(e)}