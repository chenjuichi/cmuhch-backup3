import time
import datetime
import pytz
# from tzlocal import get_localzone  # $ pip install tzlocal

from flask import Blueprint, jsonify, request
from sqlalchemy import func
from sqlalchemy import distinct

#from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound  # 2023-07-17 add

from database.tables import User, Reagent, Department, Supplier, Grid, Permission, Product, OutTag, InTag, Setting, Session

from werkzeug.security import generate_password_hash

from operator import itemgetter, attrgetter   # 2023-08-27  add

updateTable = Blueprint('updateTable', __name__)


# ------------------------------------------------------------------


def modify_InTags_grid(_id, _station, _layout, _pos, _reagID):
    return_gridID = 0  # 相同儲位

    s = Session()
    target_grid = s.query(Grid).filter_by(
        station=_station, layout=_layout, pos=_pos).first()

    if not target_grid:
        # new grid, 建立新的儲位
        new_grid = Grid(station=_station, layout=_layout, pos=_pos)
        s.add(new_grid)
        s.flush()
        current_reagent = s.query(Reagent).filter_by(reag_id=_reagID).first()
        current_reagent.grid_id = new_grid.id
        s.commit()
        return_gridID = new_grid.id
    elif not (target_grid.id == _id):  # target grid不等於既有的儲位, 就是不同儲位
        reagent_count = s.query(Reagent).filter_by(
            grid_id=target_grid.id).count()

        if reagent_count >= 1:  # 已經放其他試劑, 同一儲位不能放不同試劑
            print("hello, another same records...")
            return_gridID = -1  # 同一儲位, 不能放相同試劑
        else:
            return_gridID = target_grid.id  # 空儲位, 沒有放其他試劑

    s.close()

    return return_gridID

# ------------------------------------------------------------------

# update password from user table some data


@updateTable.route("/updatePassword", methods=['POST'])
def update_password():
    print("updatePassword....")
    request_data = request.get_json()
    userID = (request_data['empID'] or '')
    newPassword = (request_data['newPassword'] or '')

    return_value = True  # true: 資料正確, 註冊成功
    if userID == "" or newPassword == "":
        return_value = False  # false: 資料不完全 註冊失敗

    s = Session()
    s.query(User).filter(User.emp_id == userID).update(
        {'password': generate_password_hash(
            newPassword, method='sha256')})
    s.commit()
    s.close()

    return jsonify({
        'status': return_value,
    })


# update user's setting from user table some data
@updateTable.route("/updateSetting", methods=['POST'])
def update_setting():
    print("updateSetting....")

    request_data = request.get_json()
    userID = request_data['empID']
    newSetting = (request_data['setting'] or '')

    return_value = True  # true: 資料正確, 註冊成功
    if userID == "" or newSetting == "":
        return_value = False  # false: 資料不完全 註冊失敗
    # print("update setting value: ", newSetting, type(newSetting))
    s = Session()
    # 修改user的設定資料
    _user = s.query(User).filter_by(emp_id=userID).first()
    s.query(Setting).filter(Setting.id == _user.setting_id).update(
        {'items_per_page': newSetting})

    s.query(User).filter(User.emp_id == userID).update(
        {'isOnline': False})  # false:user已經登出(logout)

    s.commit()
    s.close()

    return jsonify({
        'status': return_value,
    })


# from user table update some data by id
@updateTable.route("/updateUser", methods=['POST'])
def update_user():
    print("updateUser....")
    request_data = request.get_json()

    _emp_id = request_data['emp_id']
    _emp_name = request_data['emp_name']

    return_value = True  # true: 資料正確, 註冊成功
    if _emp_id == "" or _emp_name == "":
        return_value = False  # false: 資料不完全 註冊失敗

    dep = (request_data['dep'] or '')  # convert null into empty string

    _password_reset = request_data['password_reset']    # 2023-12-07 add
    newPassword='a12345678'                             # 2023-12-07 add

    s = Session()

    department = s.query(Department).filter_by(dep_name=dep).first()
    if not department:
        return_value = False  # if the user's department does not exist

    if return_value:
        ### 2023-12-07 modify the following block
        if _password_reset=='yes':
          s.query(User).filter(User.emp_id == _emp_id).update(
              { "emp_name": _emp_name,
                "dep_id": department.id,
                "password": generate_password_hash(
                  newPassword, method='sha256')
              })
        else:
          s.query(User).filter(User.emp_id == _emp_id).update(
              { "emp_name": _emp_name,
                "dep_id": department.id,
              })
        ###
        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })


# from reagent table update some data by id
@updateTable.route("/updateReagent", methods=['POST'])
def update_reagent():
    print("updateReagent....")
    request_data = request.get_json()
    _block = request_data['block']

    _id = _block['reag_id']
    _name = _block['reag_name']
    _product = _block['reag_product']
    _in_unit = _block['reag_In_unit']
    _out_unit = _block['reag_Out_unit']
    _scale = _block['reag_scale']
    # _period = _block['reag_period']     #依2022-12-12操作教育訓練建議作修正
    _stock = _block['reag_stock']  # 在庫安全庫存量
    _temp = _block['reag_temp']
    _catalog = _block['reag_catalog']
    _catalog = _block['reag_catalog']

    return_value = True  # true: 資料正確, 註冊成功
    # if _id == "" or _name == "" or _in_unit == "" or _out_unit == "" or _scale == "" or _stock == "" or _temp == "" or _catalog == "":
    #    return_value = False  # false: 資料不完全 註冊失敗

    # convert null into empty string
    _supplier = _block['reag_supplier']

    s = Session()

    supplier = s.query(Supplier).filter_by(super_name=_supplier).first()
    if not supplier:
        return_value = False  # if the reagent's supplier does not exist

    product = s.query(Product).filter_by(name=_product).first()
    if not product:
        return_value = False  # if the reagent's product does not exist

    cat_item = s.query(Department).filter_by(dep_name=_catalog).first()
    if not cat_item:
        return_value = False

    if return_value:
        _scale = int(_scale)
        _stock = float(_stock)

        if _temp == '室溫':  # 0:室溫、1:2~8度C、2:-20度C
            k1 = 0
        if _temp == '2~8度C':
            k1 = 1
        if _temp == '-20度C':
            k1 = 2

        s.query(Reagent).filter(Reagent.reag_id == _id).update(
            {"reag_name": _name,
             "reag_In_unit": _in_unit,
             "reag_Out_unit": _out_unit,
             # "reag_period": _period,
             "reag_scale": _scale,
             "reag_stock": _stock,
             "reag_temp": k1,
             "catalog_id": cat_item.id,
             "product_id": product.id,
             "super_id": supplier.id})
        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })


# from supplier table update some data by id
@updateTable.route("/updateSupplier", methods=['POST'])
def update_supplier():
    print("updateSupplier....")

    request_data = request.get_json()

    _id = request_data['sup_id']
    _name = request_data['sup_name']
    _phone = request_data['sup_phone']
    _address = request_data['sup_address']
    _contact = request_data['sup_contact']
    _products = request_data['sup_products']
    # 2023-04-18 MODIFY
    # data_check = (True, False)[_id == "" or _name == ""
    #                           or _address == "" or _contact == "" or _phone == "" or len(_products) == 0]
    data_check = (True, False)[_id == "" or _name == "" or _contact == ""]

    return_value = True       # true: update資料成功, false: update資料失敗
    if not data_check:  # false: 資料不完全
        return_value = False
        print("step1")
    s = Session()

    current_supplier = s.query(Supplier).filter_by(super_id=_id).first()
    if not current_supplier or not current_supplier.isRemoved:
        return_value = False  # if the supplier does not exist or removed it
        print("step2")
    if return_value:
        productID_array = []
        for tt in current_supplier._products:  # get product's id from supplier
            if tt.isRemoved:  # 該產品沒有刪除
                productID_array.append(tt.id)

        query = s.query(Product).filter(Product.id.in_(productID_array))
        for tt in query:  # remove product data from supplier
            current_supplier._products.remove(tt)

        # update supplier new data
        current_supplier.sup_name = _name
        current_supplier.sup_tel = _phone
        current_supplier.sup_address = _address
        current_supplier.sup_connector = _contact

        for array in _products:  # append new product data into supplier
            prc_record = s.query(Product).filter_by(name=array).first()
            current_supplier._products.append(prc_record)

        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })


# from supplier table update some data by id
@updateTable.route("/updateProduct", methods=['POST'])
def update_product():
    print("updateProduct....")

    request_data = request.get_json()

    _id = request_data['id']
    _name = request_data['prd_name']

    data_check = (True, False)[_id == "" or _name == ""]

    return_value = True       # true: update資料成功, false: update資料失敗
    if not data_check:  # false: 資料不完全
        return_value = False

    s = Session()

    current_product = s.query(Product).filter_by(id=_id).first()
    if not current_product or not current_product.isRemoved:
        return_value = False  # if the supplier does not exist or removed it

    if return_value:
        current_product.name = _name  # update supplier new data

        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })


# from department table update some data by id
@updateTable.route("/updateDepartment", methods=['POST'])
def update_department():
    print("updateDepartment....")
    request_data = request.get_json()

    _block = request_data['block']

    _id = int(_block['id'])  # convert string into integer
    _emp_dep = _block['dep_name']

    data_check = (True, False)[_id == "" or _emp_dep == ""]

    return_value = True       # true: update資料成功, false: update資料失敗
    if not data_check:  # false: 資料不完全
        return_value = False

    s = Session()

    current_department = s.query(Department).filter_by(id=_id).first()
    if not current_department or not current_department.isRemoved:
        return_value = False  # if the supplier does not exist or removed it

    if return_value:
        current_department.dep_name = _emp_dep  # update department new data

        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })


# from reagent table update some data by id
@updateTable.route("/updateGrid", methods=['POST'])
def update_grid():
    print("updateGrid....")
    request_data = request.get_json()

    _id = request_data['grid_id']
    _reagID = request_data['grid_reagID']
    _reagName = request_data['grid_reagName']
    _station = request_data['grid_station']
    _layout = request_data['grid_layout']
    _pos = request_data['grid_pos']

    data_check = (True, False)[_id == "" or _reagID == "" or _reagName == ""]
    # return_value = True  # true: 資料正確, 註冊成功
    # if _id == "" or _reagID == "" or _reagName == "":
    #    return_value = False  # false: 資料不完全 註冊失敗

    return_value = False
    if data_check:
        s = Session()
        # targid grid
        target_grid = s.query(Grid).filter_by(station=_station,
                                              layout=_layout, pos=_pos).first()
        # return_value = False
        if not target_grid:
            # new grid
            new_grid = Grid(station=_station, layout=_layout, pos=_pos)
            s.add(new_grid)
            s.flush()
            s.query(Reagent).filter(Reagent.reag_id ==
                                    _reagID).update({"grid": new_grid.id})
            s.commit()
            return_value = True
        elif not (target_grid.id == _id):  # target grid不等於既有的儲位
            # print("hello__0_1", _id, target_grid.id)
            reagent_count = s.query(Reagent).filter_by(
                grid_id=target_grid.id).count()
            # print("hello__0_2", reagent_count)
            if reagent_count >= 2:
                print("hello, another same records...")
            # remove old grid link
            # print("hello__1")
            # old_grid = s.query(Grid).filter_by(id=_id).first()
            # reagent = s.query(Reagent).filter_by(reag_id=_reagID).first()
            # old_grid._reagents_on_grid.remove(reagent)
            # print("hello__2")
            # ---
            # another_grid = s.query(func.count(distinct(Reagent.grid_id)))
            # ---
            else:
                # update current grid link
                s.query(Reagent).filter(Reagent.reag_id == _reagID).update(
                    {"grid_id": target_grid.id})

                # print("hello__3")
                s.commit()
                # print("hello__4")
                return_value = True

        s.close()

    return jsonify({
        'status': return_value
    })


# from reagent table update some data by id
@updateTable.route("/updateGridsForLed", methods=['POST'])
def update_grids_for_led():
    print("updateGridsForLed....")
    request_data = request.get_json()

    _tab_segs_block_index = ['tab1_segs', 'tab2_segs', 'tab3_segs']
    segs_index = ['segments1', 'segments2',
                  'segments3', 'segments4', 'segments5']

    # ts = time.time()
    # now = datetime.datetime.fromtimestamp(ts)

    return_value = True
    s = Session()

    for i in range(3):
        _tab_segs_block = request_data[_tab_segs_block_index[i]]
        # print("segment: ", _tab_segs_block)

        for j in range(5):
            for obj in _tab_segs_block[segs_index[j]]:  # 第i站第j層資料
                print("obj: ", i+1, j+1, obj)

                # _currentGrid = s.query(Grid).filter_by(
                #    station=obj['grid_station'], layout=obj['grid_layout'], seg_id=obj['seg_id'],).first()
                _currentGrid = s.query(Grid).filter_by(
                    station=i+1, layout=j+1, seg_id=obj['seg_id'],).first()
                if not _currentGrid:
                    # _newGrid = Grid(station=obj['grid_station'],
                    #                layout=obj['grid_layout'],
                    #                seg_id=obj['seg_id'],
                    #                pos=obj['seg_id'],
                    #                range0=obj['range0'],
                    #                range1=obj['range1'],)
                    _newGrid = Grid(station=i+1,
                                    layout=j+1,
                                    seg_id=obj['seg_id'],
                                    pos=obj['seg_id'],
                                    range0=obj['range0'],
                                    range1=obj['range1'],)

                    s.add(_newGrid)
                    s.flush()
                    print("--add new grid--",
                          _tab_segs_block_index[i], segs_index[j], _newGrid.id)
                else:
                    print("--update old grid data--",
                          _tab_segs_block_index[i], segs_index[j], _currentGrid.id)
                    _currentGrid.pos = obj['seg_id']
                    _currentGrid.range0 = obj['range0']
                    _currentGrid.range1 = obj['range1']
                    # _currentGrid.updated_at = now  # 資料修改的時間   ,2022-12-4, 建議新增updated_at欄位

                s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })


# from reagent table update some data by id
@ updateTable.route("/updatePermissions", methods=['POST'])
def update_permissions():
    print("updatePermissions....")
    request_data = request.get_json()

    _id = request_data['perm_empID']

    _system = request_data['perm_checkboxForSystem']
    _admin = request_data['perm_checkboxForAdmin']
    _member = request_data['perm_checkboxForMember']

    return_value = True  # true: 資料正確, 註冊成功
    if _id == "":
        return_value = False  # false: 資料不完全 註冊失敗

    s = Session()
    if return_value:
        # 以最高權限寫入資料庫
        if _member:
            _p_id = 4
        if _admin:
            _p_id = 3
        if _system:
            _p_id = 2

        s.query(User).filter(User.emp_id == _id).update(
            {"perm_id": _p_id})

        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })


# update intag's stockOut_temp_count and outtag's count data
@ updateTable.route("/updateStockOutAndStockInData", methods=['POST'])
def update_StockOut_and_StockIn_data():
    print("updateStockOutAndStockInData....")
    request_data = request.get_json()

    _data = request_data['stockOut_array']
    _count = request_data['stockOut_count']  # 筆數
    print("_data, _count: ", _data, _count)

    return_value = True  # true: 資料正確
    if not _data or len(_data) != _count:
        return_value = False  # false: 資料不完全

    s = Session()

    outtag = s.query(OutTag).filter_by(id=_data['stockOutTag_ID']).first()
    intag = s.query(InTag).filter_by(id=_data['stockOutTag_InID']).first()

    outtag.count = _data['stockOutTag_cnt']   # 修改出庫資料
    # intag.count = intag.count - int(_data['stockOutTag_cnt'])  # 修改入庫資料
    # intag.stockOut_temp_count = intag.stockOut_temp_count + \
    #    int(_data['stockOutTag_cnt'])  # 修改入庫資料
    cursor = s.query(func.sum(OutTag.count)).filter(
        OutTag.intag_id == _data['stockOutTag_InID']).filter(
        OutTag.isRemoved == True)
    total = cursor.scalar()

    # intag.stockOut_temp_count = total  # 修改入庫資料
    intag.stockOut_temp_count = total  # 修改入庫資料, 暫時為0

    s.commit()

    s.close()

    return jsonify({
        'status': return_value,
    })


# from user table update some data by id
@ updateTable.route("/updateStockIn", methods=['POST'])
def update_stockIn():
    print("updateStockIn....")
    request_data = request.get_json()

    intag_id = request_data['id']
    employer = (request_data['stockInTag_Employer'] or '')
    reagID = (request_data['stockInTag_reagID'] or '')
    date = (request_data['stockInTag_Date'] or '')
    cnt = (request_data['stockInTag_cnt'] or '')
    batch = (request_data['stockInTag_batch'] or '')

    print("data: ", employer, reagID, date, cnt, batch)

    return_message = ''
    return_value = True  # true: 資料正確, 註冊成功
    if reagID == "" or employer == "" or date == "" or cnt == "" or batch == "":
        return_value = False  # false: 資料不完全
        return_message = '資料錯誤!'

    s = Session()
    _user = s.query(User).filter_by(emp_name=employer).first()
    if not _user:
        return_value = False  # if the user data does not exist

    _reagent = s.query(Reagent).filter_by(reag_id=reagID).first()
    if not _reagent:
        return_value = False  # if the reagent data  does not exist

    s = Session()

    if return_value:
        s.query(InTag).filter(InTag.id == intag_id).update({
            'user_id': _user.id,
            'reagent_id': _reagent.id,
            'count': cnt,
            'batch': batch,
            'intag_date': date,
        })

        s.commit()

    s.close()

    return jsonify({
        'status': return_value,
        'message': return_message,
    })


@updateTable.route("/updateStockInByPrintFlag", methods=['POST'])
def update_stockin_by_printFlag():
    print("updateStockInByPrintFlag....")

    request_data = request.get_json()

    _blocks = request_data['blocks']
    _count = request_data['count']
    temp = len(_blocks)
    data_check = (True, False)[_count == 0 or temp == 0 or _count != temp]

    print("data: ", _blocks)

    return_message = ''
    return_value = True  # true: 資料正確, true
    if not data_check:  # false: 資料不完全
        return_value = False  # false: 資料不完全
        return_message = '資料錯誤!'

    if return_value:
        s = Session()

        for obj in _blocks:
            _user = s.query(User).filter_by(
                emp_name=obj['stockInTag_Employer']).first()
            if not _user:
                return_value = False  # if the user data does not exist
                return_message = '資料錯誤!'
                break

            _reagent = s.query(Reagent).filter_by(
                reag_id=obj['stockInTag_reagID']).first()
            if not _reagent:
                return_value = False  # if the reagent data  does not exist
                return_message = '資料錯誤!'
                break

            waitting_stockIn = s.query(InTag).filter_by(id=obj['id']).first()
            waitting_stockIn.isPrinted = True
            '''
            new_stockIn = InTag(user_id=_user.id,
                                reagent_id=_reagent.id,
                                #grid_id=_reagent.grid_id,  # 2023-01-13 mark
                                batch=obj['stockInTag_batch'],
                                count=obj['stockInTag_cnt'],
                                # 依2022-12-12操作教育訓練建議作修正
                                reag_period=obj['stockInTag_reagPeriod'],
                                intag_date=obj['stockInTag_Date'],
                                stockIn_alpha=obj['stockInTag_alpha'],
                                isPrinted=True)
            s.add(new_stockIn)
            '''
        s.commit()
        s.close()

    return jsonify({
        'status': return_value,
        'message': return_message,
    })

