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
    choice = int(input("Enter your choice"))

    if(choice)==1:
          inventory()

    db.close
    print db


def inventory():
    os.system('cls')
    print ("Welcome to inventory")
    print ("1. Add item")
    print ("2. Remove item")
    print ("3. View Items")

    choice = int(input("Enter your Choice"))

    if(choice)==1:
        additem()
    if(choice)==2:
        deleteitem()
    if(choice)==3:
        viewitem()

def deleteitem():
    os.system('cls')
    try:
        slno = int(input("Enter the SL.NO of item that needs to be delete"))
        sql="select * from itemdetails where slno=%d" %slno
        print sql
        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        for row in data:
            slno = row[0]
            itemname = row[1]
            price = row[2]
            quantity = row[3]
            expdate = str(row[4])
            gst = row[5]
            total = row[6]
            print("---------------------------------------------------------------")
            print("Sl NO |  ItemName  |  Price  |  Quantity  |\tExpdate\t|GST|Total")
            print("---------------------------------------------------------------")
            print slno,"      " , itemname,"        ", price,"     ", quantity,"     ", expdate,"   ", gst,"   ", total 
            print ("Are you sure you want to delete the following item??")
            choice = raw_input("Enter your choice Y/N")
            if choice=='Y' or choice == 'y':
                sql = "delete from itemdetails where slno=%d" %slno
                cursor.execute(sql)
                db.commit()
                print "Item " ,itemname, " has been deleted from the inventory"

            else:
                break
            inventory()


    except MySQLdb.Error,e:
        print e
        db.rollback()
        
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
                print("Item is inserted into db")
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
             Inventory()
   
def viewitem():
        sql="select * from itemdetails"
        print sql
        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        print("---------------------------------------------------------------")
        print("Sl NO |  ItemName  |  Price  |  Quantity  |\tExpdate\t|GST|Total")
        print("---------------------------------------------------------------")
        for row in data:
            slno = row[0]
            itemname = row[1]
            price = row[2]
            quantity = row[3]
            expdate = str(row[4])
            gst = row[5]
            total = row[6]
          
            print slno,"      " , itemname,"        ", price,"     ", quantity,"     ", expdate,"   ", gst,"   ", total 
           
        choice = raw_input("Go back to inventory?Y/N")
        if choice == 'Y' or choice == 'y':
            inventory()


if __name__ == '__main__':
        main()
