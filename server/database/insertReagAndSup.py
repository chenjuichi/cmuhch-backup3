from tables import Supplier, Product, Reagent, Grid, Department, Session

import pymysql
from sqlalchemy import exc

import faker
faker = faker.Faker(locale='zh_TW')

# --------------------------

# insert
s = Session()

# ---grid table data
#             1    2    3    4     5     6    7     8    9    10   11   12
g_station = ['1', '1', '1', '1',  '1',  '1',
             '1', '1', '1', '1',  '1',  '1',
             '1', '1', '1', '1',  '1',  '1',
             '1', '1', '1', '1',  '1',  '1',
             '1', '1', '1', '1',  '1',  '1',

             '2', '2', '2', '2',  '2',  '2',
             '2', '2', '2', '2',  '2',  '2',
             '2', '2', '2', '2',  '2',  '2',
             '2', '2', '2', '2',  '2',  '2',
             '2', '2', '2', '2',  '2',  '2',

             '3', '3', '3', '3',  '3',  '3',
             '3', '3', '3', '3',  '3',  '3',
             '3', '3', '3', '3',  '3',  '3',
             '3', '3', '3', '3',  '3',  '3',
             '3', '3', '3', '3',  '3',  '3',
             ]  # 1 ~ 3
#             1    2    3    4     5     6    7    8    9    10   11   12
g_layout = [ '1', '1', '1', '1',  '1',  '1',
             '2', '2', '2', '2',  '2',  '2',
             '3', '3', '3', '3',  '3',  '3',
             '4', '4', '4', '4',  '4',  '4',
             '5', '5', '5', '5',  '5',  '5',

             '1', '1', '1', '1',  '1',  '1',
             '2', '2', '2', '2',  '2',  '2',
             '3', '3', '3', '3',  '3',  '3',
             '4', '4', '4', '4',  '4',  '4',
             '5', '5', '5', '5',  '5',  '5',

             '1', '1', '1', '1',  '1',  '1',
             '2', '2', '2', '2',  '2',  '2',
             '3', '3', '3', '3',  '3',  '3',
             '4', '4', '4', '4',  '4',  '4',
             '5', '5', '5', '5',  '5',  '5',
            ]  # 1 ~ 5
#              1    2    3    4    5    6    7    8    9    10   11   12
g_position = ['1', '2', '3', '4', '5', '6',
              '1', '2', '3', '4', '5', '6',
              '1', '2', '3', '4', '5', '6',
              '1', '2', '3', '4', '5', '6',
              '1', '2', '3', '4', '5', '6',

              '1', '2', '3', '4', '5', '6',
              '1', '2', '3', '4', '5', '6',
              '1', '2', '3', '4', '5', '6',
              '1', '2', '3', '4', '5', '6',
              '1', '2', '3', '4', '5', '6',

              '1', '2', '3', '4', '5', '6',
              '1', '2', '3', '4', '5', '6',
              '1', '2', '3', '4', '5', '6',
              '1', '2', '3', '4', '5', '6',
              '1', '2', '3', '4', '5', '6',
              ]  # 1 ~ 10
#                1     2    3    4    5    6   7    8    9   10   11    12    13    14
g_led_seg_id = ['1', '2', '3', '4', '5', '6',
               '1', '2', '3', '4', '5', '6',
               '1', '2', '3', '4', '5', '6',
               '1', '2', '3', '4', '5', '6',
               '1', '2', '3', '4', '5', '6',

               '1', '2', '3', '4', '5', '6',
               '1', '2', '3', '4', '5', '6',
               '1', '2', '3', '4', '5', '6',
               '1', '2', '3', '4', '5', '6',
               '1', '2', '3', '4', '5', '6',

               '1', '2', '3', '4', '5', '6',
               '1', '2', '3', '4', '5', '6',
               '1', '2', '3', '4', '5', '6',
               '1', '2', '3', '4', '5', '6',
               '1', '2', '3', '4', '5', '6',
                ]
