import psycopg2
import random
import sys
import os
from datetime import datetime
os.system('CLS')
class store_connection:
    def __init__(self):
        self.con = psycopg2.connect(
            host = "localhost",
            database = "clearelise",
            user = "postgres",
            password="4221")
        self.cur = self.con.cursor()
        self.cur.execute("select * from information_schema.tables where table_name=%s", ('_user',))
        user_exists = bool(self.cur.rowcount)
        if(not(user_exists)):
            self.cur.execute("create table _user (id_user BIGSERIAL PRIMARY KEY NOT NULL, date_create DATE NOT NULL, date_update DATE NOT NULL, fio varchar(150) NOT NULL, address varchar(100) not null, email varchar(50) not null, telephone varchar(20) not null)")
        self.cur.execute("SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_NAME= %s", ("unique_id",))
        unique_id_exists = self.cur.fetchone() 
        if(not(unique_id_exists)):
            self.cur.execute("ALTER TABLE _user add constraint unique_id UNIQUE (id_user)")
        self.cur.execute("SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_NAME= %s", ("name",))
        unique_name_exists = self.cur.fetchone()
        if(not(unique_name_exists)):
            self.cur.execute("ALTER TABLE _user add constraint name UNIQUE (fio)")
        
        self.cur.execute("select * from information_schema.tables where table_name=%s", ('_product',))
        product_exists = bool(self.cur.rowcount)
        if(not(product_exists)):
            self.cur.execute("create table _product (id_product BIGSERIAL PRIMARY KEY NOT NULL, name varchar(50) NOT NULL, description varchar(500) NOT NULL, description_short varchar(200) NOT NULL, visibility varchar(30) NOT NULL, date_create date NOT NULL, date_update date not null)")
        self.cur.execute("SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_NAME= %s", ("unique_id_product",))
        unique_id_product = self.cur.fetchone()
        if(not(unique_id_product)):
            self.cur.execute("ALTER TABLE _product add constraint unique_id_product UNIQUE (id_product)")

        self.cur.execute("select * from information_schema.tables where table_name=%s", ('_order',))
        order_exists = bool(self.cur.rowcount)
        if(not(order_exists)):
            self.cur.execute("create table _order (id_order BIGSERIAL PRIMARY KEY NOT NULL, id_user integer references _user (id_user) not null, date_create date not null, delivery_way varchar(30) not null, payment_way varchar(30))")
        self.cur.execute("SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_NAME= %s", ("unique_id_order",))
        unique_id_order = self.cur.fetchone()
        if(not(unique_id_order)):
            self.cur.execute("ALTER TABLE _order add constraint unique_id_order UNIQUE (id_order)")
        
        self.cur.execute("select * from information_schema.tables where table_name=%s", ('_order_row',))
        order_row_exists = bool(self.cur.rowcount)
        if(not(order_row_exists)):
            self.cur.execute("create table _order_row (id_order integer references _order (id_order), id_product integer references _product (id_product))")
        self.rows = 1000
        self.con.commit()
    def remove_all_users(self):
        self.cur.execute("TRUNCATE _user CASCADE")
        self.con.commit()
    def remove_all_product(self):
        self.cur.execute("TRUNCATE _product CASCADE")
        self.con.commit()
    def diconnect(self):
        self.cur.close()
        self.con.close()
    def fio_gen(self):
            k = random.randint(3, 12)
            fio = ""
            for i in range(k):
                    if(i==0):
                            fio = fio + chr(random.randint(65, 91))
                    else:
                            fio = fio + chr(random.randint(97, 122))
            fio = fio + " "
            k = random.randint(3, 10)
            for i in range(k):
                    if(i==0):
                            fio = fio + chr(random.randint(65, 91))
                    else:
                            fio = fio + chr(random.randint(97, 122))

            fio = fio + " "
            k = random.randint(3, 10)
            for i in range(k):
                    if(i==0):
                            fio = fio + chr(random.randint(65, 91))
                    else:
                            fio = fio + chr(random.randint(97, 122))
            return fio

    def date_create_gen(self):
            year = random.randint(2014, 2020)
            months = random.randint(1, 12)
            if(months ==2):
                day = random.randint(1, 28)
            else:
                day = random.randint(1, 30)
            if(months//10 == 0):
                if(day//10 == 0):
                    returning = str(year) + "-" + "0" + str(months) + "-" + "0" + str(day)
                else:
                    returning = str(year) + "-" + "0" + str(months) + "-" + str(day)
            else:
                if(day//10 == 0):
                    returning = str(year) + "-" + str(months) + "-" + "0" +  str(day)
                else:
                    returning = str(year) + "-" + str(months) + "-" + str(day)

                        
            return returning


    def date_update_gen(self, date_create):
                year_created = 0
                for i in range(4):
                        year_created = year_created + int(date_create[i]) * 10 **(3-i)
                if(year_created == 2020):
                    year_update = 2020
                else:
                    year_update = random.randint(year_created, 2020)
                months_created = 0
                for i in range(2):
                        months_created = months_created + int(date_create[i+5]) * 10 **(1-i)
                if(months_created == 12):
                    months_update = 12
                else:
                    months_update = random.randint(months_created, 12)
                day_created = 0
                for i in range(2):
                        day_created = day_created + int(date_create[i+8]) * 10 **(1-i)
                if(months_update==2):
                    if(day_created >= 28):
                        months_update +=1
                        day_update = random.randint(day_created, 30)
                    else:
                        day_update = random.randint(day_created, 28)
                else:
                    if(day_created == 30):
                        day_update = 30
                    else:
                        day_update = random.randint(day_created, 30)
                

                if(months_update//10 == 0):
                        if(day_update//10 == 0):
                                returning = str(year_update) + "-" + "0" + str(months_update) + "-" + "0" + str(day_update)
                        else:
                                returning = str(year_update) + "-" + "0" + str(months_update) + "-" + str(day_update)
                else:
                        if(day_update//10 == 0):
                                returning = str(year_update) + "-" + str(months_update) + "-" + "0" +  str(day_update)
                        else:
                                returning = str(year_update) + "-" + str(months_update) + "-" + str(day_update)    
                return returning
    def address_gen(self):
        address = ""
        index = random.randint(100000, 999999)
        address = str(index) + ", "
        street_n = random.randint(6, 12)
        for i in range(street_n):
            if(i==0):
                address = address + chr(random.randint(65, 91))
            address = address + chr(random.randint(97, 122))
        house_n = random.randint(1, 49)
        address = address + ", "
        address = address + str(house_n)
        return address
              
    def email_gen(self):
        email = ""
        name_n = 4
        for i in range(name_n):
            email = email + chr(random.randint(97, 122))
            email = email + "@"
            platform_n = random.randint(1, 3)
        for i in range(platform_n):
            email = email + chr(random.randint(97, 122))
        email = email + "mail.com"
        return email
    def telephone_gen(self):
        number = ""
        current_number = random.randint(100, 999)
        number = number + "("+str(current_number)+")"+"-"
        current_number = random.randint(100, 999)
        number = number +str(current_number)+ "-"
        current_number = random.randint(10, 99)
        number = number + str(current_number) + "-"
        current_number = random.randint(10, 99)
        number =  number + str(current_number) 
        return number
    def payment_way_gen(self):
        payment_ways = ["online", "cash"]
        return payment_ways[random.randint(0,1)]
    def delivery_way_gen(self):
        delivery_ways = ["to home", "pickup"]
        return delivery_ways[random.randint(0,1)]
    def description_gen(self):
        description = ""
        new_sentence = True
        new_word = False 
        word_end = random.randint(4, 8)
        sentence_end = random.randint(30, 50)
        i=0
        while(i<490):
            if(i == 489):
                description = description + "."
                i+=1
            else:
                if(i%word_end == 0):
                    description = description + " "
                    new_word = True
                    i+=1
                if(i%sentence_end == 0 and not(new_word)):
                    description = description + ". "
                    new_sentence = True
                    i+=2    
                if(new_sentence):
                    description = description + chr(random.randint(65, 91))
                    new_sentence = False   
                    i+=1
                description = description + chr(random.randint(97, 122))
                new_word = False   
                word_end = random.randint(4, 8)      
                i+=1
        return description
    def description_short_gen(self):
        description = ""
        new_sentence = True
        new_word = False 
        word_end = random.randint(4, 8)
        sentence_end = random.randint(30, 50)
        i=0
        while(i<190):
            if(i == 189):
                description = description + "."
                i+=1
            else:
                if(i%word_end == 0):
                    description = description + " "
                    new_word = True
                    i+=1
                if(i%sentence_end == 0 and not(new_word)):
                    description = description + ". "
                    new_sentence = True
                    i+=2
                if(new_sentence):
                    description = description + chr(random.randint(65, 91))
                    new_sentence = False
                description = description + chr(random.randint(97, 122))
                new_word = False
                word_end = random.randint(4, 8)
                i+=1
        return description
    def name_gen(self):
        two_words = random.randint(0, 1)
        if(two_words == 0):
            word_1 = ""
            word_1_n = random.randint(6, 12)
            for i in range(word_1_n):
                if(i==0):
                    word_1 = word_1 + chr(random.randint(65, 91))
                else:
                    word_1 = word_1 + chr(random.randint(97, 122))
            return word_1
        else:
            name = ""
            word_1 = ""
            word_2 = ""
            word_1_n = random.randint(6, 12)
            word_2_n = random.randint(6, 12)
            for i in range(word_1_n):
                if(i==0):
                    word_1 = word_1 + chr(random.randint(65, 91))
                else:
                    word_1 = word_1 + chr(random.randint(97, 122))
            for i in range(word_2_n):
                if(i==0):
                    word_2 = word_2 + chr(random.randint(65, 91))
                else:
                    word_2 = word_2 + chr(random.randint(97, 122))
                name = word_1 + " " + word_2
            return name

    def visibility_gen(self):
        visibilities = ["visible", "invisible"]
        return visibilities[random.randint(0, 1)]

    def insert_into_user(self):
        for i in range(self.rows):
            date_created = self.date_create_gen()
            date_updated = self.date_update_gen(date_created)
            fio = self.fio_gen()                        
            address = self.address_gen()
            email = self.email_gen()
            phone_number = self.telephone_gen()
            self.cur.execute("insert into _user (date_create, date_update, fio, address, email, telephone) values (%s, %s, %s, %s, %s, %s)", (date_created, date_updated, fio, address, email, phone_number))
        self.con.commit()
    def insert_into_product(self):
        for i in range(self.rows):
            product_name = self.name_gen()
            
            descrtiption = self.description_gen()
            
            descrtiption_short = self.description_short_gen() 
                                      ### ЗАКОММЕНТИЛ INSERT 1000 СТРОК В _PRODUCT
            visibility = self.visibility_gen()      
            product_created = self.date_create_gen()
            product_updated = self.date_update_gen(product_created)
            
            self.cur.execute("insert into _product (name, description, description_short, visibility, date_create, date_update) values (%s, %s, %s, %s, %s, %s)", (product_name, descrtiption, descrtiption_short, visibility, product_created, product_updated))
        self.con.commit()
    def user_random_rows(self, rows):
        for i in range(rows):
            self.cur.execute("select id_user, fio from _user ORDER BY random() limit 1")         ### ВЫВОД 20-ти случайных пользователей
            rows_of_user = self.cur.fetchone()
            print(str(rows_of_user[0]) +"\t" + str(rows_of_user[1]))
    def product_random_rows(self, rows):
        for i in range(rows):
            self.cur.execute("select id_product, name from _product ORDER BY random() limit 1")         ### ВЫВОД 20-ти случайных товаров
            rows_of_product = self.cur.fetchone()
            print(str(rows_of_product[0]) +"\t" + str(rows_of_product[1]))
    def make_order(self):
        print("Введите ваше ФИО: ")
        user_name = "'"
        user_name = user_name + input()
        user_name =  user_name + "'"
        self.cur.execute("select id_user, fio from _user where fio = "+user_name)
        user_info = self.cur.fetchone()
        print(user_info[0], user_info[1], "- Пользователь найден")
        print("Вам удобнее оплатить онлайн или наличными? Напишите <online> или <cash> соответственно: ")
        payment_info = input()
        print("Вам удобнее получить заказ дома или в пункте самовывоза? Напишите <to home> или <pickup> соответственно: ")
        delivery_info = input()
        date_create = datetime.now()
        date_create = str(date_create)
        self.cur.execute("insert into _order (id_user, date_create, delivery_way, payment_way) values (%s, %s, %s, %s)",(user_info[0], date_create, delivery_info, payment_info))
        cmd = "'"
        cmd = cmd + date_create
        cmd = cmd + "'"
        self.cur.execute("select id_order from _order order by id_order desc limit 1 ")
        order_id = self.cur.fetchone()
        #self.cur.commit()
        print("Сколько вещей вы собираетесь приобрести?")
        count = int(input())
        for i in range(count):
            print("Введите имя продукта: ")
            product_name = "'"
            product_name = product_name + input()
            product_name = product_name + "'"
            self.cur.execute("select id_product from _product where name = "+product_name)
            product_id = self.cur.fetchone()
            self.cur.execute("insert into _order_row (id_order, id_product) values (%s, %s)", (order_id[0], product_id[0]))
        self.cur.execute("select id_product from _order_row order by id_order desc limit %s", (count,))  
        products = self.cur.fetchmany(count)
        word = ""
        if(count > 1 and count < 5):
            word = "продукта "
        else: 
            word = "продуктов "
        if(count == 1):
            print("Следующий продукт был добавлен в корзину")
        else:
            print("Следющие", count, word+ "были добавлены в корзину")
        for i in range(count):
            print(products[i][0])
        self.con.commit()
        
    
A = store_connection()

#A.remove_all_product()
#A.remove_all_users()

#A.insert_into_product()
#A.insert_into_user()

A.product_random_rows(5)
print("______________________")
A.user_random_rows(5)


A.make_order()


A.diconnect()