import math

from flask import Blueprint, jsonify, request
from sqlalchemy import func
from database.tables import User, Reagent, Supplier, Product, Permission, Department, Grid, OutTag, InTag, Setting, Session

from werkzeug.security import generate_password_hash

createTable = Blueprint('createTable', __name__)


# ------------------------------------------------------------------

# create user data and perm.id=1 into table
@createTable.route("/register", methods=['POST'])
def register():
    print("register....")
    request_data = request.get_json()

    emp_id = (request_data['emp_id'] or '')
    emp_name = (request_data['emp_name'] or '')
    sPWD = (request_data['password'] or '')  # convert null into empty string

    return_value = True  # true: 資料正確, 註冊成功
    if emp_id == "" or emp_name == "" or sPWD == "":
        return_value = False  # false: 資料不完全 註冊失敗

    dep = (request_data['dep'] or '')  # convert null into empty string
    # code = request_data['perm_id']

    s = Session()
    department = s.query(Department).filter_by(dep_name=dep).first()
    if not department:
        return_value = False  # if the user's department does not exist

    # permission = s.query(Permission).filter_by(auth_code=code).first()
    # if not permission:
    #    return_value = False  # if the user's permission does not exist

    old_user = s.query(User).filter_by(emp_id=emp_id).first()
    if old_user:
        return_value = False  # if the user exist

    if return_value:
        # kk_setting = Setting(message='hello ' + emp_name)
        new_user_setting = Setting(
            message='hello ' + emp_name,)
        s.add(new_user_setting)
        s.flush()
        new_user = User(emp_id=emp_id,
                        emp_name=emp_name,
                        password=generate_password_hash(sPWD, method='sha256'),
                        dep_id=department.id,
                        # perm_id=permission.id,
                        perm_id=1,  # first permission,auth_code=0:none
                        setting_id=new_user_setting.id,)
        s.add(new_user)

        s.commit()

    s.close()

    return jsonify({
        'status': return_value,
    })


# create user data and perm.id=4 into table
@createTable.route("/createUser", methods=['POST'])
def createUser():
    print("createUser....")
    request_data = request.get_json()

    emp_id = (request_data['emp_id'] or '')
    emp_name = (request_data['emp_name'] or '')
    sPWD = (request_data['password'] or '')  # convert null into empty string

    return_value = True  # true: 資料正確, 註冊成功
    tempID = ""
    tempName = ""
    if emp_id == "" or emp_name == "" or sPWD == "":
        return_value = False  # false: 資料不完全 註冊失敗

    dep = (request_data['dep'] or '')  # convert null into empty string
    # code = request_data['perm_id']

    s = Session()
    department = s.query(Department).filter_by(dep_name=dep).first()
    if not department:
        return_value = False  # if the user's department does not exist

    # permission = s.query(Permission).filter_by(auth_code=code).first()
    # if not permission:
    #    return_value = False  # if the user's permission does not exist

    old_user = s.query(User).filter_by(emp_id=emp_id).first()
    if old_user:
        tempID = old_user.emp_id  # 歷史資料中的員工編號
        tempName = old_user.emp_name
        return_value = False  # if the user exist

    if return_value:
        new_user_setting = Setting(
            message='add ' + emp_name,)
        s.add(new_user_setting)
        s.flush()
        new_user = User(emp_id=emp_id,
                        emp_name=emp_name,
                        password=generate_password_hash(sPWD, method='sha256'),
                        dep_id=department.id,
                        # perm_id=permission.id,
                        perm_id=4,  # first permission,auth_code=0:none
                        setting_id=new_user_setting.id,)
        s.add(new_user)
        s.commit()

    s.close()
    return jsonify({
        'status': return_value,
        'returnID': tempID,
        'returnName': tempName,
    })