# 2023-09-22 add
@updateTable.route("/checkBatchForStockIn", methods=['POST'])
def check_batch_for_stockin():
  print("checkBatchForStockIn....")
  #讀前端資料
  request_data = request.get_json()
  _block = request_data['block']
  print("_block: ", _block)
  return_value = True

  s = Session()

  reagent = s.query(Reagent).filter_by(reag_id=_block['stockInTag_reagID']).first()
  intag_object = s.query(InTag).filter(InTag.reagent_id == reagent.id, InTag.intag_date == _block['stockInTag_Date'], InTag.batch == _block['stockInTag_batch']).all()
  if intag_object:
    return_value = False

  s.close()
  print("hi return_value: ", return_value)
  return jsonify({
    'status': return_value
  })


# 2023-07-19 add(modify the getLastBatchAlphaForStockIn function)
@updateTable.route("/insertAlphaForStockIn", methods=['POST'])
def insert_alpha_for_stockin():
  print("insertAlphaForStockIn....")
  #讀前端資料
  request_data = request.get_json()
  _blocks = request_data['blocks']
  print("_blocks: ", _blocks)

  #解析, 讀取並排序selected id資料(=stockinIDs)
  stockinIDs = [ sub['id'] for sub in _blocks ]
  stockinIDs.sort()
  print("data: ", stockinIDs)

  s = Session()

  _results = []
  reagentIDs = []
  batchs=[]
  intagDates=[]
  #inTag_reagIDs=[]

  #以selected id為key, 讀取入庫資料(=intags)
  intag_objects = s.query(InTag).filter(InTag.id.in_(stockinIDs))
  intags = [u.__dict__ for u in intag_objects]
  #print("intags",intags)
  for intag in intags:
    #if (intag['isRemoved'] and intag['isStockin']):
    reagentIDs.append(intag['reagent_id'])
    batchs.append(intag['batch'])
    intagDates.append(intag['intag_date'])
    # 2023-08-28 add
    #reagent = s.query(Reagent).filter_by(id=intag['reagent_id']).first()
    #inTag_reagIDs.append(reagent.reag_id)

  #排序入庫的reagent_id資料(=reagentIDs)
  #print("a: reagentIDs: ", reagentIDs)

  reagentIDs = list(dict.fromkeys(reagentIDs))
  reagentIDs.sort()
  #print("b: reagentIDs: ", reagentIDs)
  #入庫的批次資料(=batchs)
  batchs = list(dict.fromkeys(batchs))
  #batchs.sort()
  #排序入庫的入庫日期資料(=batchs)
  intagDates = list(dict.fromkeys(intagDates))
  intagDates.sort()

  i=1
  for reagentID in reagentIDs:
    #以入庫的reagent_id為key, 搜尋入庫資料中stockIn_alpha的最大值
    # 2023-08-26 MODIFY
    #maxAlphaObjectsOrder = s.query(InTag).filter(InTag.reagent_id == reagentID, InTag.isRemoved == True).order_by(InTag.stockIn_alpha.asc()).all()
    maxAlphaObjectsOrder = s.query(InTag).filter(InTag.reagent_id == reagentID, InTag.isRemoved == True, InTag.isStockin == True).order_by(InTag.stockIn_alpha.asc()).all()
    #print("maxAlphaObjectsOrder: ",maxAlphaObjectsOrder)
    # 2023-0-22 add if~else~
    if maxAlphaObjectsOrder:
      # 2023-08-31 update
      #myAlpha=max(node.stockIn_alpha for node in maxAlphaObjectsOrder)
      myCreateAt=max(node.create_at for node in maxAlphaObjectsOrder)
      kks = [u.__dict__ for u in maxAlphaObjectsOrder]
      #Find the index of a dict within a list, by matching the dict's value
      _index = next((index for (index, d) in enumerate(kks) if d["create_at"] == myCreateAt), None)
      myAlpha=kks[_index]['stockIn_alpha']
    else:
      myAlpha="Z"
    print("myAlpha: ", myAlpha)

    #以入庫日期及批次進行alpha更換
    for intagDate in intagDates: # 2023-08-27 modify
      for batch in batchs:
        _objects=s.query(InTag).filter_by(
          reagent_id=reagentID,
          batch=batch,
          intag_date=intagDate,
        ).all()

        #_objects=[item for item in _blocks if item.get('stockInTag_reagID')==myIntag.id]

        if _objects:
          # 2023-08-27 MODIFY THE FOLLOWING BLOCK
          myAscii=ord(myAlpha)
          if myAscii==ord("Z"):
            myAlpha="A"
          else:
            myAlpha=chr(ord(myAlpha) + 1)
          ###
          for myIntag in _objects:
            #myIntag.stockIn_alpha=myAlpha
            s.query(InTag).filter(InTag.id == myIntag.id).update({'stockIn_alpha': myAlpha})
            selectedItem=[item for item in _blocks if item.get('id')==myIntag.id]
            _obj = {
              'id': selectedItem[0]['id'],
              'stockInTag_reagID': selectedItem[0]['stockInTag_reagID'],
              'stockInTag_reagName': selectedItem[0]['stockInTag_reagName'],
              'stockInTag_reagPeriod': selectedItem[0]['stockInTag_reagPeriod'],  # 依2022-12-12操作教育訓練建議作修正
              'stockInTag_reagTemp': selectedItem[0]['stockInTag_reagTemp'],
              'stockInTag_Date': selectedItem[0]['stockInTag_Date'],  # 入庫日期
              'stockInTag_Employer': selectedItem[0]['stockInTag_Employer'],
              'stockInTag_batch': selectedItem[0]['stockInTag_batch'],
              'stockInTag_cnt': myIntag.count,
              'stockInTag_alpha': myAlpha,
              # 'stockInTag_cnt': myIntag.count - myIntag.stockOut_temp_count,
              'stockInTag_isPrinted': selectedItem[0]['stockInTag_isPrinted'],
              'stockInTag_isStockin': selectedItem[0]['stockInTag_isStockin'],
            }
            _results.append(_obj)

            #print(i,":", myIntag)
            print(i,":", _obj)
            i=i+1
          #myAscii=ord(myAlpha)
          #if myAscii==ord("Z"):
          #  myAlpha="A"
          #else:
          #  myAlpha=chr(ord(myAlpha) + 1)

  #update
  s.commit()

  s.close()

  return_message = ''
  return_value = True   # true: 資料正確
  #newlist = sorted(_results, key=attrgetter('id'))
  newlist = sorted(_results, key=itemgetter('id'))   # 2023-08-25 add

  return jsonify({
    'status': return_value,
    #'outputs': _results
    'outputs': newlist
  })


