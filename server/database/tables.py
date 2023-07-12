from datetime import datetime
# from email.policy import default

from sqlalchemy import Table, Column, Float, Integer, String, DateTime, Boolean, func, ForeignKey, create_engine
from sqlalchemy import text
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 宣告一個映射, 建立一個基礎類別
BASE = declarative_base()


# ------------------------------------------------------------------


class User(BASE):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(String(6), nullable=False)
    emp_name = Column(String(10), nullable=False)
    password = Column(String(100), nullable=False)
    # password = Column(String(100), default='a12345678')
    dep_id = Column(Integer, ForeignKey('department.id'))   # 一對多中的 "多"
    perm_id = Column(Integer, ForeignKey('permission.id'))  # 一對多中的 "多"
    setting_id = Column(Integer, ForeignKey('setting.id'))  # 一對多中的 "多"
    isRemoved = Column(Boolean, default=True)  # false:已經刪除資料
    isOnline = Column(Boolean, default=False)  # false:user不再線上(logout)
    _instocks = relationship('InTag', backref="user")     # 一對多中的 "一"
    _outstocks = relationship('OutTag', backref="user")   # 一對多中的 "一"
    create_at = Column(DateTime, server_default=func.now())
    # instock_id = relationship('InStock', backref='user')

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, emp_id={}, emp_name={}, password={}, dep_id={}, perm_id={}, setting_id={}, isRemoved={}".format(
            self.id, self.emp_id, self.emp_name, self.password, self.dep_id, self.perm_id, self.setting_id, self.isRemoved)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'emp_id': self.emp_id,
            'emp_name': self.emp_name,
            'password': self.password,
            'dep_id': self.dep_id,
            'perm_id': self.perm_id,
            'setting_id': self.setting_id,
            'isRemoved': self.isRemoved,
        }


# ------------------------------------------------------------------


class Permission(BASE):  # 一對多, "一":permission, "多":user
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 1:none, 2:system, 3:admin, 4:member
    auth_code = Column(Integer, default=0)
    # 10:none, 2:system, 32:admin, 4:member
    auth_name = Column(String(10), default='none')
    # 設定一對多關聯的"一"
    # 設定cascade後,可刪除級關連
    # 不設定cascade, 則perm_id為空的, 但沒刪除級關連
    _user = relationship('User', backref='permission')
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, auth_code={}".format(self.id, self.auth_code)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'auth_code': self.auth_code,
        }


# ------------------------------------------------------------------


class Department(BASE):  # 一對多, "一":department, "多":user
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dep_name = Column(String(12), nullable=False)
    _reagents = relationship('Reagent', backref="department")

    # 設定一對多關聯的"一"
    # 設定cascade後,可刪除級關連
    # 不設定cascade, 則dep_id為空的, 但沒刪除級關連
    _user = relationship('User', backref='department')
    isRemoved = Column(Boolean, default=True)  # false:已經刪除資料
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, dep_name={}, isRemoved={}".format(self.id, self.dep_name, self.isRemoved)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'dep_name': self.dep_name,
            'isRemoved': self.isRemoved,
        }


# ------------------------------------------------------------------


class Setting(BASE):  # 一對多, "一":permission, "多":user
    __tablename__ = 'setting'

    id = Column(Integer, primary_key=True, autoincrement=True)
    items_per_page = Column(Integer, default=10)
    isSee = Column(String(1), default=text("0"))      # 0:user沒有看去看公告資料
    message = Column(String(30))
    _user = relationship('User', backref='setting')
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, items_per_page={}, isSee={}, message={}".format(self.id, self.items_per_page, self.isSee, self.message)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'items_per_page': self.items_per_page,
            'isSee': self.isSee,
            'message': self.message,
        }


# ------------------------------------------------------------------


