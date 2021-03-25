# file name : __init__.py
# pwd : /Test/app/__init__.py

from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.debug = True
api = Api(app)

# 추가할 모듈이 있다면 추가
# config 파일이 있다면 추가

# 앞으로 새로운 폴더를 만들어서 파일을 추가할 예정임
# from app.main.[파일 이름] --> app 폴더 아래에 main 폴더 아래에 [파일 이름].py 를 import 한 것임

# 위에서 추가한 파일을 연동해주는 역할
# app.register_blueprint(추가한 파일)

# 파일 이름이 index.py 이므로
from app.main.index import main as main
from app.main.test import test as test
from app.main.nailpod import UpsertMonitoringInfo
from app.main.nailpod_payment import CreatePaymentInfo
from app.main.nailpod import CreateErrorInfo
from app.main.nailpod import SelectMaster
from app.main.nailpod import SelectPayment
from app.main.nailpod import SelectErrorInfo
from app.main.nailpod import CreatePrintInfo
from app.main.nailpod import SelectMonitoringInfo
from app.main.nailpod_payment import UpdateCancelPayment
from app.main.nailpod_update import SelectAppVersion
from app.main.nailpod_update import SelectUpdateProcess
from app.main.nailpod_update import DeleteUpdateProcess
from app.main.nailpod_update import SelectDeleteContents
from app.main.nailpod_update import UpdateUpdateYN
from app.main.nailpod_update import UpsertUpdateContents
from app.main.nailpod_update import UpdateDelYN
from app.main.nailpod_update import UpdateAppVersion
from app.main.nailpod import UpdateMachineStatus

# 위에서 추가한 파일을 연동해주는 역할
app.register_blueprint(main)  # as main으로 설정해주었으므로
app.register_blueprint(test)  # as main으로 설정해주었으므로
# app.register_blueprint(nailpod)  # as main으로 설정해주었으므로

api.add_resource(UpsertMonitoringInfo, '/nailpod/upsertMonitoringInfo')
api.add_resource(CreatePaymentInfo, '/nailpod/createPaymentInfo')
api.add_resource(CreateErrorInfo, '/nailpod/createErrorInfo')
api.add_resource(SelectMaster, '/nailpod/selectMaster')
api.add_resource(SelectPayment, '/nailpod/selectPayment/<int:machine_id>')
api.add_resource(SelectErrorInfo, '/nailpod/selectErrorInfo/<int:machine_id>')
api.add_resource(CreatePrintInfo, '/nailpod/createPrintInfo')
api.add_resource(SelectMonitoringInfo, '/nailpod/selectMonitoringInfo/<int:machine_id>')
api.add_resource(UpdateCancelPayment, '/nailpod/updateCancelPayment')
api.add_resource(SelectAppVersion, '/nailpod/selectAppVersion')
api.add_resource(SelectUpdateProcess, '/nailpod/selectUpdateProcess')
api.add_resource(DeleteUpdateProcess, '/nailpod/deleteUpdateProcess')
api.add_resource(SelectDeleteContents, '/nailpod/selectDeleteContents/<string:version>')
api.add_resource(UpdateUpdateYN, '/nailpod/updateUpdateYN/<string:update_yn>/<string:machine_id>')
api.add_resource(UpsertUpdateContents, '/nailpod/upsertUpdateContents')
api.add_resource(UpdateDelYN, '/nailpod/updateDelYN')
api.add_resource(UpdateAppVersion, '/nailpod/updateAppVersion/<string:version>')
api.add_resource(UpdateMachineStatus, '/nailpod/updateMachineStatus/<int:machine_id>/<string:status>')
