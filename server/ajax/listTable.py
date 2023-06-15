import math

from flask import Blueprint, jsonify, request
from sqlalchemy.sql import func
# from werkzeug.security import check_password_hash
from database.tables import User, Permission, Reagent, Supplier, Department, Grid, Product
from database.tables import InTag, OutTag, Session

#from common.ma import ReagentSchema

from flask_cors import CORS

listTable = Blueprint('listTable', __name__)


# ------------------------------------------------------------------

# list user table all data
@listTable.route("/listUsers", methods=['GET'])
def list_users():
    print("listUsers....")
    s = Session()
    _user_results = []
    return_value = True
    _objects = s.query(User).all()
    users = [u.__dict__ for u in _objects]
    for user in users:
        # if (user.dep_id != None):
        dep_item = s.query(Department).filter_by(id=user['dep_id']).first()
        # if (user.perm_id != None):
        perm_item = s.query(Permission).filter_by(id=user['perm_id']).first()

        dep_name_data=''                      # 2023-04-25 add
        if dep_item is not None:              # 2023-04-25 add
          dep_name_data=dep_item.dep_name     # 2023-04-25 add

        if (user['isRemoved']):
            _user_object = {
                'emp_id': user['emp_id'],
                'emp_name': user['emp_name'],
                'emp_dep': dep_name_data,         # 2023-04-25 modify
                'emp_perm': perm_item.auth_code   # for inventory.vue
            }
            _user_results.append(_user_object)
    s.close()

    temp_len = len(_user_results)
    print("listUsers, 員工總數: ", temp_len)
    if (temp_len == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': _user_results
    })


# list reagent table all data
@listTable.route("/listReagents", methods=['GET'])
def list_reagents():
    print("listReagents....")
    s = Session()
    _results = []
    return_value = True
    _objects = s.query(Reagent).all()
    reagents = [u.__dict__ for u in _objects]
    for reagent in reagents:
        sup_item = s.query(Supplier).filter_by(id=reagent['super_id']).first()
        prc_item = s.query(Product).filter_by(id=reagent['product_id']).first()
        cat_item = s.query(Department).filter_by(
            id=reagent['catalog_id']).first()

        sup_name_data=''                      # 2023-04-25 add
        if sup_item is not None:              # 2023-04-25 add
          sup_name_data=sup_item.super_name   # 2023-04-25 add
        prc_name_data=''                      # 2023-04-25 add
        if prc_item is not None:              # 2023-04-25 add
          prc_name_data=prc_item.name         # 2023-04-25 add
        dep_name_data=''                      # 2023-04-25 add
        if cat_item is not None:              # 2023-04-25 add
          dep_name_data=cat_item.dep_name     # 2023-04-25 add

        k1 = ''
        if reagent['reag_temp'] == 0:  # 0:室溫、1:2~8度C、2:-20度C
            k1 = '室溫'
        if reagent['reag_temp'] == 1:
            k1 = '2~8度C'
        if reagent['reag_temp'] == 2:
            k1 = '-20度C'

        if (reagent['isRemoved']):
            _obj = {
                'id': reagent['id'],
                'reag_id': reagent['reag_id'],
                'reag_name': reagent['reag_name'],
                'reag_product': prc_name_data,              # 2023-04-25 modify
                'reag_In_unit': reagent['reag_In_unit'],
                'reag_Out_unit': reagent['reag_Out_unit'],
                'reag_scale': reagent['reag_scale'],
                # 'reag_period': reagent['reag_period'],    #依2022-12-12操作教育訓練建議作修正(刪除)
                'reag_stock': reagent['reag_stock'],
                'reag_temp': k1,
                'reag_catalog': dep_name_data,              # 2023-04-25 modify
                'reag_supplier': sup_name_data,             # 2023-04-25 modify
            }
            _results.append(_obj)
    s.close()

    temp_len = len(_results)
    print("listReagents, 試劑總數量: ", temp_len)
    if (temp_len == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': _results,
    })


# list department table all data
@listTable.route("/listDepartments", methods=['GET'])
def list_departments():
    print("listDepartments....")
    s = Session()
    _department_results = []
    return_value = True
    _objects = s.query(Department).all()
    departments = [u.__dict__ for u in _objects]
    for dep in departments:
        _department_object = {
            'id': dep['id'],
            'dep_name': dep['dep_name'],
        }
        _department_results.append(_department_object)

    s.close()

    temp_len = len(_department_results)
    print("listUsers, 部門總數: ", temp_len)
    if (temp_len == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': _department_results
    })


# list product table all data by object format
@listTable.route("/listProductsByObj", methods=['GET'])
def list_products_by_object():
    print("listProductsByObj....")
    s = Session()
    _product_results = []
    _objects = s.query(Product).all()
    products = [u.__dict__ for u in _objects]
    for product in products:
        _product_object = {
            'id': product['id'],
            'prd_name': product['name'],
        }
        _product_results.append(_product_object)

    s.close()

    return jsonify({
        'outputs': _product_results
    })


