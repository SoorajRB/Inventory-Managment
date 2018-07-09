import MySQLdb
import os
import time
servername = "localhost"
username = "root"
password = ""
db = "prema groc"
db = MySQLdb.connect(servername,username,password,db)
cursor = db.cursor()



def main():
    os.system('cls')
    print("1. Inventory")
    print("2. Billing")
    choice = int(input("Enter your choice"))


    if(choice)==1:
          inventory()
    if(choice)==2:
           billing()

    db.close()
    print db
   

def billing():
    os.system('cls')
    print ("Welcome to Billing")
    print ("1.Start new billing")
    choice = int(input("Enter your choice"))

    if(choice)==1:
        newbill()

def newbill():
    os.system('cls')
    billviewitem()
    additembill()

def additembill():
    slno = int(input("Enter the Serial No. of Item that needs to be added"))
    qnt = float(input("Enter the quantity of the item"))
    
    try:
        sql = "select * from itemdetails where slno = %d" %slno
        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        
        for i in range(0,len(data)):
            total = data[i][6]
            gttotal = total * qnt
            sql = "insert into custitems (slno,itemname,Price,Quantity,ExpiryDate,GST,Total,ItemNumber) values (%d,'%s',%d,%d,'%s',%d,%d)" % data[i][0],data[i][1],data[i][2],qnt,data[i][4],data[i][5],gttotal,
            cursor.execute(sql)
            db.commit()
                   
    except MySQLdb.Error, e:
        print e
        db.rollback()

    choice = int(input("Next Items?Y/N"))
    if choice=='Y' or choice=='y':
        additembill()



def billviewitem():
   
    try:
        sql = "select * from itemdetails"
        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        print("------------------")
        print("Sl NO |  ItemName |")
        print("------------------")
        l = len(data)
        for i in range(0,l):
           print  data[i][0], "\t "  , data[i][1]
    except MySQLdb.Error,e:
        print e

def inventory():
    os.system('cls')
    print ("Welcome to inventory")
    print ("1. Add item")
    print ("2. Remove item")
    print ("3. View Items")
    print ("4. Edit items")
    print ("5. Back to Main Menu")

    choice = int(input("Enter your Choice"))

    if(choice)==1:
        additem()
    if(choice)==2:
        deleteitem()
    if(choice)==3:
        viewitem()
    if(choice)==4:
        edititem()
    if(choice)==4:
        main()

def edititem():
    os.system('cls')
    billviewitem()
    slno = int(input("Enter the sl no. of item that needs to be edited:"))
    sql="select * from itemdetails where slno = %d" %slno
    cursor.execute(sql)
    db.commit()
    data = cursor.fetchall()
    print("----------------------------------------------------------------------------------------------")
    print("Sl NO |  ItemName  |  Price  |  Quantity  |\tExpdate\t\t|\tGST\t|\tTotal|")
    print("----------------------------------------------------------------------------------------------")
    l = len(data)
    for i in range(0,l):
        print  data[i][0], "\t "  , data[i][1], "\t"  , data[i][2], "\t"  , data[i][3], "\t\t"  , data[i][4], "\t\t" , data[i][5], "\t\t"  , data[i][6]   
     
    print("1. Item Name")
    print("2. Price")
    print("3. Quantity")
    print("4. Expiry date")
    print("5. GST")
    choice = int(input("What feild would you like to edit?:"))

    if choice == 1:
        newitemname(slno)

    if choice == 2:
        newitemprice(slno)  
        
    if choice == 3:
        newitemquantity(slno)

    if choice == 4:
        newitemexpdate(slno)

def newitemexpdate(slno):
       print(slno)
       newexpydate = raw_input("Enter the new item quantity:")
       try:
           sql = "Update itemdetails set Price = %d where slno=%d" % newquantity,slno
           print(sql)
           cursor.execute(sql)
           db.commit()
           sql="select * from itemdetails where slno = %d" %slno
           cursor.execute(sql)
           db.commit()
           data = cursor.fetchall()
           os.system('cls')
           print("----------------------------------------------------------------------------------------------")
           print("Sl NO |  ItemName  |  Price  |  Quantity  |\tExpdate\t\t|\tGST\t|\tTotal|")
           print("----------------------------------------------------------------------------------------------")
           l = len(data)
           for i in range(0,l):
               print  data[i][0], "\t "  , data[i][1], "\t"  , data[i][2], "\t"  , data[i][3], "\t\t"  , data[i][4], "\t\t" , data[i][5], "\t\t"  , data[i][6]
       except MySQLdb.Error,e:
            print e
            db.rollback()

def newitemquantity(slno):
       print(slno)
       newquantity = raw_input("Enter the new item quantity:")
       try:
           sql = "Update itemdetails set Price = %d where slno=%d" % newquantity,slno
           print(sql)
           cursor.execute(sql)
           db.commit()
           sql="select * from itemdetails where slno = %d" %slno
           cursor.execute(sql)
           db.commit()
           data = cursor.fetchall()
           os.system('cls')
           print("----------------------------------------------------------------------------------------------")
           print("Sl NO |  ItemName  |  Price  |  Quantity  |\tExpdate\t\t|\tGST\t|\tTotal|")
           print("----------------------------------------------------------------------------------------------")
           l = len(data)
           for i in range(0,l):
               print  data[i][0], "\t "  , data[i][1], "\t"  , data[i][2], "\t"  , data[i][3], "\t\t"  , data[i][4], "\t\t" , data[i][5], "\t\t"  , data[i][6]
       except MySQLdb.Error,e:
            print e
            db.rollback()
        


