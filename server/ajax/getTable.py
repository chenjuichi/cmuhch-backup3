from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from database.tables import User, Permission, Department, Setting, Supplier, Reagent, Product, InTag, OutTag, Session
from sqlalchemy import and_, or_, not_

from flask_cors import CORS

getTable = Blueprint('getTable', __name__)


# ------------------------------------------------------------------

'''
def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers",
                         "x-requested-with,content-type")
    response.headers.add("Access-Control-Allow-Methods", "POST")
    return response


@getTable.before_request
def oauth_verify(*args, **kwargs):
    """Ensure the oauth authorization header is set"""
    if request.method in ['OPTIONS', ]:
        return
    # if not _is_oauth_valid():
    #    return some_custome_error_response("you need oauth!")


@getTable.after_request
def af_request(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return resp
'''

'''
def props(cls):
    return [i for i in cls.__dict__.keys() if i[:1] != '_']
'''

# list user, department, permission and setting table all data by employee id and password


@getTable.route('/login', methods=['POST'])
def login():
    print("login....")
    request_data = request.get_json()
    userID = (request_data['empID'] or '')
    password = (request_data['password'] or '')
    # remember = True if request_data['remember'] else False

    s = Session()
    user = s.query(User).filter_by(emp_id=userID).first()

    return_value = True  # true: 資料正確
    if not user:
        return_value = False
        _user_object = {}
    else:
        print("login user: ", user)

        xx = not user.isRemoved  # isRemoved=False, 表示該使用者已被註記移除

        if not user or not check_password_hash(user.password, password) or xx:
            return_value = False  # if the user doesn't exist or password is wrong, reload the page
            _user_object = {}
        else:
            # if the above check passes, then we know the user has the right credentials
            # return_value = True

            dep_item = s.query(Department).filter_by(id=user.dep_id).first()
            perm_item = s.query(Permission).filter_by(
                id=user.perm_id).first()
            setting_item = s.query(Setting).filter_by(
                id=user.setting_id).first()

            s.query(User).filter(User.emp_id ==
                                 userID).update({'isOnline': True})
            s.commit()

            _user_object = {
                'empID': user.emp_id,
                'name': user.emp_name,
                'dep': dep_item.dep_name,
                'dep_id': dep_item.id,
                'perm_name': perm_item.auth_name,
                'perm': perm_item.auth_code,
                'password': password,
                'setting_items_per_page': setting_item.items_per_page,
                'setting_message': setting_item.message,
            }

    s.close()

    return jsonify({
        'status': return_value,
        'user': _user_object
    })


# list supplier and inTag table all data by select product object
@getTable.route("/listSuppliersBySelect", methods=['POST'])
def list_suppliers_by_select():
    print("listSuppliersBySelect....")

    request_data = request.get_json()
    selectedProducts = (request_data['catalogs'])
    print("product catalogs: ", selectedProducts)

    _results_for_supplier = []
    _results_for_stockOut = []

    s = Session()

    if selectedProducts:    # 有產品類別選項資料
        products = s.query(Product).all()
        for product in products:  # 列出產品類別
            if product.name in selectedProducts:
                #print("*: ", product.name)
                for supplier in product._suppliers:  # 列出供應商
                    #print("--> ", supplier.super_name)
                    _results_for_supplier.append(supplier.super_name)

                    for reagent in supplier._reagents:  # 列出該供應商的所有試劑編號
                        #print("b reagent: ", reagent.id)
                        _inTag = s.query(InTag).filter_by(reagent_id=reagent.id).first()
                        #if _inTag:
                        #    temp = _inTag.count - _inTag.stockOut_temp_count
                        #if _inTag and temp > 0 and _inTag.isRemoved:    # 列出在庫所有試劑資料
                        if _inTag and _inTag.count > 0 and _inTag.isRemoved and _inTag.isStockin:    # 列出在庫所有試劑資料
                            #print("a reagent: ", _inTag.reagent_id)
                            _obj = {
                                'stockIn_reagent_id': reagent.reag_id,
                                'stockIn_reagent_name': reagent.reag_name,
                                'stockIn_supplier': supplier.super_name,
                                'stockIn_reagent_period': _inTag.reag_period,  # 依2022-12-12操作教育訓練建議作修正
                                'stockIn_date': _inTag.intag_date,  # 入庫日期
                                'stockIn_reagent_Out_unit': reagent.reag_Out_unit,
                                #'stockIn_reagent_Out_unit': reagent.reag_In_unit,
                                # 'stockIn_reagent_Out_cnt': _inTag.count,
                                'stockIn_reagent_Out_cnt': _inTag.count,
                                # 'stockIn_reagent_Out_cnt': 1,
                                'stockIn_id': _inTag.id,
                            }
                            _results_for_stockOut.append(_obj)

    s.close()

    return jsonify({
        'status': 'success',
        'outputs_for_supplier': _results_for_supplier,
        'outputs_for_stockOut': _results_for_stockOut,
    })