# list product table all data
@listTable.route("/listProducts", methods=['GET'])
def list_products():
    print("listProducts....")
    s = Session()
    _product_results = []
    _objects = s.query(Product).all()
    products = [u.__dict__ for u in _objects]
    for product in products:
        _product_results.append(product['name'])
    s.close()

    return jsonify({
        'outputs': _product_results
    })


# list permission table all data
@listTable.route("/listPermissions", methods=['GET'])
def list_permissions():
    print("listPermissions....")
    s = Session()
    _results = []
    _objects = s.query(User).all()
    users = [u.__dict__ for u in _objects]
    for user in users:
        dep_item = s.query(Department).filter_by(id=user['dep_id']).first()

        perm_item = s.query(Permission).filter_by(id=user['perm_id']).first()
        k1 = False
        k2 = False
        k3 = False
        # print("permission: ", perm_item.auth_code)
        if perm_item.auth_code == 1:  # 0:none, 1:system, 2:admin, 3:member
            k1 = True
        if perm_item.auth_code == 2:
            k2 = True
        if perm_item.auth_code == 3:
            k3 = True
        # print("permission: ", k1, k2, k3)
        if (user['isRemoved']):
            _obj = {
                'perm_empID': user['emp_id'],
                'perm_empName': user['emp_name'],
                'perm_empDep': dep_item.dep_name,
                'perm_checkboxForSystem': k1,
                'perm_checkboxForAdmin': k2,
                'perm_checkboxForMember': k3,
                # 'emp_perm': perm_item.auth_code  # 0:none, 1:system, 2:admin, 3:member
            }
            _results.append(_obj)
    s.close()

    return jsonify({
        'status': 'success',
        'outputs': _results
    })


# list grid table all data
@listTable.route("/listGrids", methods=['GET'])
def list_grids():
    print("listGrids....")
    s = Session()
    _results = []
    _objects = s.query(Grid).all()
    # grids = [u.__dict__ for u in _objects]
    for grid in _objects:
        # if (grid.isRemoved):
        for reagent in grid._reagents_on_grid:
            _obj = {
                'id': reagent.id,

                'grid_reagID': reagent.reag_id,
                'grid_reagName': reagent.reag_name,
                'grid_station': grid.station,
                'grid_layout': grid.layout,
                'grid_pos': grid.pos,
                'grid_id': grid.id,
                'seg_id': grid.seg_id,
                'range0': grid.range0,
                'range1': grid.range1,
            }
            _results.append(_obj)

    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })


# list grid table all data for 入庫
@listTable.route("/listStockInGrids", methods=['GET'])
def list_stockin_grids():
    print("listStockInGrids....")
    s = Session()
    _results = []
    _objects = s.query(Grid).all()

    for grid in _objects:
        # if (grid.isRemoved):
        for reagent in grid._reagents_on_grid:
            _obj = {
                'grid_reagID': reagent.reag_id,
                'grid_reagName': reagent.reag_name,
                'grid_station': grid.station,
                'grid_layout': grid.layout,
                'grid_pos': grid.pos,
                'id': grid.id,
                'seg_id': grid.seg_id,
                'range0': grid.range0,
                'range1': grid.range1,
            }
            _results.append(_obj)

    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })


# list grid table all data for 入庫
@listTable.route("/listStockOutGrids", methods=['GET'])
def list_stockout_grids():
    print("listStockOutGrids....")
    s = Session()
    _results = []
    _objects = s.query(Grid).all()

    for grid in _objects:
        # if (grid.isRemoved):
        for reagent in grid._reagents_on_grid:
            _obj = {
                'grid_reagID': reagent.reag_id,
                'grid_reagName': reagent.reag_name,
                'grid_station': grid.station,
                'grid_layout': grid.layout,
                'grid_pos': grid.pos,
                'id': grid.id,
                'seg_id': grid.seg_id,
                'range0': grid.range0,
                'range1': grid.range1,
            }
            _results.append(_obj)

    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })


# list grid table for Led
@listTable.route("/listGridsForLed", methods=['GET'])
def list_grids_for_led():
    print("listGridsForLed....")
    s = Session()
    _results = []
    _objects = s.query(Grid).all()
    # grids = [u.__dict__ for u in _objects]
    for grid in _objects:
        # if (grid.isRemoved):
        # for reagent in grid._reagents_on_grid:
        _obj = {
            # 'grid_reagID': reagent.reag_id,
            # 'grid_reagName': reagent.reag_name,
            'grid_station': grid.station,
            'grid_layout': grid.layout,
            # 'grid_pos': grid.pos,
            'seg_id': grid.seg_id,
            'range0': grid.range0,
            'range1': grid.range1,
        }
        _results.append(_obj)

    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })


# list supplier table all data
@listTable.route("/listSuppliers", methods=['GET'])
def list_suppliers():
    print("listSuppliers....")
    s = Session()
    _results = []
    _objects = s.query(Supplier).all()
    # grids = [u.__dict__ for u in _objects]
    for supplier in _objects:
        # print("supplier: ", supplier.super_name, len(supplier._products))
        if (supplier.isRemoved):
            _obj = {
                'id': supplier.id,

                'sup_id': supplier.super_id,
                'sup_name': supplier.super_name,
                'sup_address': supplier.super_address,
                'sup_contact': supplier.super_connector,
                'sup_phone': supplier.super_tel,
                'sup_products': [],
            }

            for product in supplier._products:
                # _obj['sup_products'].append(product.id)
                _obj['sup_products'].append(product.name)
                # print("supplier product: ", product.id)

            _results.append(_obj)
            # print("supplier product: ", _results)

    temp_len = len(_results)
    print("listSuppliers, input total(供應商總數): ", temp_len)
    if (temp_len == 0):
        return_value = False

    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })


# list supplier table all data
@listTable.route("/listSuppliersByProc", methods=['POST'])
def list_suppliers_by_product():
    print("listSuppliersByProc....")

    request_data = request.get_json()

    _name = request_data['prd_name']
    print("prod_name: ", _name)

    s = Session()
    _results = []

    product = s.query(Product).filter_by(name=_name).first()
    for supplier in product._suppliers:  # 列出供應商
        print("supplier: ", supplier.super_name, len(supplier._products))
        if (supplier.isRemoved):
            _results.append(supplier.super_name)

    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })


@listTable.route("/listGridForCheck", methods=['POST'])
def list_grid_for_check():
    print("listGridForCheck....")

    request_data = request.get_json()

    _reag_id = request_data['reag_id']
    print("reeagent id: ", _reag_id)
    return_value = True

    s = Session()
    reag_item = s.query(Reagent).filter_by(reag_id=_reag_id).first()
    if reag_item:   # 2023-05-03 add
      if not reag_item.grid_id:
        return_value = False
    else:           # 2023-05-03 add
        return_value = False  # 2023-05-03 add

    print("reeagent grid: ", reag_item.grid_id, return_value)

    s.close()
    return jsonify({
        'status':  return_value,
    })

# 2023-04-14 add
@listTable.route("/listGridForCheckByReagentName", methods=['POST'])
def list_grid_for_check_by_reagent_name():
    print("listGridForCheckByReagentName....")

    request_data = request.get_json()
    _reag_name = request_data['reag_name']
    print("reeagent name: ", _reag_name)

    _results = []
    return_value = True
    s = Session()

    if _reag_name is not None:  # 2023-05-03 add
      _objects = s.query(Reagent).filter(Reagent.reag_name.ilike("%" + _reag_name + "%")).all()
      #reag_item = [u.__dict__ for u in _objects]
      for reag_item in _objects:
        print(reag_item.reag_name)
        _results.append(reag_item.reag_name)

    s.close()
    return jsonify({
        'status':  return_value,
         'outputs': _results
    })


# list inStock table all data
@listTable.route("/listStockInData", methods=['GET'])
def list_stockin_data():
    print("listStockInData....")
    s = Session()
    _results = []
    return_value = True
    _objects = s.query(InTag).all()
    # grids = [u.__dict__ for u in _objects]
    for intag in _objects:
        if (intag.isRemoved and (not intag.isPrinted) and (not intag.isStockin)):
            user = s.query(User).filter_by(id=intag.user_id).first()
            reagent = s.query(Reagent).filter_by(id=intag.reagent_id).first()

            k1 = ''
            if reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if reagent.reag_temp == 1:
                k1 = '2~8度C'
            if reagent.reag_temp == 2:
                k1 = '-20度C'

            _obj = {
                'id': intag.id,
                'stockInTag_reagID': reagent.reag_id,
                'stockInTag_reagName': reagent.reag_name,
                'stockInTag_reagPeriod': intag.reag_period,  # 依2022-12-12操作教育訓練建議作修正
                'stockInTag_reagTemp': k1,
                'stockInTag_Date': intag.intag_date,  # 入庫日期
                'stockInTag_EmpID': user.emp_id,
                'stockInTag_Employer': user.emp_name,
                'stockInTag_batch': intag.batch,
                'stockInTag_cnt': intag.count,
                'stockInTag_cnt_max': intag.count,
                'stockInTag_alpha': intag.stockIn_alpha,
                'stockInTag_isPrinted': intag.isPrinted,
                'stockInTag_isStockin': intag.isStockin,
            }

            _results.append(_obj)

    temp_len = len(_results)
    print("listStockInData, total(待入庫資料總數): ", temp_len)
    if (temp_len == 0):
        return_value = False

    s.close()
    return jsonify({
        'status': return_value,
        'outputs': _results
    })