# 2023-07-20 add
@updateTable.route("/insertBadge", methods=['POST'])
def insert_badge():
  print("insertBadge....")

  request_data = request.get_json()

  _blocks = request_data['blocks']
  #print("_blocks: ", _blocks)
  stockinIDs = [ sub['id'] for sub in _blocks ]
  print("data: ", stockinIDs)

  s = Session()
  return_message = ''
  return_value=True
  _results = []
  reagentIDs = []
  batchs=[]
  intagDates=[]
  letters=[]

  intag_objects = s.query(InTag).filter(InTag.id.in_(stockinIDs))
  intags = [u.__dict__ for u in intag_objects]
  print("intags: ",intags)

  for intag in intags:
    reagentIDs.append(intag['reagent_id'])
    batchs.append(intag['batch'])
    intagDates.append(intag['intag_date'])
    letters.append(intag['stockIn_alpha'])

  print("reagentIDs :", reagentIDs)

  selectMinLetter=''
  selectMaxLetter=''
  if letters:
    selectMinLetter=min(letters)
    selectMaxLetter=max(letters)

  print("letters: ", letters)
  i=0

  for reagentID in reagentIDs:
    # 2023-08-07 add , InTag.count != 0
    maxLetterObjectsOrder = s.query(InTag).filter(InTag.reagent_id == reagentID, InTag.isRemoved == True, InTag.isStockin == True, InTag.count != 0).order_by(InTag.stockIn_alpha.desc()).all()
    myMaxLetter=max(node.stockIn_alpha for node in maxLetterObjectsOrder)
    # 2023-08-07 add , InTag.count != 0
    minLetterObjectsOrder = s.query(InTag).filter(InTag.reagent_id == reagentID, InTag.isRemoved == True, InTag.isStockin == True, InTag.count != 0).order_by(InTag.stockIn_alpha.desc()).all()
    #minObjects = [u.__dict__ for u in minLetterObjectsOrder]
    #print("最晚: ", minObjects)
    #myMinLetter=min(node['stockIn_alpha'] for node in minObjects)
    myMinLetter=min(node.stockIn_alpha for node in minLetterObjectsOrder)
    print("最晚: ", minLetterObjectsOrder)
    t0=ord(letters[i])  #點選紀錄的字母
    t2=ord(myMaxLetter) #最早批號日期的字母
    t1=ord(myMinLetter) #最晚批號日期的字母
    print("sel, t0, t2(最早), t1(最晚): ",ord(selectMinLetter), selectMinLetter, t0, letters[i], t2, myMaxLetter, t1, myMinLetter)

    if ord(selectMinLetter) == t1:
      return_message = ''
      return_value = True
    else:
      return_message = '有更早的在庫試劑...'
      return_value = False
    #print("currentLetter, myMaxLetter, minLetter: ", letters[i], myMaxLetter, myMinLetter )
    i=i+1
  s.close()

  return jsonify({
    'outputs': _results,
    'status': return_value,
    'message':  return_message
  })