# list StockIn table all data by select supplier
@getTable.route("/listStockInDataBySelect", methods=['POST'])
def list_stockInData_by_Select():
    print("listStockInDataBySelect....")

    request_data = request.get_json()
    selectedSuppliers = (request_data['suppliers'])
    selectedCatalogs = (request_data['catalogs'])
    print("product suppliers: ", selectedSuppliers)
    print("product catalogs: ", selectedCatalogs)

    _results_for_stockOut = []

    s = Session()
# ===狀況1
    if selectedCatalogs and selectedSuppliers:  # 有產品類別和供應商選項資料
        print("狀況1...")
        products = s.query(Product).all()
        for product in products:  # 列出產品類別
            if product.name in selectedCatalogs:  # 選項資料內有該筆產品類別名稱
                #print("*: ", product.name)
                for supplier in product._suppliers:  # 列出供應商
                    if supplier.super_name in selectedSuppliers:  # 選項資料內有該筆供應商名稱
                        #print("--> ", supplier.super_name)
                        for reagent in supplier._reagents:  # 列出試劑

                            intags = s.query(InTag).all()
                            for _inTag in intags:
                            #_inTag = s.query(InTag).filter_by(reagent_id=reagent.id).first()
                            #if _inTag:
                            #    #temp = _inTag.count - _inTag.stockOut_temp_count  #stockOut_temp_count暫時都為0
                            #    temp = _inTag.count #stockOut_temp_count暫時都為0
                              if _inTag and _inTag.reagent_id==reagent.id and _inTag.count > 0 and _inTag.isRemoved and _inTag.isStockin:    # 列出在庫所有試劑資料
                                  _obj = {
                                      'id': _inTag.id,
                                      'stockIn_reagent_id': reagent.reag_id,
                                      'stockIn_reagent_name': reagent.reag_name,
                                      'stockIn_supplier': supplier.super_name,
                                      'stockIn_reagent_period': _inTag.reag_period,       #效期
                                      'stockIn_date': _inTag.intag_date,                  #入庫日期
                                      #'stockIn_reagent_Out_unit': reagent.reag_Out_unit,  #領料單位
                                      #'stockIn_reagent_Out_unit': reagent.reag_In_unit,
                                      # 'stockIn_reagent_Out_cnt': _inTag.count,
                                      'stockIn_reagent_Out_cnt': _inTag.count * reagent.reag_scale, #領料數(在庫數 * 比例)
                                      #'stockIn_reagent_Out_cnt': reagent.reag_stock * reagent.reag_scale, #領料數(在庫安全存量 * 比例)
                                # 'stockIn_reagent_Out_cnt': 1,
                                      'stockIn_id': _inTag.id,
                                  }
                                  _results_for_stockOut.append(_obj)
    #end 狀況1
# ===狀況2
    elif not selectedCatalogs and selectedSuppliers:  # 只有供應商選項資料
        print("狀況2...")
        suppliers = s.query(Supplier).all()

        for supplier in suppliers:  # 列出供應商
            if supplier.super_name in selectedSuppliers:  # 選項資料內有該筆供應商名稱
                #print("*: ", supplier.super_name)

                for reagent in supplier._reagents:  # 列出該供應商的所有試劑編號
                    #print("b reagent: ", reagent.id)

                    intags = s.query(InTag).all()
                    for _inTag in intags:
                    #_inTag = s.query(InTag).filter_by(reagent_id=reagent.id).first()

                    #if _inTag:
                    #    #print(type(_inTag.count), type(_inTag.stockOut_temp_count))
                    #    #temp = _inTag.count - _inTag.stockOut_temp_count  #stockOut_temp_count暫時都為0
                    #    temp = _inTag.count #stockOut_temp_count暫時都為0
                    #if _inTag and temp > 0 and _inTag.isRemoved:    # 列出在庫所有試劑資料
                      if _inTag and _inTag.reagent_id==reagent.id and _inTag.count > 0 and _inTag.isRemoved and _inTag.isStockin:    # 列出在庫所有試劑資料
                          _obj = {
                              'id': _inTag.id,
                              'stockIn_reagent_id': reagent.reag_id,
                              'stockIn_reagent_name': reagent.reag_name,
                              'stockIn_supplier': supplier.super_name,
                              'stockIn_reagent_period': _inTag.reag_period,       #效期, 依2022-12-12操作教育訓練建議作修正
                              'stockIn_date': _inTag.intag_date,                  #入庫日期
                              #'stockIn_reagent_Out_unit': reagent.reag_In_unit,
                              'stockIn_reagent_Out_unit': reagent.reag_Out_unit,  #領料單位

                              # 'stockIn_reagent_Out_cnt': _inTag.count,
                              #'stockIn_reagent_Out_cnt': temp,
                              'stockIn_reagent_Out_cnt': _inTag.count * reagent.reag_scale, #領料數(在庫數 * 比例)
                              #'stockIn_reagent_Out_cnt': reagent.reag_stock * reagent.reag_scale, #領料數(在庫安全存量 * 比例)

                              # 'stockIn_reagent_Out_cnt': 1,
                              'stockIn_id': _inTag.id,
                          }
                          _results_for_stockOut.append(_obj)
    #end 狀況2