# list inStock table all data(isPrint) for 入庫
@listTable.route("/listStockInLastAlpha", methods=['GET'])
def list_stockin_last_alpha():
    print("listStockInLastAlpha....")
    s = Session()
    _results = []
    return_value = True
    _objects = s.query(InTag).order_by(InTag.stockIn_alpha.desc()).all()
    '''
    for intag in _objects:
        if (intag.isRemoved and intag.isPrinted and (not intag.isStockin)):  # 資料存在, 而且已經貼標籤,
            user = s.query(User).filter_by(id=intag.user_id).first()
            reagent = s.query(Reagent).filter_by(id=intag.reagent_id).first()

            k1 = ''
            if reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if reagent.reag_temp == 1:
                k1 = '2~8度C'
            if reagent.reag_temp == 2:
                k1 = '-20度C'

            _obj = {
                'id': intag.id,
                'stockInTag_reagID': reagent.reag_id,
                'stockInTag_reagName': reagent.reag_name,
                'stockInTag_reagPeriod': intag.reag_period,  # 依2022-12-12操作教育訓練建議作修正
                'stockInTag_reagTemp': k1,
                'stockInTag_Date': intag.intag_date,  # 入庫日期
                'stockInTag_EmpID': user.emp_id,
                'stockInTag_Employer': user.emp_name,
                'stockInTag_batch': intag.batch,
                'stockInTag_cnt': intag.count,

                'active': False,
            }

            _results.append(_obj)
    '''
    s.close()

    temp_len = len(_results)
    print("listStockInLastAlpha, input total(準備列印標籤入庫數): ", temp_len)
    if (temp_len == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': _results
    })


# list inStock table all data(isPrint) for 入庫
@listTable.route("/listStockInItems", methods=['GET'])
def list_stockin_items():
    print("listStockInItems....")
    s = Session()
    _results = []
    return_value = True
    _objects = s.query(InTag).all()

    for intag in _objects:
        if (intag.isRemoved and intag.isPrinted and (not intag.isStockin)):  # 資料存在, 而且已經貼標籤,
            user = s.query(User).filter_by(id=intag.user_id).first()
            reagent = s.query(Reagent).filter_by(id=intag.reagent_id).first()

            k1 = ''
            if reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if reagent.reag_temp == 1:
                k1 = '2~8度C'
            if reagent.reag_temp == 2:
                k1 = '-20度C'

            _obj = {
                'id': intag.id,
                'stockInTag_reagID': reagent.reag_id,
                'stockInTag_reagName': reagent.reag_name,
                'stockInTag_reagPeriod': intag.reag_period,  # 依2022-12-12操作教育訓練建議作修正
                'stockInTag_reagTemp': k1,
                'stockInTag_Date': intag.intag_date,  # 入庫日期
                'stockInTag_EmpID': user.emp_id,
                'stockInTag_Employer': user.emp_name,
                'stockInTag_batch': intag.batch,
                'stockInTag_unit':reagent.reag_In_unit, # add
                'stockInTag_cnt': intag.count,

                'active': False,
            }

            _results.append(_obj)

    s.close()

    temp_len = len(_results)
    print("listStockInItems, input total(準備列印標籤入庫數): ", temp_len)
    if (temp_len == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': _results
    })


# list inStock table all data(isPrint) for 入庫
@listTable.route("/listStockOutItems", methods=['GET'])
def list_stockout_items():
    print("listStockOutItems....")
    s = Session()
    _results = []
    return_value = True  # true: 資料正確
    _objects = s.query(OutTag).all()

    for outtag in _objects:
        if (outtag.isRemoved and outtag.isPrinted and (not outtag.isStockout)):  # 資料存在, 而且已經貼標籤
            user = s.query(User).filter_by(id=outtag.user_id).first()

            in_tag = s.query(InTag).filter_by(id=outtag.intag_id).first()
            reagent = s.query(Reagent).filter_by(id=in_tag.reagent_id).first()

            k1 = ''
            if reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if reagent.reag_temp == 1:
                k1 = '2~8度C'
            if reagent.reag_temp == 2:
                k1 = '-20度C'

            _obj = {
                'id': outtag.id,
                'stockOutTag_reagID': reagent.reag_id,
                'stockOutTag_reagName': reagent.reag_name,
                'stockOutTag_reagPeriod': in_tag.reag_period,  # 依2022-12-12操作教育訓練建議作修正
                'stockOutTag_reagTemp': k1,
                'stockOutTag_Date': outtag.outtag_date,  # 出庫日期
                'stockOutTag_EmpID': user.emp_id,
                'stockOutTag_Employer': user.emp_name,
                'stockOutTag_batch': in_tag.batch,
                'stockOutTag_cnt': outtag.count,
                'stockOutTag_unit':reagent.reag_Out_unit,   # add
                #'stockOutTag_unit':reagent.reag_In_unit,   # add
                'stockOutTag_scale':reagent.reag_scale,

                'active': False,
            }

            _results.append(_obj)
    s.close()

    temp_len = len(_results)
    print("listStockOutItems, output total(準備列印標籤出庫數): ", temp_len)
    if (temp_len == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': _results
    })