'''
@updateTable.route("/updateStockInByPrintFlag", methods=['POST'])
def update_stockin_by_printFlag():
    print("updateStockInByPrintFlag....")

    request_data = request.get_json()

    _blocks = request_data['blocks']
    _count = request_data['count']
    temp = len(_blocks)
    data_check = (True, False)[_count == 0 or temp == 0 or _count != temp]

    print("data: ", _blocks)

    return_message = ''
    return_value = True  # true: 資料正確, true
    if not data_check:  # false: 資料不完全
        return_value = False  # false: 資料不完全
        return_message = '資料錯誤!'
    # now = datetime.datetime.utcnow()
    ts = time.time()
    now = datetime.datetime.fromtimestamp(ts)
    # utc_now, now = datetime.datetime.utcfromtimestamp(
    #    ts), datetime.datetime.fromtimestamp(ts)
    # local_tz = get_localzone()  # get local timezone
    # local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(
    #    local_tz)  # utc -> local

    # print("now: ", now)
    if return_value:
        s = Session()

        items = s.query(InTag).all()
        for row in items:
            if (row.isPrinted and row.isStockin):
                row.isPrinted = False
        s.commit()

        for obj in _blocks:
            s.query(InTag).filter(InTag.id == obj['id']).update(
                {'isPrinted': True,  # true, 條碼已經列印完成
                 'updated_at': now,  # 資料修改的時間
                 })

        s.commit()
        s.close()

    return jsonify({
        'status': return_value,
        'message': return_message,
    })
'''


@updateTable.route("/updateStockOutByPrintFlag", methods=['POST'])
def update_stockout_by_printFlag():
    print("updateStockOutByPrintFlag....")

    request_data = request.get_json()

    _blocks = request_data['blocks']
    _count = request_data['count']
    temp = len(_blocks)
    data_check = (True, False)[_count == 0 or temp == 0 or _count != temp]

    print("data: ", _blocks)

    return_message = ''
    return_value = True  # true: 資料正確, true
    if not data_check:  # false: 資料不完全
        return_value = False  # false: 資料不完全
        return_message = '資料錯誤!'

    if return_value:
        s = Session()

        for obj in _blocks:
            _user = s.query(User).filter_by(
                emp_name=obj['stockOutTag_Employer']).first()
            #print("output barcode, step1...")
            if not _user:
                return_value = False  # if the user data does not exist
                return_message = '資料錯誤!'
                break
            #print("output barcode, step2...")

            waitting_stockOut = s.query(OutTag).filter_by(id=obj['id']).first()
            waitting_stockOut.isPrinted = True
            '''
            new_stockOut = OutTag(user_id=_user.id,
                                  intag_id=obj['stockOutTag_InID'],
                                  count=obj['stockOutTag_cnt'],
                                  #unit=obj['stockOutTag_unit'],
                                  outtag_date=obj['stockOutTag_Out_Date'],
                                  isPrinted=True)

            s.add(new_stockOut)
            '''
            #print("output barcode, step3...")
        s.commit()
        s.close()

    return jsonify({
        'status': return_value,
        'message': return_message,
    })


'''
@updateTable.route("/updateStockOutByPrintFlag", methods=['POST'])
def update_stockout_by_printFlag():
    print("updateStockOutByPrintFlag....")

    request_data = request.get_json()

    _blocks = request_data['blocks']
    _count = request_data['count']
    temp = len(_blocks)
    data_check = (True, False)[_count == 0 or temp == 0 or _count != temp]

    print("data: ", _blocks)

    return_message = ''
    return_value = True  # true: 資料正確
    if not data_check:  # false: 資料不完全
        return_value = False  # false: 資料不完全
        return_message = '資料錯誤!'
    # now = datetime.datetime.utcnow()
    ts = time.time()
    now = datetime.datetime.fromtimestamp(ts)

    # print("now: ", now)
    if return_value:
        s = Session()

        items = s.query(OutTag).all()
        for row in items:
            if (row.isPrinted and row.isStockout):
                row.isPrinted = False
        s.commit()

        for obj in _blocks:
            s.query(OutTag).filter(OutTag.id == obj['id']).update(
                {'isPrinted': True,  # true, 條碼已經列印完成
                 'updated_at': now,  # 資料修改的時間
                 })

        s.commit()
        s.close()

    return jsonify({
        'status': return_value,
        'message': return_message,
    })
'''


@updateTable.route("/updateStockInByCnt", methods=['POST'])
def update_stockin_by_cnt():
    print("updateStockInByCnt....")

    request_data = request.get_json()

    cnt = (request_data['stockInTag_cnt'] or '')
    intag_id = (request_data['id'] or '')

    print("data: ", cnt, intag_id)

    return_message = ''
    return_value = True  # true: 資料正確, true
    if intag_id == "" or cnt == "":
        return_value = False  # false: 資料不完全
        return_message = '數量資料錯誤!'

    if return_value:
        s = Session()
        intag = s.query(InTag).filter_by(
            id=intag_id, isPrinted=False, isStockin=False).first()
        intag.count = cnt
        s.commit()

        s.close()

    return jsonify({
        'status': return_value,
        'message': return_message,
    })