#                1      2     3     4    5      6     7    8     9   10    11    12    13    14
g_led_range0 = ['1',  '7',  '12', '17', '22', '27',
                '1',  '7',  '12', '17', '22', '27',
                '1',  '7',  '12', '17', '22', '27',
                '1',  '7',  '12', '17', '22', '27',
                '1',  '7',  '12', '17', '22', '27',

                '2',  '7',  '12', '17', '22', '27',
                '2',  '7',  '12', '17', '22', '27',
                '2',  '7',  '12', '17', '22', '27',
                '2',  '7',  '12', '17', '22', '27',
                '2',  '7',  '12', '17', '22', '27',

                '3',  '7',  '12', '17', '22', '27',
                '3',  '7',  '12', '17', '22', '27',
                '3',  '7',  '12', '17', '22', '27',
                '3',  '7',  '12', '17', '22', '27',
                '3',  '7',  '12', '17', '22', '27',
                ]
#                 1     2     3     4    5      6     7    8     9     10    11    12    13    14
g_led_range1 = ['5',  '10', '15', '20', '25', '30',
                '5',  '10', '15', '20', '25', '30',
                '5',  '10', '15', '20', '25', '30',
                '5',  '10', '15', '20', '25', '30',
                '5',  '10', '15', '20', '25', '30',

                '5',  '10', '15', '20', '25', '29',
                '5',  '10', '15', '20', '25', '29',
                '5',  '10', '15', '20', '25', '29',
                '5',  '10', '15', '20', '25', '29',
                '5',  '10', '15', '20', '25', '29',

                '5',  '10', '15', '20', '25', '28',
                '5',  '10', '15', '20', '25', '28',
                '5',  '10', '15', '20', '25', '28',
                '5',  '10', '15', '20', '25', '28',
                '5',  '10', '15', '20', '25', '28',
                ]

G_objects = []
temp_grid_size = len(g_station)
print("insert grid size: ", temp_grid_size)
for i in range(temp_grid_size):
    g = Grid(
        # reagent_id=g_reag_id[i],
        station=g_station[i],
        layout=g_layout[i],
        pos=g_position[i],
        seg_id=g_led_seg_id[i],
        range0=g_led_range0[i],
        range1=g_led_range1[i],
    )
    G_objects.append(g)

s.bulk_save_objects(G_objects)
try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()
# ---

# ---supplier table data
super_id = ['1234', '1201', '2301', '3401',
            '2222', '3333', '6767', '2525', '5555', '6789', '7700']
#             0         1       2       3       4        5      6        7      8       9
super_name = ['貝克曼', '醫全',  '裕利', '大樹', '實用',  '尚上', '伯昂',  '育聖', '亞培', '醫尚', '希森美康']

tel = faker.numerify("0#-########")
if (tel[0:3] == '00'):
    tel.replace("00", "02")
if (tel[0:3] == '01'):
    tel.replace("01", "02")
if (tel[0:3] == '09'):
    tel.replace("09", "02")
su1 = Supplier(
    super_id=super_id[0],
    super_name=super_name[0],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=tel)
s.add(su1)

tel = faker.numerify("0#-########")
if (tel[0:3] == '00'):
    tel.replace("00", "02")
if (tel[0:3] == '01'):
    tel.replace("01", "02")
if (tel[0:3] == '09'):
    tel.replace("09", "02")
su2 = Supplier(
    super_id=super_id[1],
    super_name=super_name[1],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=tel)
s.add(su2)

tel = faker.numerify("0#-########")
if (tel[0:3] == '00'):
    tel.replace("00", "02")
if (tel[0:3] == '01'):
    tel.replace("01", "02")
if (tel[0:3] == '09'):
    tel.replace("09", "02")
su3 = Supplier(
    super_id=super_id[2],
    super_name=super_name[2],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=tel)
s.add(su3)

tel = faker.numerify("0#-########")
if (tel[0:3] == '00'):
    tel.replace("00", "02")
if (tel[0:3] == '01'):
    tel.replace("01", "02")
if (tel[0:3] == '09'):
    tel.replace("09", "02")
