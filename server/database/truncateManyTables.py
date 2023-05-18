from tables import Session, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
#from tables import Product, ProductList, InTag


s = Session()
def truncate_table(table_name):
  #base = declarative_base()
  metadata = MetaData()
  metadata.reflect(bind=engine)
  table = metadata.tables.get(table_name)
  if table is not None:
      print("Truncating", table_name, "table")
      del_name='TRUNCATE TABLE cmuhch.' + table_name;
      s.execute(del_name)


s.execute('SET FOREIGN_KEY_CHECKS = 0')

#truncate_table('intag')
#truncate_table('outtag')
'''

'''
truncate_table('outtag')       # 待入庫table
truncate_table('intag')       # 待入庫table

truncate_table('user')        # 員工table
truncate_table('permission')  # 權限table
truncate_table('department')  # 部門table, 2022-12-31 remove

truncate_table('setting')     # 部門table

truncate_table('reagent')     # 試劑table
truncate_table('grid')        # 格位table
truncate_table('department')  # 部門table, 2022-12-31 add

truncate_table('supplier_product')
truncate_table('product')           # 產品類別table
truncate_table('supplier')          # 供應商table

s.execute('SET FOREIGN_KEY_CHECKS = 1')

s.close()

print("truncate table is ok...")