@updateTable.route("/updateStockOutByCnt", methods=['POST'])
def update_stockout_by_cnt():
    print("updateStockOutByCnt....")

    request_data = request.get_json()

    cnt = (request_data['stockOutTag_cnt'] or '')
    outtag_id = (request_data['id'] or '')

    print("data: ", cnt, outtag_id)

    return_message = ''
    return_value = True  # true: 資料正確, true
    if outtag_id == "" or cnt == "":
        return_value = False  # false: 資料不完全
        return_message = '數量資料錯誤!'

    if return_value:
        s = Session()
        outtag = s.query(OutTag).filter_by(
            id=outtag_id, isPrinted=False, isStockout=False).first()
        outtag.count = cnt
        s.commit()

        s.close()

    return jsonify({
        'status': return_value,
        'message': return_message,
    })


@updateTable.route("/updateStockInDataByInv", methods=['POST', 'GET'])
def update_StockIn_data_by_Inv():
    print("updateStockInDataByInv....")

    request_data = request.get_json()

    _blocks = request_data['blocks']
    _count = request_data['count']
    _empID = request_data['empID']
    temp = len(_blocks)
    data_check = (True, False)[_count == 0 or temp == 0 or _count != temp]
    return_value = True  # true: export into excel成功
    return_message = ''
    if not data_check:  # false: 資料不完全
        return_value = False
        return_message = '資料不完整.'

    print("step1, check:", return_value, data_check)

    if return_value:
      ts = time.time()
      now = datetime.datetime.fromtimestamp(ts)
      tty=now.strftime('%Y')
      tty=str(int(tty)-1911)
      ttm=now.strftime('%m')
      ttd=now.strftime('%d')

      # utc_now, now = datetime.datetime.utcfromtimestamp(
      #    ts), datetime.datetime.fromtimestamp(ts)
      # local_tz = get_localzone()  # get local timezone
      # local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(
      #    local_tz)  # utc -> local

      s = Session()
      _user = s.query(User).filter_by(emp_id=_empID).first()
      #print("_empID:", _empID, _user)

      for obj in _blocks:
        #print("obj: ", obj)
        if obj['isGridChange']:  # 儲位有變更
          #print("obj: ", obj)
          gridID = modify_InTags_grid(obj['stockInTag_grid_id'], int(obj['stockInTag_grid_station']),
                                      int(obj['stockInTag_grid_layout']), int(obj['stockInTag_grid_pos']), obj['stockInTag_reagID']) # 2023-06-14 modify
          print("return grid id: ", gridID)
          intag = s.query(InTag).filter_by(id=obj['intag_id']).first()
          reagent = s.query(Reagent).filter_by(id=intag.reagent_id).first()  # 2023-01-13 add

          if gridID == -1:
            return_value = False  # 已經放其他試劑, 儲位重複
            return_message = '儲位重複.'
          if gridID > 0:  # 新儲位或空儲位
            # intag.grid_id = gridID   # 2023-01-13 mark
            reagent.grid_id = gridID  # 2023-01-13 add
          # intag.count = int(obj['stockInTag_cnt_inv_mdf'])      # 修改在庫數資料
          # 修改在庫數資料, 2023-02-13 update
          #intag.count = float(obj['stockInTag_cnt_inv_mdf']) # 2023-06-12 modify

          strTemp=obj['stockInTag_cnt_inv_mdf'].strip()   # 2023-07-13 add
          comment=obj['stockInTag_comment'].strip()       # 2023-07-13 add
          if strTemp:                                     # 2023-07-13 add
            print("intag...step1")
            floatTemp=float(strTemp)                      # 2023-07-13 add
            intag.count = floatTemp
          #print("intag.count = obj['stockInTag_cnt_inv_mdf'] ", intag.count, obj['stockInTag_cnt_inv_mdf'], type(obj['stockInTag_cnt_inv_mdf']) )
          # 修改盤點數資料
          # intag.count_inv_modify = int(obj['stockInTag_cnt_inv_mdf'])   # 2023-01-05 mark
          #intag.count_inv_modify = 0   # 2023-06-12 modify
          #intag.count_inv_modify = 0.0                                   # 2023-07-13 modify
            intag.count_inv_modify = floatTemp                            # 2023-07-13 modify
          elif comment:
            print("intag...step2")
            intag.comment = comment     # 修改盤點說明資料

          if strTemp or comment:
            print("intag...step3")
            #print("_user: ",_empID, _user, _user.id)
            intag.user_id_inv_modify=_user.id                               # 2023-07-13 add
            #print("intag...step4")
            intag.date_inv_modify=tty+"/"+ttm+"/"+ttd
            intag.updated_at = now  # 資料修改的時間

      s.commit()
      s.close()

    return jsonify({
        'status': return_value,
        'message': return_message,
    })