# ===狀況3
    elif selectedCatalogs and not selectedSuppliers:  # 只有產品類別選項資料
        print("狀況3...")
        products = s.query(Product).all()
        for product in products:  # 列出產品類別
            if product.name in selectedCatalogs:  # 選項資料內有該筆產品類別名稱
                for supplier in product._suppliers:  # 列出供應商
                    # if supplier.super_name in selectedSuppliers:  # 選項資料內有該筆供應商名稱
                    for reagent in supplier._reagents:  # 列出試劑

                        intags = s.query(InTag).all()
                        for _inTag in intags:
                        #_inTag = s.query(InTag).filter_by(reagent_id=reagent.id).first()
                        #print("_inTag: ", _inTag)
                        #if _inTag:
                        #    #temp = _inTag.count - _inTag.stockOut_temp_count  #stockOut_temp_count暫時都為0
                        #    temp = _inTag.count #stockOut_temp_count暫時都為0
                        #if _inTag and temp > 0 and _inTag.isRemoved:    # 列出在庫所有試劑資料
                          if _inTag and _inTag.reagent_id==reagent.id and _inTag.count > 0 and _inTag.isRemoved and _inTag.isStockin:    # 列出在庫所有試劑資料
                              _obj = {
                                  'id': _inTag.id,
                                  'stockIn_reagent_id': reagent.reag_id,
                                  'stockIn_reagent_name': reagent.reag_name,
                                  'stockIn_supplier': supplier.super_name,
                                  # 'stockIn_supplier': '',
                                  'stockIn_reagent_period': _inTag.reag_period,         #效期, 依2022-12-12操作教育訓練建議作修正
                                  'stockIn_date': _inTag.intag_date,                    #入庫日期
                                  'stockIn_reagent_Out_unit': reagent.reag_Out_unit,    #領料單位
                                  # 'stockIn_reagent_Out_cnt': _inTag.count,
                                  #'stockIn_reagent_Out_cnt': _inTag.count,
                                  'stockIn_reagent_Out_cnt': _inTag.count * reagent.reag_scale, #領料數(在庫數 * 比例)
                                  #'stockIn_reagent_Out_cnt': reagent.reag_stock * reagent.reag_scale, #領料數(在庫安全存量 * 比例)

                                  # 'stockIn_reagent_Out_cnt': 1,
                                  'stockIn_id': _inTag.id,
                              }
                              _results_for_stockOut.append(_obj)
    #end 狀況3
    s.close()

    return jsonify({
        'status': 'success',
        # 'outputs_for_supplier': _results_for_supplier,
        'outputs_for_stockOut': _results_for_stockOut,
    })


@getTable.route("/getLastBatchAlphaForStockIn", methods=['GET'])
def get_last_batch_alpha_for_stockin():
    print("getLastBatchAlphaForStockIn....")
    s = Session()
    _results = ''
    return_value = True

    _objects = s.query(InTag).filter(InTag.isRemoved == True, or_(InTag.isPrinted == True, InTag.isStockin == True)
                                     ).order_by(InTag.stockIn_alpha.asc()).all()
    your_count = len(_objects)
    print("your_count: ", your_count)
    your_stockin_date = _objects[your_count-1].intag_date
    if (your_count != 0):
        your_last_alpha = _objects[your_count-1].stockIn_alpha
    else:
        your_last_alpha = 'A'
    print("In, Alpha: ", your_last_alpha)

    s.close()

    if (your_count == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': your_last_alpha,
        'output_date': your_stockin_date,
    })