# create InTag data into table
@createTable.route("/createStockIn", methods=['POST'])
def create_stockin():
    print("createStockIn....")
    request_data = request.get_json()

    employer = (request_data['stockInTag_Employer'] or '')
    reagID = (request_data['stockInTag_reagID'] or '')
    date = (request_data['stockInTag_Date'] or '')
    cnt = (request_data['stockInTag_cnt'] or '')

    # 依2022-12-12操作教育訓練建議作修正(新增)
    reagPeriod = (request_data['stockInTag_reagPeriod'] or '')

    batch = (request_data['stockInTag_batch'] or '')

    #print("data: ", employer, reagID, date, cnt, batch)

    return_value = True  # true: 資料正確, true
    if reagID == "" or employer == "" or date == "" or cnt == "" or reagPeriod == "" or batch == "":
        return_value = False  # false: 資料不完全

    #print("step1: ", return_value)

    s = Session()
    _user = s.query(User).filter_by(emp_name=employer).first()
    if not _user:
        return_value = False  # if the user data does not exist

    #print("step2: ", return_value)

    _reagent = s.query(Reagent).filter_by(reag_id=reagID).first()
    if not _reagent:
        return_value = False  # if the reagent data  does not exist

    #print("step3: ", return_value)

    if return_value:
        new_stockIn = InTag(user_id=_user.id,
                            reagent_id=_reagent.id,
                            #grid_id=_reagent.grid_id,  # 2023-01-12 mark
                            batch=batch,
                            count=cnt,
                            reag_period=reagPeriod,  # 依2022-12-12操作教育訓練建議作修正
                            intag_date=date,
                            stockIn_alpha='A',
                            comment='')
        s.add(new_stockIn)
        s.flush()
        last_id = new_stockIn.id
        s.commit()
        print("last_id: ", last_id)

    s.close()

    return jsonify({
        'status': return_value,
        'last_id': last_id,
    })


# create InTag data into table
@createTable.route("/addStockInItem", methods=['POST'])
def add_stockin_item():
    print("addStockInItem....")
    request_data = request.get_json()

    _id = request_data['InTagID']
    _count = (request_data['InTagCount'] or '')

    return_value = True  # true: 資料正確, true
    print("stockIn, 入庫: ", _id, _count)

    s = Session()

    intag_item = s.query(InTag).filter_by(id=_id).first()
    # 狀況1, 數量不同(add=>isStockin, _count; modify=>isPrinted, cnt - _count)
    print("intag_item.count: ", intag_item.count, _count)
    if (intag_item.count != _count):  #部分入庫
        print("部分入庫, status 1...")

        new_intag = InTag(user_id=intag_item.user_id,
                          reagent_id=intag_item.reagent_id,
                          count=_count,
                          reag_period=intag_item.reag_period,
                          batch=intag_item.batch,
                          intag_date=intag_item.intag_date,
                          stockIn_alpha=intag_item.stockIn_alpha,
                          #grid_id=intag_item.grid_id, # 2023-01-12 mark
                          isStockin=True)
        s.add(new_intag)

        s.query(InTag).filter(InTag.id == _id).update({
            'isStockin': False,
            'isPrinted': True,
            'count': intag_item.count - _count,
        })
    # 狀況2, 數量相同(add=>isStockin, _count;  modify=>isPrinted false)
    else: #全部入庫
        print("全部入庫, status 2...")
        new_intag = InTag(user_id=intag_item.user_id,
                          reagent_id=intag_item.reagent_id,
                          count=_count,
                          reag_period=intag_item.reag_period,
                          batch=intag_item.batch,
                          intag_date=intag_item.intag_date,
                          stockIn_alpha=intag_item.stockIn_alpha,
                          #grid_id=intag_item.grid_id, # 2023-01-12 mark
                          isStockin=True)
        s.add(new_intag)
        '''
        s.query(InTag).filter(InTag.id == _id).update({
            'isStockin': False,
            'isPrinted': False,
            # 'count': intag_item.count - _count,
        })
        '''
        del_obj = s.query(InTag).filter(InTag.id == _id).delete()
        print("del_obj: ", del_obj)

    s.commit()

    s.close()

    return jsonify({
        'status': return_value,
    })