su4 = Supplier(
    super_id=super_id[3],
    super_name=super_name[3],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=tel)
s.add(su4)

tel = faker.numerify("0#-########")
if (tel[0:3] == '00'):
    tel.replace("00", "02")
if (tel[0:3] == '01'):
    tel.replace("01", "02")
if (tel[0:3] == '09'):
    tel.replace("09", "02")
su5 = Supplier(
    super_id=super_id[4],
    super_name=super_name[4],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=tel)
s.add(su5)

tel = faker.numerify("0#-########")
if (tel[0:3] == '00'):
    tel.replace("00", "02")
if (tel[0:3] == '01'):
    tel.replace("01", "02")
if (tel[0:3] == '09'):
    tel.replace("09", "02")
su6 = Supplier(
    super_id=super_id[5],
    super_name=super_name[5],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=tel)
s.add(su6)

tel = faker.numerify("0#-########")
if (tel[0:3] == '00'):
    tel.replace("00", "02")
if (tel[0:3] == '01'):
    tel.replace("01", "02")
if (tel[0:3] == '09'):
    tel.replace("09", "02")
su7 = Supplier(
    super_id=super_id[6],
    super_name=super_name[6],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=tel)
s.add(su7)

tel = faker.numerify("0#-########")
if (tel[0:3] == '00'):
    tel.replace("00", "02")
if (tel[0:3] == '01'):
    tel.replace("01", "02")
if (tel[0:3] == '09'):
    tel.replace("09", "02")
su8 = Supplier(
    super_id=super_id[7],
    super_name=super_name[7],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=tel)
s.add(su8)

tel = faker.numerify("0#-########")
if (tel[0:3] == '00'):
    tel.replace("00", "02")
if (tel[0:3] == '01'):
    tel.replace("01", "02")
if (tel[0:3] == '09'):
    tel.replace("09", "02")
su9 = Supplier(
    super_id=super_id[8],
    super_name=super_name[8],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=tel)
s.add(su9)

tel = faker.numerify("0#-########")
if (tel[0:3] == '00'):
    tel.replace("00", "02")
if (tel[0:3] == '01'):
    tel.replace("01", "02")
if (tel[0:3] == '09'):
    tel.replace("09", "02")
su10 = Supplier(
    super_id=super_id[9],
    super_name=super_name[9],
    super_address=faker.address(),
    super_connector=faker.name(),
    super_tel=tel)
s.add(su10)

tel = faker.numerify("0#-########")
if (tel[0:3] == '00'):
    tel.replace("00", "02")
if (tel[0:3] == '01'):
    tel.replace("01", "02")
if (tel[0:3] == '09'):
    tel.replace("09", "02")
su11 = Supplier(
    super_id=super_id[10],
    super_name=super_name[10],
    super_address='台北市',
    super_connector='洪小姐',
    super_tel=tel)
s.add(su11)

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()
# ---

# ---product table data 產品類別
p1 = Product(name='基因檢測試劑')  # '貝克曼', '醫全',  '尚上', '伯昂',  '育聖', '亞培', '醫尚'
p2 = Product(name='核酸萃取試劑')  # '貝克曼', '醫全',  '實用',  '伯昂',  '育聖', '亞培', '醫尚'
p3 = Product(name='離心機')
p4 = Product(name='C13檢測試劑')
p5 = Product(name='能力試驗')
p6 = Product(name='教育訓練')
p7 = Product(name='抗血清試劑')
p8 = Product(name='血液諮詢')
p9 = Product(name='Microscan細菌鑑定試劑')
p10 = Product(name='台塑生醫EV71-IgM(rapid-tset)')

s.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10])
try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

# 供應商資料
records = s.query(Supplier).all()
#print("total suppliers: ", records)

# 將供應商與產品類別做連結
arrays = [p1, p2, p3, p4, p5, p6, p8]  # '貝克曼'
for array in arrays:
    records[0]._products.append(array)
arrays = [p1, p2, p3, p7]  # '醫全'
for array in arrays:
    records[1]._products.append(array)