class Grid(BASE):
    __tablename__ = 'grid'

    id = Column(Integer, primary_key=True, autoincrement=True)
    station = Column(String(9), nullable=False)
    layout = Column(String(10), nullable=False)
    pos = Column(String(10), nullable=False)
    seg_id = Column(String(10), nullable=False)
    range0 = Column(String(10), nullable=False)
    range1 = Column(String(10), nullable=False)
    # reagent table內的資料除, 父子relation切斷, 也會刪除 reagent的資料
    # _reagents_on_grid = relationship(
    #    'Reagent', backref='grid', cascade="all, delete-orphan")
    # reagent table內的資料除, 父子relation切斷, 但不會刪除 reagent的資料
    _reagents_on_grid = relationship('Reagent', backref='grid', cascade="all, delete")
    #_instocks = relationship('InTag', backref="grid")  # 一對多中的 "一"
    # isRemoved = Column(Boolean, default=True)  # false:已經刪除資料
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, station={}, layout={}, pos={}, seg_id={}, range0={}, range1={}".format(self.id, self.station, self.layout, self.pos, self.seg_id, self.range0, self.range1)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'station': self.station,
            'layout': self.layout,
            'pos': self.pos,  # pos == seg_id
            'seg_id': self.seg_id,
            'range0': self.range0,
            'range1': self.range1,
        }


# ------------------------------------------------------------------


class Reagent(BASE):
    __tablename__ = 'reagent'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reag_id = Column(String(10), nullable=False)    # 2023-04-13 modify String(9) into String(10)
    reag_name = Column(String(50), nullable=False)
    reag_In_unit = Column(String(10), nullable=False)  # 入庫單位
    reag_Out_unit = Column(String(10), nullable=False)  # 出庫單位
    reag_scale = Column(Integer)  # 比例
    # reag_period = Column(String(10), nullable=False)  # 效期, 依2022-12-12教育訓練會後需求,將其移至InTag table
    reag_stock = Column(Float)  # 安全存量
    reag_temp = Column(Integer, default=0)  # 0:室溫、1:2~8度C、2:-20度C

    # reag_catalog = Column(String(20))  # 試劑組別, 2022/11/15討論增加
    catalog_id = Column(Integer, ForeignKey('department.id'))  # 試劑組別
    super_id = Column(Integer, ForeignKey('supplier.id'))

    product_id = Column(Integer, ForeignKey(
        'product.id'))  # 試劑類別  2022-11-18 add

    grid_id = Column(Integer, ForeignKey('grid.id'))
    # true: table有資料,  false:table已經刪除該資料
    isRemoved = Column(Boolean, default=True)
    _instocks = relationship('InTag', backref="reagent")  # 一對多中的 "一"
    # _outstocks = relationship('OutTag', backref="reagent")  # 一對多中的 "一"

    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, reag_id={}, reag_name={}, reag_In_unit={}, \
                reag_Out_unit={}, reag_scale={}, reag_stock={}, \
                reag_temp={}, catalog_id={}, super_id={}, product_id={}, grid_id={}, \
                isRemoved={}, create_at={}".format(
            self.id, self.reag_id, self.reag_name, self.reag_In_unit,
            self.reag_Out_unit, self.reag_scale, self.reag_stock,
            self.reag_temp, self.catalog_id, self.super_id, self.product_id, self.grid_id,
            self.isRemoved, self.create_at)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'reag_id': self.reag_id,
            'reag_name': self.reag_name,
            'reag_In_unit': self.reag_In_unit,
            'reag_Out_unit': self.reag_Out_unit,
            'reag_scale': self.reag_scale,

            'reag_stock': self.reag_stock,
            'reag_temp': self.reag_temp,
            'reag_catalog': self.reag_catalog,
            'super_id': self.super_id,
            'product_id': self.product_id,
            'grid_id': self.grid_id,
            'isRemoved': self.isRemoved,
            'create_at': self.create_at,
        }


# ------------------------------------------------------------------


class Supplier(BASE):
    __tablename__ = 'supplier'

    id = Column(Integer, primary_key=True, autoincrement=True)
    super_id = Column(String(6), nullable=False)        # 2023-04-13 modify String(4) into String(6)
    super_name = Column(String(40), nullable=False)
    super_address = Column(String(80), nullable=False)
    super_connector = Column(String(10), nullable=False)
    super_tel = Column(String(11), nullable=False)

    _reagents = relationship('Reagent', backref="supplier")

    # a:反向參考 Product.Supplier, b:children objects were getting disassociated (parent set to NULL) before the parent is deleted
    _products = relationship(
        'Product', secondary="supplier_product", back_populates="_suppliers")
    # product_supplier_id = relationship('Product', secondary="relations", backref="supplier", cascade="all, delete")
    isRemoved = Column(Boolean, default=True)  # false:已經刪除資料
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, super_id={}, super_name={}, super_address={}, super_connector={}, super_tel={}, isRemoved={}".format(
            self.id, self.super_id, self.super_name, self.super_address, self.super_connector, self.super_tel, self.isRemoved)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'super_id': self.super_id,
            'super_name': self.super_name,
            'super_address': self.super_address,
            'super_connector': self.super_connector,
            'super_tel': self.super_tel,
            'isRemoved': self.isRemoved,
            # 'reag_id': self.reag_id,
            # 'super_product': self.super_product,
        }