# create InTag data into table
@createTable.route("/addStockOutItem", methods=['POST'])
def add_stockout_item():
    print("addStockOutItem....")
    request_data = request.get_json()

    _id = request_data['OutTagID']
    _count = (request_data['OutTagCount'] or '')

    return_value = True  # true: 資料正確, true
    print("stockOut, 領料: ", _id, _count)

    s = Session()

    outtag_item = s.query(OutTag).filter_by(id=_id).first()
    intag_item = s.query(InTag).filter_by(id=outtag_item.intag_id).first()
    _reagent = s.query(Reagent).filter_by(id=intag_item.reagent_id).first()

    if (outtag_item.count != _count):  # 部分領料
      #新增領料紀錄(isStockout=True)
      new_outtag = OutTag(user_id=outtag_item.user_id, intag_id=outtag_item.intag_id,
                          count=_count,
                          #unit=outtag_item.unit,       # 2023-01-13 mark
                          outtag_date=outtag_item.outtag_date,

                          stockOut_alpha=outtag_item.stockOut_alpha,
                          isStockout=True)
      s.add(new_outtag)
      #修改目前待領料紀錄(isPrinted=True)
      outtag_item.count = outtag_item.count - _count

      if (_reagent.reag_scale == 1):  #單位相同
        print("狀況1, 部分領料, 出入庫單位相同")  #出入庫單位相同
        '''
        #新增領料紀錄(isStockout=True)
        new_outtag = OutTag(user_id=outtag_item.user_id, intag_id=outtag_item.intag_id,
                            count=_count,
                            #unit=outtag_item.unit,       # 2023-01-13 mark
                            outtag_date=outtag_item.outtag_date,

                            stockOut_alpha=outtag_item.stockOut_alpha,
                            isStockout=True)
        s.add(new_outtag)
        '''

        '''
        s.query(OutTag).filter(OutTag.id == _id).update({
            'isStockout': False,
            'isPrinted': True,
            'count': outtag_item.count - _count,
        })
        '''

        '''
        #修改目前待領料紀錄(isPrinted=True)
        outtag_item.count = outtag_item.count - _count
        '''
        #stockin_item = s.query(InTag).filter_by(id == outtag_item.intag_id).first()
        ##stockin_item = s.query(InTag).filter_by(id = outtag_item.intag_id).first()
        ##tt = stockin_item.count - _count
        #修改領料後,原來在庫紀錄(isStockin=True)
        tt = intag_item.count - _count
        if (tt != 0):
          #s.query(InTag).filter(InTag.id == outtag_item.intag_id).update({'count': tt})
          intag_item.count=tt
        else:
          s.delete(intag_item)
      else: #單位不相同
        print("狀況2, 部分領料, 出入庫單位不同")  #出入庫單位不同

        '''
        new_outtag = OutTag(user_id=outtag_item.user_id, intag_id=outtag_item.intag_id,
                            count=_count,
                            #unit=outtag_item.unit,       # 2023-01-13 mark
                            outtag_date=outtag_item.outtag_date,
                            stockOut_alpha=outtag_item.stockOut_alpha,
                            isStockout=True)
        s.add(new_outtag)
        '''

        #stockin_item = s.query(InTag).filter_by(id == outtag_item.intag_id).first()
        #stockin_item = s.query(InTag).filter_by(id = outtag_item.intag_id).first()
        '''
        tt = intag_item.count * _reagent.reag_scale - _count

        myInCount=tt/_reagent.reag_scale
        myInCount=math.ceil(myInCount*10)
        myInCount=myInCount/10
        '''
####
        temp_count = _count * -1
        temp_scale = _reagent.reag_scale
        for intag_row in s.query(InTag):
          if (not (intag_row.id==outtag_item.intag_id and intag_row.isRemoved and (not intag_row.isPrinted) and intag_row.isStockin)):
            continue

          myReturn=intag_row.count * temp_scale + temp_count   #入庫出庫單位轉換

          if (myReturn==0): #該筆入庫數量與出庫數量相同(單位已轉換)
            intag_row.isRemoved=False
            intag_item.isStockin=False
            intag_item.count=0
            break

          if (myReturn>0):  #該筆入庫數量大於出庫數量(單位已轉換)
            myInCount=myReturn / _reagent.reag_scale
            myInCount=math.floor(myInCount)*10  # 取小數點1位
            myInCount=myInCount/10
            intag_item.count=myInCount
            break

          if (myReturn<0):  #該筆入庫數量小於出庫數量(單位已轉換)
            intag_row.isRemoved=False
            intag_item.isStockin=False
            intag_item.count=0
            temp_count=myReturn