arrays = [p4, p5, p10]  # '裕利'
for array in arrays:
    records[2]._products.append(array)
arrays = [p6, p7, p8, p9]  # '大樹'
for array in arrays:
    records[3]._products.append(array)
arrays = [p2, p4, p6, p8]  # '實用'
for array in arrays:
    records[4]._products.append(array)
arrays = [p1, p4, p6, p8]  # '尚上'
for array in arrays:
    records[5]._products.append(array)
arrays = [p1, p2, p6, p8]  # '伯昂'
for array in arrays:
    records[6]._products.append(array)
arrays = [p1, p2, p4]  # '育聖'
for array in arrays:
    records[7]._products.append(array)
arrays = [p1, p2, p3, p4, p5, p6, p7, p8, p9]  # '亞培'
for array in arrays:
    records[8]._products.append(array)
arrays = [p1, p2, p3, p4, p5, p6, p7, p8, p9]  # '醫尚'
for array in arrays:
    records[9]._products.append(array)
arrays = [p1, p2, p3, p4, p5, p6, p7, p8]  # '希森美康'
for array in arrays:
    records[10]._products.append(array)

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

# --------------------------

# ---reagent table data 試劑
reag_id = ['3896124', '3896125', '3802252',
           '3802253', '3896126', '3896090',
           '3802255', '3896127', '3896085',
           '3896089', '2G22.01', '7C18.03',
           '6C32.01', '6C34.01',
           '6C37.02', '8L44.01', '4J27.03', '6C17.03', '2K47.01',
           '2K46.01', '2G22.10', '7C18.13', '6C32.10', '6C34.10',
           '6C37.15', '8L44.10', '4J27.12', '6C17.13', '2K47.20',
           '2K46.10',
           '3896100', '3803212', '3803150', '3803284', '3803285', '3803129', '3802341',
           '3802342',
           '3802343',
           'OSR6178',
           ]
reag_name = ['HBsAg',  'Anti-HBs',   'HBeAg',
             'Anti-HBe',  'Anti-HCV',  'Anti-TPO',
             'Anti-HBc', 'HIV',  'Anti-Rubella IgG',
             'Anti-TG', 'HBsAg Cali   2G22.01',  'Anti-HBs Cali  7C18.03',
             'HBeAg Cali  6C32.01', 'Anti-HBe Cali  6C34.01',
             'Anti-HCV Cali  6C37.02', 'Anti-HBc Cali  8L44.01', 'HIV Cali  4J27.03', 'Anti-Rubella IgG Cali  6C17.03', 'Anti-TPO Cali  2K47.01',
             'Anti-TG Cali  2K46.01 ', 'HBsAg QC  2G22.10', 'Anti-HBs QC  7C18.13', 'HBeAg QC  6C32.10', 'Anti-HBe QC  6C34.10',
             'Anti-HCV QC  6C37.15', 'Anti-HBc QC  8L44.10', 'HIV QC  4J27.12', 'Anti-Rubella IgG QC  6C17.13', 'Anti-TPO QC  2K47.10',
             'Anti-TG QC  2K46.10',
             'Probe Condition Solution  1L56.40', 'PCT', 'D-Dimer', 'NT-proBNP', 'QCV', 'ETOH', 'OSR6199 CRP Latex',
             'OSR6193 Lactate',
             'B46435 Urine/CSF Albumin',
             'CREA',
             ]
#                1     2     3     4     5     6    7     8     9    10
reag_In_unit = ['組', '組', '組', '組', '組', '組', '組', '組', '組', '組',
                '組', '組', '組', '組', '組', '組', '組', '組', '組', '組',
                '組', '組', '組', '組', '組', '組', '組', '組', '組', '組',
                '盒', '盒', '盒', '盒', '盒', '盒', '盒', '盒', '盒', '盒',
                ]