# ------------------------------------------------------------------


class Supplier_Product(BASE):
    __tablename__ = 'supplier_product'

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    suppier_id = Column(Integer, ForeignKey('supplier.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    # create_at = Column(DateTime, server_default=func.now())


# ------------------------------------------------------------------


class Product(BASE):    # 多對多, "多":product, "多":supplier
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)

    _reagents = relationship('Reagent', backref="product")  # 2022-11-18 add

    _suppliers = relationship(
        'Supplier', secondary="supplier_product", back_populates="_products")  # a:反向參考 Product.Supplier, b:children objects were getting disassociated (parent set to NULL) before the parent is deleted
    isRemoved = Column(Boolean, default=True)  # false:已經刪除資料
    create_at = Column(DateTime, server_default=func.now())

    # __str__, for print function的輸出; __repr__, 給python顯示變數的輸出
    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, name={}, isRemoved={}".format(self.id, self.name, self.isRemoved)

    # 定義class的dict內容
    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'isRemoved': self.isRemoved,
        }


'''
class InStock(BASE):
    __tablename__ = 'instock'

    id = Column(Integer, primary_key=True, autoincrement=True)
    _intags = relationship('InTag', backref='instock')
    # tag_count = Column(Integer, default=1)
    # tag_unit = Column(String(10), nullable=False)
    create_at = Column(DateTime, server_default=func.now())
    # updated_at = Column(DateTime, onupdate=func.now())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, tag_id={}, create_at={}, update_at={}".format(self.id, self.tag_id, self.create_at, self.update_at)

    def get_dict(self):
        return {
            'id': self.id,
            'tag_id': self.tag_id,
            # 'tag_count': self.count,
            # 'tag_unit': self.unit,
            'create_at':  self.create_at,
            'updated_at':  self.updated_at
        }
'''

# ------------------------------------------------------------------


class InTag(BASE):
    __tablename__ = 'intag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))        # 一對多中的 "多"
    reagent_id = Column(Integer, ForeignKey('reagent.id'))  # 一對多中的 "多"
    #grid_id = Column(Integer, ForeignKey('grid.id'))  # 一對多中的 "多" , 11/26建議刪除, 2023-01-13 mark
    count = Column(Float, default=1.0)                # 入(在)庫數量,  2023-2-10 modify
    ori_count = Column(Float)
    # 效期, 依2022-12-12教育訓練會後需求作增加
    reag_period = Column(String(10), nullable=False)

    stockOut_temp_count = Column(Integer, default=0)  # 暫時領料數 for stockOut計數
    #batch = Column(String(20))                        # 批號
    batch = Column(String(14))                        # 批號  # 2023-01-15 modify
    intag_date = Column(String(10), nullable=False)   # 入庫日期

    _outstocks = relationship('OutTag', backref="intag")  # 一對多中的 "一"

    isRemoved = Column(Boolean, default=True)   # true: 在庫, false:已經刪除資料
    isPrinted = Column(Boolean, default=False)  # false: 標籤尚未列印, true:已列印
    isStockin = Column(Boolean, default=False)  # false:尚未入庫, true:已入庫

    stockIn_alpha = Column(String(4))  # 入庫標籤上的批次文字, 2022/11/15討論增加

    #count_inv_modify = Column(Integer, default=0)  # 盤點數
    count_inv_modify = Column(Float, default=0.0)  # 盤點數 2023-06-12 modify

    comment = Column(String(80), default='')  # 盤點說明  ,  , 11/26建議 default=''

    updated_at = Column(DateTime, onupdate=datetime.utcnow())  # 資料修改的時間

    create_at = Column(DateTime, server_default=func.now())

    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, user_id={}, reagent_id={}, count={}, reag_period={}, \
                batch={}, intag_date={}, stockIn_alpha={}, count_inv_modify={}, comment={}"\
                .format(self.id, self.user_id, self.reagent_id, self.count, self.reag_period,\
                self.batch, self.intag_date, self.stockIn_alpha, self.count_inv_modify, self.comment)

    def get_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'reagent_id': self.reagent_id,
            'count': self.count,

            'reag_period': self.reag_period,
            'batch': self.batch,
            'intag_date': self.intag_date,
            'stockIn_alpha': self.stockIn_alpha,
            'count_inv_modify': self.count_inv_modify,
            'comment': self.comment,

            #'grid_id': self.grid_id,
        }