####
        '''
        myInCount=item.count * _reagent.reag_scale
        myInCount=myInCount - myOutCount
        myInCount=myInCount/_reagent.reag_scale
        myInCount=math.ceil(myInCount*10)
        myInCount=myInCount/10
        '''

        '''
        if (tt != 0):
          s.query(InTag).filter(InTag.id == outtag_item.intag_id).update(
                {'count': myInCount})
        else:
          s.delete(stockin_item)
        '''
    else:  # 全部領料
      '''
      new_outtag = OutTag(user_id=outtag_item.user_id, intag_id=outtag_item.intag_id, count=_count,
                          #unit=outtag_item.unit,        # 2023-01-13 mark
                          outtag_date=outtag_item.outtag_date,
                          stockOut_alpha=outtag_item.stockOut_alpha,
                          isStockout=True)
      s.add(new_outtag)
      '''
      outtag_item.count = _count
      outtag_item.isPrinted = False
      outtag_item.isStockout = True
      #if (_reagent.reag_scale == 1):  #單位相同
      print("狀況3/4, 全部領料, 出入庫單位相同/出入庫單位不同")  #出入庫單位相同
      #
      #_objects = s.query(InTag).all()
      #for intag in _objects:
      temp_count = _count * -1
      temp_scale = _reagent.reag_scale
      for intag_row in s.query(InTag):
        if (not (intag_row.id==outtag_item.intag_id and intag_row.isRemoved and (not intag_row.isPrinted) and intag_row.isStockin)):
          continue

        myReturn=intag_row.count * temp_scale + temp_count   #入庫出庫單位轉換

        if (myReturn==0): #該筆入庫數量與出庫數量相同(單位已轉換)
          intag_row.isRemoved=False
          intag_item.isStockin=False
          intag_item.count=0
          break

        if (myReturn>0):  #該筆入庫數量大於出庫數量(單位已轉換)
          myInCount=myReturn / _reagent.reag_scale
          myInCount=math.floor(myInCount)*10  # 取小數點1位
          myInCount=myInCount/10
          intag_item.count=myInCount
          break

        if (myReturn<0):  #該筆入庫數量小於出庫數量(單位已轉換)
          intag_row.isRemoved=False
          intag_item.isStockin=False
          intag_item.count=0
          temp_count=myReturn

    s.commit()

    s.close()

    return jsonify({
        'status': return_value,
    })


'''
# create InTag data into table
@createTable.route("/addStockOutItem", methods=['POST'])
def add_stockout_item():
    print("addStockOutItem....")
    request_data = request.get_json()

    _id = request_data['InTagID']
    _count = (request_data['InTagCount'] or '')

    return_value = True  # true: 資料正確, true
    print("stockOut, 領料: ", _id, _count)

    s = Session()

    s.query(OutTag).filter(OutTag.id == _id).update({
        'isStockout': True,  # true:已入庫
        'count': _count,
    })

    s.commit()

    s.close()

    return jsonify({
        'status': return_value,
    })
'''

# create reagent data table


@createTable.route("/createReagent", methods=['POST'])
def create_reagent():
    print("createReagent....")
    request_data = request.get_json()

    _block = request_data['block']
    #_emp_dep = _block['dep_name']
    print("_block", _block)

    _id = _block['reag_id']
    _name = _block['reag_name']
    _product = _block['reag_product']
    _in_unit = _block['reag_In_unit']
    _out_unit = _block['reag_Out_unit']
    _scale = _block['reag_scale']
    # _period = _block['reag_period']    #依2022-12-12操作教育訓練建議作修正
    _stock = _block['reag_stock']
    _temp = _block['reag_temp']
    _catalog = _block['reag_catalog']

    return_value = True  # true: 資料正確, 註冊成功
    tempID = ""
    tempName = ""

    # if _id == "" or _name == "" or _in_unit == "" or _out_unit == "" or _scale == "" or _stock == "" or _temp == "" or _catalog == "":
    #    return_value = False  # false: 資料不完全 註冊失敗

    # convert null into empty string
    _supplier = _block['reag_supplier']

    s = Session()

    supplier = s.query(Supplier).filter_by(super_name=_supplier).first()
    if not supplier:
        return_value = False  # if the reagent's supplier does not exist
        print("step1")

    product = s.query(Product).filter_by(name=_product).first()
    if not product:
        return_value = False  # if the reagent's product does not exist
        print("step2")

    cat_item = s.query(Department).filter_by(dep_name=_catalog).first()
    if not cat_item:
        return_value = False  # if the reagent's product does not exist
        print("step2-1")

    old_reagent = s.query(Reagent).filter_by(reag_id=_id).first()
    if old_reagent:
        tempID = old_reagent.reag_id
        tempName = old_reagent.reag_name
        return_value = False  # if the user exist
        print("step3")

    if return_value:
        _scale = int(_scale)
        _stock = float(_stock)

        if _temp == '室溫':  # 0:室溫、1:2~8度C、2:-20度C
            k1 = 0
        if _temp == '2~8度C':
            k1 = 1
        if _temp == '-20度C':
            k1 = 2

        new_reagent = Reagent(reag_id = _id,
                              reag_name = _name,
                              reag_In_unit = _in_unit,
                              reag_Out_unit = _out_unit,
                              # reag_period=_period,    #依2022-12-12操作教育訓練建議作修正
                              reag_scale = _scale,
                              reag_stock = _stock,
                              reag_temp = k1,
                              # reag_catalog=_catalog,
                              catalog_id = cat_item.id,
                              product_id = product.id,
                              super_id = supplier.id)
        s.add(new_reagent)
        s.commit()

    s.close()
    return jsonify({
        'status': return_value,
        'returnID': tempID,
        'returnName': tempName,
    })