# list outStock_tagPrint table all data
@listTable.route("/liststockOutTagPrintData", methods=['GET'])
def list_stockout_tag_print_data():
    print("liststockOutTagPrintData....")
    s = Session()
    _results = []
    _objects = s.query(OutTag).all()
    # grids = [u.__dict__ for u in _objects]
    for outtag_print in _objects:
        if (outtag_print.isRemoved and (not outtag_print.isPrinted) and (not outtag_print.isStockout)):  # 在庫, 還沒列印標籤, 還沒出庫
            user = s.query(User).filter_by(id=outtag_print.user_id).first()

            in_tag = s.query(InTag).filter_by(
                id=outtag_print.intag_id).first()
            reagent = s.query(Reagent).filter_by(id=in_tag.reagent_id).first()

            k1 = ''
            if reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if reagent.reag_temp == 1:
                k1 = '2~8度C'
            if reagent.reag_temp == 2:
                k1 = '-20度C'

            _obj = {
                'id': outtag_print.id,
                'stockOutTag_InID': outtag_print.intag_id,
                'stockOutTag_reagID': reagent.reag_id,
                'stockOutTag_reagName': reagent.reag_name,
                'stockOutTag_reagPeriod': in_tag.reag_period,  # 依2022-12-12操作教育訓練建議作修正
                'stockOutTag_reagTemp': k1,
                'stockOutTag_In_Date': in_tag.intag_date,  # 入庫日期
                'stockOutTag_Out_Date': outtag_print.outtag_date,  # 出庫日期(領用日期)
                'stockOutTag_Employer': user.emp_name,
                'stockOutTag_batch': in_tag.batch,
                #'stockOutTag_unit': outtag_print.unit,     # 2023-01-13 mark
                'stockOutTag_unit': reagent.reag_Out_unit,  # 2023-01-13 add
                'stockOutTag_cnt': outtag_print.count,
                #'stockOutTag_cnt': in_tag.count * reagent.reag_scale, #在庫數 * 比例
                'stockOutTag_alpha': outtag_print.stockOut_alpha,
                # 'stockOutTag_cnt': outtag_print.count - outtag_print.stockOut_temp_count,
                'stockOutTag_isPrinted': outtag_print.isPrinted,
                'stockOutTag_isStockin': outtag_print.isStockout,
            }

            _results.append(_obj)

    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })


# list inStock_tagPrint table all data
@listTable.route("/listStockInTagPrintData", methods=['GET'])
def list_stockin_tag_print_data():
    print("listStockInTagPrintData....")
    s = Session()
    _results = []
    _objects = s.query(InTag).all()
    # grids = [u.__dict__ for u in _objects]
    for intag_print in _objects:
        if (intag_print.isRemoved and (not intag_print.isPrinted) and (not intag_print.isStockin)):
            user = s.query(User).filter_by(id=intag_print.user_id).first()
            reagent = s.query(Reagent).filter_by(
                id=intag_print.reagent_id).first()

            k1 = ''
            if reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if reagent.reag_temp == 1:
                k1 = '2~8度C'
            if reagent.reag_temp == 2:
                k1 = '-20度C'

            _obj = {
                'id': intag_print.id,
                'stockInTag_reagID': reagent.reag_id,
                'stockInTag_reagName': reagent.reag_name,
                'stockInTag_reagPeriod': intag_print.reag_period,  # 依2022-12-12操作教育訓練建議作修正
                'stockInTag_reagTemp': k1,
                'stockInTag_Date': intag_print.intag_date,  # 入庫日期
                'stockInTag_Employer': user.emp_name,
                'stockInTag_batch': intag_print.batch,
                'stockInTag_cnt': intag_print.count,
                'stockInTag_alpha': intag_print.stockIn_alpha,
                # 'stockInTag_cnt': intag_print.count - intag_print.stockOut_temp_count,
                'stockInTag_isPrinted': intag_print.isPrinted,
                'stockInTag_isStockin': intag_print.isStockin,
            }

            _results.append(_obj)

    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })


# list inStock_tagPrint all data count
@listTable.route("/listStockInTagPrintCount", methods=['GET'])
def list_stockin_tag_print_count():
    print("listStockInTagPrintCount....")
    s = Session()

    temp_count = 0
    return_value = True
    _objects = s.query(InTag).all()
    # grids = [u.__dict__ for u in _objects]
    for intag_print in _objects:
        if (intag_print.isRemoved and intag_print.isPrinted and (not intag_print.isStockin)):
            temp_count = temp_count + 1
            print("id: ", intag_print.id)

    s.close()

    print("listStockInTagPrintCount, total(入庫試劑總數): ", temp_count)
    if (temp_count == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': temp_count,
    })