#                 1     2     3     4    5     6     7     8     9     10
reag_Out_unit = ['組', '組', '組', '組', '組', '組', '組', '組', '組', '組',
                 '組', '組', '組', '組', '組', '組', '組', '組', '組', '組',
                 '組', '組', '組', '組', '組', '組', '組', '組', '組', '組',
                 '盒', '盒', '盒', '盒', '盒', '瓶', '瓶', '瓶', '瓶', '瓶',
                 ]
#             1  2  3  4  5  6  7  8  9  10
reag_scale = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 1, 2, 4, 4, 4, 4,
              ]
#             1  2  3  4  5  6  7  8  9  10
reag_stock = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 1, 1, 2, 2, 2, 2,
              ]
#            1  2  3  4  5  6  7  8  9  10
reag_temp = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 2, 2,
             1, 1, 1, 1, 1, 1, 1, 1, 2, 2,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             ]  # 0:室溫、1:2~8度C、2:-20度C

#                 1      2       3      4       5      6       7       8       9      10
reag_catalog = ['血清', '血清', '血清', '血清', '血清', '血液', '血液', '血液', '血液', '血液',
                '血液', '血液', '血液', '血液', '血清', '血清', '血清', '血清', '血液', '血液',
                '血清', '血清', '血清', '血液', '血液', '血清', '血清', '血清', '血液', '血液',
                '血液', '血液', '血液', '血液', '血液', '血清', '血清', '血清', '血清', '血清',
               ]

#           1  2  3  4  5  6  7  8  9  10
catalogs = [1, 2, 3, 4, 5, 6, 1, 2, 3, 4,
            5, 6, 1, 2, 3, 4, 5, 6, 1, 2,
            3, 4, 5, 6, 1, 2, 3, 4, 5, 6,
            1, 2, 3, 4, 5, 6, 1, 2, 6, 6,
            ]

reag_id_size = len(reag_id)
_objects = s.query(Department).all()
departments = [u.__dict__ for u in _objects]

#           1  2   3   4   5   6  7  8  9  10
super_id = [9, 9,  9,  9,  9,  9, 9, 9, 9, 9,
            9, 9,  9,  9,  9,  9, 9, 9, 9, 9,
            9, 9,  9,  9,  9,  9, 9, 9, 9, 9,
            9, 10, 10, 10, 10, 1, 1, 1, 1, 1,
           ]
#             1  2  3  4  5  6  7  8  9  10
product_id = [1, 2, 4, 8, 1, 7, 3, 6, 5, 10,
              2, 6, 4, 4, 7, 7, 7, 7, 7, 7,
              7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
              2, 1, 2, 1, 2, 2, 2, 3, 3, 3,
              ]
grid_id = [1,  2,  3,  4,  5,  6,  7,  8,  9,  10,
           11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
           21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
           31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
           ]  # 試劑存放於不同格位位置

_objects = []
#reag_id_size = len(reag_id)
tt = 0
for x in range(reag_id_size):
    tt = tt+1
    kk = catalogs[x]-1
    #print("kk: ", tt, " ", kk)
    u = Reagent(
        reag_id=reag_id[x],
        reag_name=reag_name[x],
        reag_In_unit=reag_In_unit[x],
        reag_Out_unit=reag_Out_unit[x],
        reag_scale=reag_scale[x],
        # reag_period=reag_period[x],
        reag_stock=reag_stock[x],
        reag_temp=reag_temp[x],
        # reag_catalog=reag_catalog[x],
        catalog_id=departments[kk]['id'],
        # super_id=super_id[x],
        grid_id=grid_id[x]
    )
    _objects.append(u)

s.bulk_save_objects(_objects)

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

reagent_objects = s.query(Reagent).all()
reagents = [u.__dict__ for u in reagent_objects]
i = 1
for reagent in reagents:
    s.query(Reagent).filter(Reagent.id == i).update(
        {"super_id": super_id[i-1],
         "product_id": product_id[i-1]
         })
    i = i+1

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

s.close()

#print("insert " + str(temp_grid_size) + " grid data is ok...")
print("insert 10 supplier data is ok...")
print("insert 10 product data is ok...")
print("insert 14+16 reagent data is ok...")