# create grid data table
@createTable.route("/createGrid", methods=['POST'])
def create_grid():
    print("createGrid....")
    request_data = request.get_json()

    _reagID = request_data['grid_reagID']
    _reagName = request_data['grid_reagName']
    _station = request_data['grid_station']
    _layout = request_data['grid_layout']
    _pos = request_data['grid_pos']

    print("createGrid, data: ", request_data)

    data_check = (True, False)[_reagID == "" or _reagName == ""]
    # return_value = True  # true: 資料正確, 註冊成功
    # if _id == "" or _reagID == "" or _reagName == "":
    #    return_value = False  # false: 資料不完全 註冊失敗

    return_value = True
    tempID=""
    tempName=""
    tempGrid=""
    tempCode=0
    if data_check:
        s = Session()

        old_reagent = s.query(Reagent).filter_by(reag_id=_reagID).first()
        if not old_reagent: #
            tempID = _reagID
            tempName=""
            tempGrid=""
            tempCode=1
            print("createGrid, 狀況1..., 沒有試劑資料")
            return_value = False  ##沒有試劑資料

        else: #有試劑資料
          _old_reagent_id=old_reagent.id

          find_grid = s.query(Grid).filter_by(station=_station, layout=_layout, pos=_pos).first()  # 2023-1-5 mark

          if not find_grid:
              tempID = ""
              tempName=""
              tempGrid=str(_station) + '站' + str(_layout) + '層' + str(_pos) + '格位'
              tempCode=2
              print("createGrid, 狀況2..., 沒有格位資料")
              return_value = False  ##沒有試劑資料
          else: #有格位資料
            _id=find_grid.id

            target_reagent = s.query(Reagent).filter_by(grid_id=_id).first()
            if target_reagent:
                tempID = target_reagent.reag_id
                tempName = target_reagent.reag_name
                tempGrid=str(_station) + '站' + str(_layout) + '層' + str(_pos) + '格位'
                tempCode=3
                print("createGrid, 狀況3..., 該格位已有其他試劑資料" + target_reagent.reag_id)
                return_value = False  #該格位已有其他試劑資料

            else:
                else_grid = s.query(Grid).filter_by(id=_id).first()
                else_reagent = s.query(Reagent).filter_by(grid_id=else_grid.id).first()
                if else_reagent:
                    tempID = _reagID
                    tempName = _reagName
                    tempGrid = else_grid.station + '站' + else_grid.layout + '層' + else_grid.pos + '格位'
                    tempCode=4
                    print("createGrid, 狀況4..., 在其他格位已有該試劑資料")
                    return_value = False  #在其他格位已有該試劑資料
                else: # new grid
                    print("createGrid, 狀況5..., add new grid")

                    s.query(Reagent).filter(Reagent.reag_id == _reagID).update({"grid_id": find_grid.id})
                    s.commit()

        s.close()

    return jsonify({
        'status': return_value,
        'returnID': tempID,
        'returnName': tempName,
        'returnGrid': tempGrid,
        'returnCode': tempCode,
    })


# create supplier data table
@createTable.route("/createSupplier", methods=['POST'])
def create_supplier():
    print("createSupplier....")
    request_data = request.get_json()

    _supID = request_data['sup_id']
    _supName = request_data['sup_name']
    _supAddress = request_data['sup_address']
    _supContact = request_data['sup_contact']
    _supPhone = request_data['sup_phone']
    _supProducts = request_data['sup_products']
    print("_supProducts: ", _supProducts)

    data_check = (True, False)[_supID == "" or _supName ==
                               "" or _supAddress == "" or _supContact == "" or _supPhone == "" or len(_supProducts) == 0]

    return_value = True  # true: 資料正確, 註冊成功
    if not data_check:
        return_value = False  # false: 資料不完全 註冊失敗

    s = Session()

    old_supplier = s.query(Supplier).filter_by(super_id=_supID).first()
    if old_supplier:
        return_value = False  # if the supplier exist

    if return_value:
        new_supplier = Supplier(super_id=_supID, super_name=_supName,
                                super_address=_supAddress, super_connector=_supContact, super_tel=_supPhone)

        s.add(new_supplier)

        s.flush()
        tempID=new_supplier.id
        print("tempID", tempID)

        for array in _supProducts:
            target = s.query(Product).filter_by(name=array).first()
            new_supplier._products.append(target)

        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })


# create product data table
@createTable.route("/createProduct", methods=['POST'])
def create_product():
    print("createProduct....")
    request_data = request.get_json()

    _prdName = request_data['prd_name']

    data_check = (True, False)[_prdName == ""]

    return_value = True   # true: create資料成功, false: create資料失敗
    if not data_check:    # false: 資料不完全
        return_value = False

    s = Session()

    old_product = s.query(Product).filter_by(name=_prdName).first()
    if old_product:
        return_value = False  # the product record had existed

    if return_value:
        new_product = Product(name=_prdName)

        s.add(new_product)
        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })


# create department data table
@createTable.route("/createDepartment", methods=['POST'])
def create_department():
    print("createDepartment....")
    request_data = request.get_json()

    _block = request_data['block']
    _emp_dep = _block['dep_name']

    data_check = (True, False)[_emp_dep == ""]

    return_value = True   # true: create資料成功, false: create資料失敗
    if not data_check:    # false: 資料不完全
        return_value = False

    s = Session()
    old_department = s.query(Department).filter_by(dep_name=_emp_dep).first()
    if old_department:
        return_value = False  # the product record had existed

    if return_value:
        new_department = Department(dep_name=_emp_dep)
        s.add(new_department)
        s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })


# create stockout data into table
@createTable.route("/createStockOut", methods=['POST'])
def create_stockOut():
    print("createStockOut....")
    request_data = request.get_json()

    _data = request_data['stockOut_array']
    _count = request_data['stockOut_count']

    # print("_data, _count: ", _data, _count)
    return_array = []
    return_value = True  # true: 資料正確
    if not _data or len(_data) != _count:
        return_value = False  # false: 資料不完全

    s = Session()

    # _objects = s.query(OutTag).all()
    # _outtags = [u.__dict__ for u in _objects]
    # print("_objects, _outtags: ", type(_objects), type(_outtags))
    # cnt1 = len(_objects)
    # cnt2 = len(_data)
    # print("cnt1, cnt2: ", cnt1, cnt2)
    '''
    for i in range(cnt1):
        result1 = list(_outtags[i].keys())
        for j in range(cnt2):
            result2 = list(_data[j].keys())
            # if outtagKey in _data.keys():
            print("compare Key1: ", result1)
            print("compare Key2: ", result2)
    '''
    _user = s.query(User).filter_by(emp_name=_data[0]['stockOutTag_Employer']).first()

    for i in range(_count):
        new_outtag = OutTag(intag_id=_data[i]['stockOutTag_InID'],
                            user_id=_user.id,
                            #count=_data[i]['stockOutTag_cnt'],
                            count=_data[i]['stockOutTag_cnt'],
                            #unit=_data[i]['stockOutTag_unit'], # 2023-01-13 mark
                            outtag_date=_data[i]['stockOutTag_Date'],
                            )
        s.add(new_outtag)  # 新增一筆出庫資料
        s.flush()
        # print("outtag add, id: ", new_outtag.id)
        return_array.append(new_outtag.id)

        cursor = s.query(func.sum(OutTag.count)).filter(
            OutTag.intag_id == _data[i]['stockOutTag_InID']).filter(
            OutTag.isRemoved == True)
        total = cursor.scalar()
        # print("total: ", total)

        intag = s.query(InTag).filter_by(
            id=_data[i]['stockOutTag_InID']).first()
        # intag.count = intag.count - _data[i]['stockOutTag_cnt']  # 修改入庫資料
        # intag.stockOut_temp_count = intag.stockOut_temp_count + \
        #    _data[i]['stockOutTag_cnt']  # 修改入庫資料
        #intag.stockOut_temp_count = total  # 修改入庫資料
        intag.stockOut_temp_count = 0  # 修改入庫資料, 暫時為0

        s.commit()
    s.close()

    return jsonify({
        'status': return_value,
        'return_outTag_ID': return_array,
    })


'''


for key in Boys.keys():
    if key in Dict.keys():
        print True
    else:
        print False

    s = Session()
    if return_value:
        _objects = s.query(OutTag).all()
        for outtagKey in _objects.keys():
            if outtagKey in _data.keys():

            new_department = OutTag(dep_name=_emp_dep)
            s.add(new_department)
            s.commit()

    s.close()

    return jsonify({
        'status': return_value
    })
'''