# list outStock_tagPrint all data count
@listTable.route("/listStockOutTagPrintCount", methods=['GET'])
def list_stockout_tag_print_count():
    print("listStockOutTagPrintCount....")
    s = Session()

    temp_count = 0
    return_value = True
    _objects = s.query(OutTag).all()
    # grids = [u.__dict__ for u in _objects]
    for outtag_print in _objects:
        if (outtag_print.isRemoved and outtag_print.isPrinted and (not outtag_print.isStockout)):
            temp_count = temp_count + 1
            print("id: ", outtag_print.id)

    s.close()

    print("listStockOutTagPrintCount, total(待領料試劑總數): ", temp_count)
    if (temp_count == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': temp_count,
    })


# list outStock table all data
@listTable.route("/listStockOutData", methods=['GET'])
def list_stockout_data():
    print("listStockOutData....")
    s = Session()
    _results = []
    return_value = True
    _objects = s.query(OutTag).all()
    # grids = [u.__dict__ for u in _objects]
    for outtag in _objects:
        if (outtag.isRemoved and (not outtag.isPrinted) and (not outtag.isStockout)):
            _inTag = s.query(InTag).filter_by(id=outtag.intag_id).first()
            user = s.query(User).filter_by(id=outtag.user_id).first()
            reagent = s.query(Reagent).filter_by(id=_inTag.reagent_id).first()
            supplier = s.query(Supplier).filter_by(id=reagent.super_id).first()

            _obj = {
                'stockOutTag_reagID': reagent.reag_id,  # 資材碼
                'stockOutTag_reagName': reagent.reag_name,  # 品名
                'stockOutTag_batch': _inTag.batch,    # 入庫批號, 2023-02-10 add
                'stockOutTag_supplier': supplier.super_name,  # 供應商
                'stockOutTag_reagPeriod': _inTag.reag_period,  # 效期, 依2022-12-12操作教育訓練建議作修正
                'stockOutTag_InDate': _inTag.intag_date,  # 入庫日期
                'stockOutTag_Date': outtag.outtag_date,  # 領用日期
                'stockOutTag_EmpID': user.emp_id,
                'stockOutTag_Employer': user.emp_name,
                #'stockOutTag_cnt': outtag.count,
                #'stockOutTag_cnt': _inTag.count * reagent.reag_scale,
                #'stockOutTag_cnt': _inTag.count,
                'stockOutTag_cnt_max': outtag.count,
                'stockOutTag_cnt': outtag.count,
                'stockOutTag_scale': reagent.reag_scale,
                #'stockOutTag_unit': outtag.unit,           # 2023-01-13 mark
                'stockOutTag_unit': reagent.reag_Out_unit,  # 2023-01-13 add
                #'stockOutTag_unit':  reagent.reag_In_unit,  #在庫單位,reag_In_unit
                'stockOutTag_InID': _inTag.id,
                'stockOutTag_ID': outtag.id,
                'stockOutTag_isPrinted': outtag.isPrinted,
                'stockOutTag_isStockin': outtag.isStockout,
            }

            _results.append(_obj)

    temp_len = len(_results)
    print("listStockOutData, total(待出庫資料總數): ", temp_len)
    if (temp_len == 0):
        return_value = False

    s.close()
    return jsonify({
        'status': return_value,
        'outputs': _results
    })