def newitemprice(slno):
       print(slno)
       newprice = float(input("Enter the new item Price:"))
       try:
           sql = "Update itemdetails set Price = {0} where slno= {1}" .format(newprice,slno)
           print(sql)
           cursor.execute(sql)
           db.commit()
           sql="select * from itemdetails where slno = %d" %slno
           cursor.execute(sql)
           db.commit()
           data = cursor.fetchall()
           os.system('cls')
           print("----------------------------------------------------------------------------------------------")
           print("Sl NO |  ItemName  |  Price  |  Quantity  |\tExpdate\t\t|\tGST\t|\tTotal|")
           print("----------------------------------------------------------------------------------------------")
           l = len(data)
           newprice = (newprice*(data[0][5]/100))+newprice
           print newprice
           for i in range(0,l):
               print  data[i][0], "\t "  , data[i][1], "\t"  , data[i][2], "\t"  , data[i][3], "\t\t"  , data[i][4], "\t\t" , data[i][5], "\t\t"  , newprice
       except MySQLdb.Error,e:
            print(sql)
            print e
            db.rollback()



def newitemname(slno):
       print(slno)
       newitemname = raw_input("Enter the new item Name:")
       try:
           sql = "Update itemdetails set itemname = '%s' where slno=%d" % newitemname,slno
           print(sql)
           cursor.execute(sql)
           db.commit()
           sql="select * from itemdetails where slno = %d" %slno
           cursor.execute(sql)
           db.commit()
           data = cursor.fetchall()
           os.system('cls')
           print("----------------------------------------------------------------------------------------------")
           print("Sl NO |  ItemName  |  Price  |  Quantity  |\tExpdate\t\t|\tGST\t|\tTotal|")
           print("----------------------------------------------------------------------------------------------")
           l = len(data)
           for i in range(0,l):
               print  data[i][0], "\t "  , data[i][1], "\t"  , data[i][2], "\t"  , data[i][3], "\t\t"  , data[i][4], "\t\t" , data[i][5], "\t\t"  , data[i][6]
       except MySQLdb.Error,e:
            print e
            db.rollback()



def deleteitem():
    os.system('cls')
    try:
        slno = int(input("Enter the SL.NO of item that needs to be delete"))
        sql="select * from itemdetails where slno=%d" %slno
        
        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        print("----------------------------------------------------------------------------------------------")
        print("Sl NO |  ItemName  |  Price  |  Quantity  |\tExpdate\t\t|\tGST\t|\tTotal|")
        print("----------------------------------------------------------------------------------------------")
        l = len(data)
        
        for i in range(0,l):
           print  data[i][0], "\t "  , data[i][1], "\t"  , data[i][2], "\t"  , data[i][3], "\t\t"  , data[i][4], "\t\t" , data[i][5], "\t\t"  , data[i][6]
           print ("Are you sure you want to delete the following item??")
           choice = raw_input("Enter your choice Y/N")
           if choice=='Y' or choice == 'y':
                    sql = "delete from itemdetails where slno=%d" %slno
                    cursor.execute(sql)
                    db.commit()
                    print "Item has been deleted from the inventory"
                    time.sleep(3)
                    inventory()
           else:
                break
                inventory()


    except MySQLdb.Error,e:
        print e
        db.rollback()
    inventory()
  
    

def additem():
    
    while(1):
        try:
            os.system('cls')
            slno = int(input("Enter the Serial Number: "))
            itemname = raw_input("Enter the itemname: ")
            price = float(input("Enter the price: "))
            quantity = int(input("Enter the quantity: "))
            expdate = raw_input("Enter the date YYYY-MM-DD: ")
            GST = float(input("Enter the GST Rate: "))

            total = (price * GST/100) + price

            sql = 'Insert into itemdetails (slno,itemname,price,quantity,ExpiryDate,GST,total) values (%d,"%s",%f,%d,"%s",%f,%f)' % (slno,itemname,price,quantity,expdate,GST,total) 

            try:
                cursor.execute(sql)
                db.commit()
                print("Item is inserted into inventory")
            except MySQLdb.Error,e:
                print e
                db.rollback()
        
            choice = raw_input("Add next item?Y/N")
            if choice=='y' or choice=='Y':
                additem()
            else: 
                for i in range (0,3):
                    print("Returning to inventory in...", i)
                    time.sleep(1)
                    inventory()
        except Exception, e:
             print e
             inventory()
   


def viewitem():
       os.system('cls')
       try:
            sql="select * from itemdetails"
       
            cursor.execute(sql)
            db.commit()
            data = cursor.fetchall()
            print("----------------------------------------------------------------------------------------------")
            print("Sl NO |  ItemName  |  Price  |  Quantity  |\tExpdate\t\t|\tGST\t|\tTotal|")
            print("----------------------------------------------------------------------------------------------")
            l = len(data)
            for i in range(0,l):
               print  data[i][0], "\t "  , data[i][1], "\t"  , data[i][2], "\t"  , data[i][3], "\t\t"  , data[i][4], "\t\t" , data[i][5], "\t\t"  , data[i][6]
           
            choice = raw_input("Go back to inventory?Y/N")
            if choice == 'Y' or choice == 'y':
                inventory()
            else:
                viewitem()
       except MySQLdb.Error,e:
            print e
            db.rollback()





if __name__ == '__main__':
        main()
            

        