# ------------------------------------------------------------------

'''
class OutStock(BASE):
    __tablename__ = 'outstock'

    id = Column(Integer, primary_key=True, autoincrement=True)
    _outtags = relationship('OutTag', backref='outstock')
    # tag_count = Column(Integer, default=1)
    # tag_unit = Column(String(10), nullable=False)
    create_at = Column(DateTime, server_default=func.now())
    # updated_at = Column(DateTime, onupdate=func.now())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    def __repr__(self):  # 定義變數輸出的內容
        return "id={}, tag_id={}, create_at={}, update_at={}".format(self.id, self.tag_id, self.create_at, self.update_at)

    def get_dict(self):
        return {
            'id': self.id,
            'tag_id': self.tag_id,
            # 'tag_count': self.count,
            # 'tag_unit': self.unit,
            'create_at':  self.create_at,
            'updated_at':  self.updated_at
        }
'''

# ------------------------------------------------------------------


class OutTag(BASE):
    __tablename__ = 'outtag'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    intag_id = Column(Integer, ForeignKey('intag.id'))
    user_id = Column(Integer, ForeignKey('user.id'))  # 一對多中的 "多"
    # reagent_id = Column(Integer, ForeignKey('reagent.id'))  # 一對多中的 "多"
    # grid_id = Column(Integer, ForeignKey('grid.id'))  # 一對多中的 "多"
    # indate_id = Column(String(10), nullable=False)  # 入庫日期

    count = Column(Float, default=1.0)  # 領料數量,  2023-2-10 modify
    #unit = Column(String(10), nullable=False)  # 單位  # 2023-01-13 mark
    outtag_date = Column(String(10), nullable=False)    # 領用日期

    isRemoved = Column(Boolean, default=True)     # true: 在庫, false:已領料, 且刪單
    isPrinted = Column(Boolean, default=False)    # false: 標籤尚未列印, true:已列印
    # false:尚未出庫(在庫), true:已出庫(領料)
    isStockout = Column(Boolean, default=False)   # false: 還沒出庫

    stockOut_alpha = Column(String(4))  # 出庫標籤上的批次文字, 2022/11/15討論增加

    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    create_at = Column(DateTime, server_default=func.now())

    def __repr__(self):  # 定義變數輸出的內容
        #return "id={}, intag_id={}, user_id={}, count={}, unit={}, outtag_date={}".format(self.id, self.intag_id, self.user_id, self.count, self.unit, self.outtag_date)
        return "id={}, intag_id={}, user_id={}, count={}, outtag_date={}".format(self.id, self.intag_id, self.user_id, self.count, self.outtag_date)

    def get_dict(self):
        return {
            'id': self.id,
            'intag_id': self.intag_id,
            'user_id': self.user_id,
            'count': self.count,
            #'unit': self.unit,   # 2023-01-13 mark
            'outtag_date': self.outtag_date,
        }


# ------------------------------------------------------------------


# 建立連線
###
# 中文字需要 4-bytes 來作為 UTF-8 encoding.
# MySQL databases and tables are created using a UTF-8 with 3-bytes encoding.
# To store 中文字, you need to use the utf8mb4 character set
###
engine = create_engine(
    "mysql+pymysql://root:77974590@localhost:3306/cmuhch?charset=utf8mb4", echo=False)
# 將己連結的資料庫engine綁定到這個session
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    BASE.metadata.create_all(engine)  # 在資料庫中建立表格, 及映射表格內容
    print("table creating is ok...")