@getTable.route("/getLastBatchAlphaForStockOut", methods=['GET'])
def get_last_batch_alpha_for_stockout():
    print("getLastBatchAlphaForStockOut....")
    s = Session()
    _results = ''
    return_value = True

    _objects = s.query(OutTag).filter(OutTag.isRemoved == True, or_(OutTag.isPrinted == True, OutTag.isStockout == True)
                                      ).order_by(OutTag.stockOut_alpha.asc()).all()
    your_count = len(_objects)
    print("your_count: ", your_count)
    your_stockout_date = _objects[your_count-1].outtag_date
    if (your_count != 0):
        your_last_alpha = _objects[your_count-1].stockOut_alpha
    else:
        your_last_alpha = 'a'
    print("Out, Alpha: ", your_last_alpha)

    s.close()

    if (your_count == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': your_last_alpha,
        'output_date': your_stockout_date,
    })


@getTable.route("/getLastAlphaForUniqueStockIn", methods=['POST'])
def get_last_alpha_for_unique_stockin():
    print("getLastAlphaForUniqueStockIn....")

    UniqueStockIn = request.get_json()

    print("UniqueStockIn: ", UniqueStockIn)

    s = Session()
    _results = []
    return_value = True

    for record in UniqueStockIn:
      item = s.query(Reagent).filter_by(reag_id=record['stockInTag_reagID']).first()
      _objects = s.query(InTag).filter(InTag.isRemoved==True , InTag.reagent_id==item.id, or_(InTag.isPrinted==True , InTag.isStockin==True)) \
                               .order_by(InTag.stockIn_alpha.asc()).all()


      #_objects = s.query(InTag).filter(InTag.isRemoved==True, InTag.reagent_id==record['stockInTag_reagID'], or_(InTag.isPrinted==True, InTag.isStockin==True)
      #                               ).order_by(InTag.stockIn_alpha.asc()).all()
      #_results.append(_objects)
      current_count = len(_objects)
      #print("current_count: ", current_count)
      #print("_objects: ", _objects)

      #current_stockin_date = _objects[current_count-1].intag_date
      if (current_count != 0):
          #your_last_alpha = chr(ord(_objects[current_count-1].stockIn_alpha)+1)
          your_last_code = ord(_objects[current_count-1].stockIn_alpha) + 1
      else:
          #your_last_alpha = 'A'
          your_last_code = 65

      if (your_last_code > 90):  #ascii is over 'Z'
        your_last_code=65 # 'A'
      your_last_alpha=chr(your_last_code)

      _obj = {
        'reagent_id': record['stockInTag_reagID'],
        'lastAlpha': your_last_alpha,
      }
      _results.append(_obj)

      print("In, Last Alpha: ", your_last_alpha)

    s.close()

    your_count = len(_results)
    if (your_count == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': _results,
    })


@getTable.route("/getLastAlphaForUniqueStockOut", methods=['POST'])
def get_last_alpha_for_unique_stockout():
    print("getLastAlphaForUniqueStockOut....")

    UniqueStockOut = request.get_json()

    print("UniqueStockOut: ", UniqueStockOut)

    s = Session()
    _results = []
    return_value = True

    for record in UniqueStockOut:
      item = s.query(InTag).filter_by(id=record['stockOutTag_InID']).first()
      #print("item: ", item)
      itemForRegent = s.query(Reagent).filter_by(id=item.reagent_id).first()
     # print("itemForRegent: ", itemForRegent)

      _objects = s.query(OutTag) \
                  .filter(OutTag.isRemoved==True , OutTag.intag_id==item.id, or_(OutTag.isPrinted==True , OutTag.isStockout==True)) \
                  .order_by(OutTag.stockOut_alpha.asc()) \
                  .all()
      objs = [u.__dict__ for u in _objects]

      current_count = len(objs)
      #print("current_count: ", current_count)
      #if (current_count != 0):
      #  print("current_count: ", objs[current_count-1]['stockOut_alpha'])

      if (current_count != 0 and (objs[current_count-1]['stockOut_alpha'] is not None)):
          #your_last_alpha = chr(ord(_objects[current_count-1].stockOut_alpha)+1)
          #your_last_code = ord(_objects[current_count-1].stockOut_alpha) + 1
          #your_last_code = ord(_objects[current_count-1]['stockOut_alpha']) + 1
          your_last_code = ord(objs[current_count-1]['stockOut_alpha']) + 1
      else:
          #your_last_alpha = 'a'
          your_last_code = 97

      if (your_last_code > 122):  #ascii is over 'z'
        your_last_code=97 # 'a'

      your_last_alpha=chr(your_last_code)

      _obj = {
        'reagent_id': itemForRegent.reag_id,
        'lastAlpha': your_last_alpha,
      }
      _results.append(_obj)

      print("Out, Last Alpha: ", your_last_alpha, _results)

    s.close()

    your_count = len(_results)
    if (your_count == 0):
        return_value = False

    return jsonify({
        'status': return_value,
        'outputs': _results,
    })