# list requed records(StockOut) all data
@listTable.route("/listRequirements", methods=['GET'])
def list_requirements_data():
    print("listRequirements....")
    s = Session()
    _results = []

    _objects = s.query(OutTag).all()
    ##dup_outtag_list= list()
    for outtag in _objects:
      #print("outtag: ", outtag)
      if (outtag.isRemoved and outtag.isStockout and not outtag.isPrinted):
        _inTag = s.query(InTag).filter_by(id=outtag.intag_id).first()
        #reagent = s.query(Reagent).filter_by(id=in_tag.reagent_id).first()
        ##if in_tag.reagent_id not in dup_outtag_list:
        ##  dup_outtag_list.append(outtag.intag_id)
          #print(outtag.intag_id)

    ##print("dup_outtag_list: ", dup_outtag_list)   #save InTag's reagent_id

    ##for obj in dup_outtag_list:
    #for outtag in _objects:listRequirements
        ##mySum=0
        ##_inobjects = s.query(InTag).all()
        ##for intag in _inobjects:
        ##  if (intag.reagent_id==obj and outtag.isRemoved and outtag.isStockout):
        ##    mySum=mySum+outtag.count

        ##_inTag = s.query(InTag).filter_by(reagent_id=obj).first()
        ##print("_inTag", _inTag.id)
        ##_outTag = s.query(OutTag).filter_by(intag_id=_inTag.id, isRemoved=True, isStockout=True).first()
        _user = s.query(User).filter_by(id=outtag.user_id).first()
        _reagent = s.query(Reagent).filter_by(id=_inTag.reagent_id).first()
        #print("_reagent", _reagent.reag_id)
        _department = s.query(Department).filter_by(id=_reagent.catalog_id).first()
        _supplier = s.query(Supplier).filter_by(id=_reagent.super_id).first()
        _product = s.query(Product).filter_by(id=_reagent.product_id).first()

        dep_name_data=''                        # 2023-04-25 add
        if _department is not None:             # 2023-04-25 add
          dep_name_data=_department.dep_name    # 2023-04-25 add
        sup_name_data=''                        # 2023-04-25 add
        if _supplier is not None:               # 2023-04-25 add
          sup_name_data=_supplier.super_name    # 2023-04-25 add
        prc_name_data=''                        # 2023-04-25 add
        if _product is not None:                # 2023-04-25 add
          prc_name_data=_product.name           # 2023-04-25 add

        #item = s.query(InTag).filter_by(id=obj).first()
        #_reagent = s.query(Reagent).filter_by(id=obj).first()
        print("item.count", outtag.id, _reagent.reag_id)

        '''
        if (outtag.isRemoved and outtag.isStockout):
            _inTag = s.query(InTag).filter_by(id=outtag.intag_id).first()
            _user = s.query(User).filter_by(id=outtag.user_id).first()
            _reagent = s.query(Reagent).filter_by(id=_inTag.reagent_id).first()
            _department = s.query(Department).filter_by(
                id=_reagent.catalog_id).first()
            _supplier = s.query(Supplier).filter_by(
                id=_reagent.super_id).first()
            _product = s.query(Product).filter_by(
                id=_reagent.product_id).first()
            '''

            # grid = s.query(Grid).filter_by(id=_inTag.grid_id).first()
        '''
        for product in _products:  # 列出產品類別
            p_name = product.name
            for _supr in product._suppliers:  # 列出供應商
                for _rg in _supr._reagents:  # 列出該供應商的所有試劑編號
                    if (_rg.reag_id == _reagent.reag_id):
                        break
                else:
                    continue
                break
            else:
                continue
            break
        '''
        _obj = {
            'reqRecord_reagID': _reagent.reag_id,  # 資材碼
            'reqRecord_reagName': _reagent.reag_name,  # 品名
            'reqRecord_prdName': prc_name_data,  # 產品類別
            'reqRecord_catalog': dep_name_data,  # 資材組別
            'reqRecord_supplier': sup_name_data,  # 供應商
            'reqRecord_stockInDate': _inTag.intag_date,  # 入庫日期
            'reqRecord_stockInBatch': _inTag.batch, # 入庫批次, 2023-2-4 add
            'reqRecord_Date': outtag.outtag_date,  # 領用日期
            'reqRecord_Employer': _user.emp_name,
            #'reqRecord_cnt': str(outtag.count) + outtag.unit,              # 2023-01-13 mark
            'reqRecord_cnt': str(outtag.count) + _reagent.reag_Out_unit,    # 2023-01-13 add

            'reqRecord_InTag_ID': _inTag.id,  # 入庫record id
            'reqRecord_OutTag_ID': outtag.id,  # 出庫record id
        }

        _results.append(_obj)

    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })


# list Stock records(StockIn) all data
@listTable.route("/listStockRecords", methods=['GET'])
def list_stock_records():
    print("listStockRecords....")
    s = Session()
    temp_kk = 1  # 紀錄筆數id, 起始值=1
    _results = []

    _objects = s.query(InTag).all()
    dup_intag_list= list()
    for intag in _objects:
      if (intag.isRemoved and intag.isStockin):
        if intag.reagent_id not in dup_intag_list:
          dup_intag_list.append(intag.reagent_id)
          print(intag.reagent_id)

        '''
        #已出庫數
        _objects0 = s.query(OutTag).all()
        myOutCount=0
        myTest=False
        for outtag in _objects0:
          #print("id: ", outtag.intag_id, intag[0])
          if (outtag.intag_id == intag[0]):
            myOutCount=outtag.count
            myTest=True
            print (intag[0])
            break
        #
        if (myTest==False):
          continue
        item = s.query(InTag).filter_by(id=intag[0]).first()
        if (not (item.isRemoved and item.isStockin)):
          continue
        '''
    #_objects = s.query(InTag).all()
    for obj in dup_intag_list:
        mySum=0
        for intag in _objects:
          if (intag.reagent_id==obj and intag.isRemoved and intag.isStockin):
            mySum=mySum+intag.count

        item = s.query(InTag).filter_by(reagent_id=obj).first()
        _reagent = s.query(Reagent).filter_by(id=obj).first()
        print("item.count", obj, mySum)
        '''
        #
        myInCount=item.count * _reagent.reag_scale
        myInCount=myInCount - myOutCount
        myInCount=myInCount/_reagent.reag_scale
        myInCount=math.ceil(myInCount*10)
        myInCount=myInCount/10
        '''
        #
        _supplier = s.query(Supplier).filter_by(id=_reagent.super_id).first()
        #_grid = s.query(Grid).filter_by(id=item.grid_id).first()     # 2023-01-13 mark
        _grid = s.query(Grid).filter_by(id=_reagent.grid_id).first()  # 2023-01-13 add

        sup_name_data=''                        # 2023-04-25 add
        if _supplier is not None:               # 2023-04-25 add
          sup_name_data=_supplier.super_name    # 2023-04-25 add

        _obj = {
            'id': temp_kk,
            'stkRecord_reagID': _reagent.reag_id,         # 資材碼
            'stkRecord_reagName': _reagent.reag_name,     # 品名
            'stkRecord_supplier': sup_name_data,          # 供應商, 2023-04-25 modify
            'stkRecord_Date': item.intag_date,            # 入庫日期
            'stkRecord_period': item.reag_period,         # 效期, 依2022-12-12操作教育訓練建議作修正
            # 安全存量
            'stkRecord_saftStockUnit': str(_reagent.reag_stock) + _reagent.reag_In_unit,
            'stkRecord_saftStock': str(_reagent.reag_stock),  # 安全存量, 數量

            # 在庫數量
            'stkRecord_cntUnit': str(mySum) + _reagent.reag_In_unit,  # 入庫單位
            'stkRecord_scale': _reagent.reag_scale,     # 比例
            'stkRecord_inStock_count': str(item.count),
            # 安全存量與在庫數量的單位
            'stkRecord_unit': _reagent.reag_In_unit,

            'stkRecord_grid': _grid.station + '站' + _grid.layout + '層' + _grid.pos + '格'
        }

        _results.append(_obj)
        temp_kk += 1

    s.close()

    print("temp_kk: ", temp_kk)
    return jsonify({
        'status': 'success',
        'outputs': _results
    })


# list inventory records all data
@listTable.route("/listInventorys", methods=['GET'])
def list_inventorys():
    print("listInventorys....")
    s = Session()
    temp_kk = 1  # 紀錄筆數id, 起始值=1
    _results = []
    _objects = s.query(InTag).all()
    # intags = [u.__dict__ for u in _objects]
    for intag in _objects:
        # if (intag.isRemoved and intag.isPrinted and intag.isStockin):
        #if (intag.isRemoved and intag.isStockin): # 在庫 且 已入庫    , 2023-06-12 modify
        if (intag.isRemoved and intag.isStockin and intag.count > 0): # 在庫 且 已入庫, 2023-06-15 modify
            _user = s.query(User).filter_by(id=intag.user_id).first()
            _reagent = s.query(Reagent).filter_by(id=intag.reagent_id).first()
            # _supplier = s.query(Supplier).filter_by(id=_reagent.super_id).first()
            #_grid = s.query(Grid).filter_by(id=intag.grid_id).first()    # 2023-01-13 mark
            _grid = s.query(Grid).filter_by(id=_reagent.grid_id).first()  # 2023-01-13 add

            _product = s.query(Product).filter_by(id=_reagent.product_id).first() # 2023-05-23 add
            print("_product.name: ", _product.name)
            k1 = ''
            if _reagent.reag_temp == 0:  # 0:室溫、1:2~8度C、2:-20度C
                k1 = '室溫'
            if _reagent.reag_temp == 1:
                k1 = '2~8度C'
            if _reagent.reag_temp == 2:
                k1 = '-20度C'

            # 2023-06-15 modify
            #modify_cnt_str=str(intag.count_inv_modify)
            #modify_comment=intag.comment
            #if intag.count_inv_modify==0.0:
            #  modify_cnt_str=''
            #  modify_comment=''
            modify_cnt_str=''
            modify_comment=''

            _obj = {
                #'id': temp_kk,     # 2023-0612 modify
                'id': intag.id,     #
                'stockInTag_reagID': _reagent.reag_id,          # 資材碼
                'stockInTag_reagName': _reagent.reag_name,      # 品名
                'stockInTag_reagProduct': _product.name,        # 2023-05-23 add, 資材類別
                'stockInTag_stockInBatch': intag.batch,         #批次, # 2023-0216 add
                'stockInTag_reagPeriod': intag.reag_period,     # 效期, 依2022-12-12操作教育訓練建議作修正
                'stockInTag_reagTemp': k1,    # 保存溫度
                'stockInTag_Date': intag.intag_date,    # 入庫日期
                'stockInTag_Employer': _user.emp_name,  # 入庫人員
                'stockInTag_grid': _grid.station + '站' + _grid.layout + '層' + _grid.pos + '格',
                #'stockInTag_grid_id': _grid.id,      # 2023-01-13 mark
                'stockInTag_grid_id': _reagent.grid_id,   # 2023-01-13 add
                'stockInTag_grid_station': _grid.station,
                'stockInTag_grid_layout': _grid.layout,
                'stockInTag_grid_pos': _grid.pos,
                # 在庫數量
                # 'stockInTag_cnt': str(intag.count) + _reagent.reag_In_unit,
                'stockInTag_cnt': str(intag.count) + _reagent.reag_In_unit,
                'stockInTag_cnt_inv_mdf': modify_cnt_str,
                'stockInTag_comment': modify_comment,
                'intag_id': intag.id,
            }

            _results.append(_obj)
            temp_kk += 1

    s.close()
    return jsonify({
        'status': 'success',
        'outputs': _results
    })
