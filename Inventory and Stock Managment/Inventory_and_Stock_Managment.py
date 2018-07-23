import MySQLdb
import os
import time
servername = "localhost"
username = "root"
password = ""
db = "prema groc"
db = MySQLdb.connect(servername,username,password,db)
cursor = db.cursor()
itemnumber = 0





def main():
    os.system('cls')
    print("1. Inventory")
    print("2. Billing")
    choice = int(input("Enter your choice"))


    if(choice)==1:
          inventory()
    if(choice)==2:
           billing()

    
   
   

def billing():
    os.system('cls')
    print ("Welcome to Billing")
    print ("1. Start new billing")
    print ("2. Continue Billing")
    print ("3. Checkout")
    choice = int(input("Enter your choice"))

    if(choice)==1:
        newbill()
    if(choice)==2:
        contbill()
    if(choice)==3:
        checkout()

def checkout():
    os.system('cls')
    viewcustomeritems()
    calgrandtotal()
    print("1. Cash")
    print("2. Card")
    choice = int(input("Enter your choice"))
    if choice== 1:
        cash()
    if choice == 2:
        card()

def dailyupdate():
     try:
          sql="select * from custitems"
          cursor.execute(sql)
          db.commit()
          data = cursor.fetchall()
          for i in range(0,len(data)):
              cqt = data[i][0]
              sql = "update itemdetails set Quantity = Quantity - (select Quantity from custitems where slno = %d) where slno = %d" %(cqt,cqt)
              cursor.execute(sql)
              db.commit()
              sql = "delete from custitems where slno = %d" %(cqt)
              cursor.execute(sql)
              db.commit()
              
     except MySQLdb.Error,e:
        print e

def cash():
    customeramount = float(input("Enter the cash amount from customer"))
    gt = calgrandtotal()
    balance = customeramount - gt
    print "The balance amount to return to customer is :%f " % balance
    if(balance < 0):
        print "Error not enough Cash given going back to checkout"
        time.sleep(3)
        checkout()
    else:
        dailyupdate()
        removecustitems()
        billing()


    
def removecustitems():
      try:
        sql = "Delete from custitems"
        cursor.execute(sql)
        db.commit()
      except MySQLdb.Error,e:
        print e


def card():
    choice = raw_input("Was transaction success full?Y/N")
    if choice == 'y' or choice == 'Y':
        removecustitems()
        main()
    else:
        checkout()

def newbill():
    os.system('cls')
    sql = "select count(*) from custitems"
    cursor.execute(sql)
    db.commit()
    data = cursor.fetchall()
    if(data[0][0] != 0):
        choice = raw_input("Warning customer bill already exisit and hasnt checkedout! Continue? Y/N")
        if choice == 'Y' or choice == 'y':
            sql = "Delete from custitems"
            cursor.execute(sql)
            db.commit()
            billviewitem()
            additembill()
        elif choice == 'N' or choice == 'n':
            billing()
      
    os.system('cls')
    billviewitem()
    additembill()
     
    

def contbill():
    os.system('cls')
    billviewitem()
    additembill()


def additembill():
  
    sql="select max(itemnumber) from custitems"
    cursor.execute(sql)
    db.commit()
    data = cursor.fetchall()
    itemnumber = data[0][0]
    if(itemnumber == 0 or itemnumber == None):
        itemnumber = 1
    else:
        itemnumber +=1
    
    slno = int(input("Enter the Serial No. of Item that needs to be added: "))
    qnt = float(input("Enter the quantity of the item: "))
    try:
        sql = "select count(*) from custitems where slno = %d" %slno
        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        count = data[0][0]
        if(count == 1):
            print qnt
            sql = "update custitems set quantity = quantity + %d where slno = %d" %(qnt,slno)
            cursor.execute(sql)
            db.commit()
            sql = "select quantity from custitems where slno = %d" %(slno)
            cursor.execute(sql)
            db.commit()
            data = cursor.fetchall()
            qnt = data[0][0]
            sql = "select * from itemdetails where slno = %d" %slno
            cursor.execute(sql)
            db.commit()
            data = cursor.fetchall()
            total = data[0][6]
            gttotal = total * qnt
            sql = "update custitems set total = %f where slno = %d" % (gttotal,slno)
            cursor.execute(sql)
            db.commit()
            print sql
       
        if (count == 0):
                sql = "select * from itemdetails where slno = %d" %slno
                cursor.execute(sql)
                db.commit()
                data = cursor.fetchall()
                total = data[0][6]
                gttotal = total * qnt
                sql = "insert into custitems (slno,itemname,Price,Quantity,ExpiryDate,GST,Total,ItemNumber) values (%d,'%s',%f,%f,'%s',%f,%f,%d)" % (data[0][0],data[0][1],data[0][2],qnt,data[0][4],data[0][5],gttotal,itemnumber)
                cursor.execute(sql)
                db.commit()
                  
    except MySQLdb.Error, e:
        print e
        db.rollback()
        additembill()
    viewcustomeritems()
    calgrandtotal()
    choice = raw_input("\nNext Items?Y/N")
    if choice=='Y' or choice=='y':
       additembill()
    else:
        billing()

    

def calgrandtotal():
    try:
        sql = "select sum(total) from custitems"
        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        grandtotal = data[0][0]
        print "Grand Total is " , grandtotal
        return grandtotal
    except MySQLdb.Error(),e:
        print e


def viewcustomeritems():
     try:
            sql="select * from custitems"
       
            cursor.execute(sql)
            db.commit()
            data = cursor.fetchall()
            print("----------------------------------------------------------------------------------------------")
            print("Item Number| \tSl NO |  ItemName  |  Price  |  Quantity  |\tExpdate\t\t|\tGST\t|\tTotal|")
            print("----------------------------------------------------------------------------------------------")
            l = len(data)
            for i in range(0,l):
               print data[i][7],"\t\t " ,data[i][0], "\t "  , data[i][1], "\t"  , data[i][2], "\t"  , data[i][3], "\t\t"  , data[i][4], "\t\t" , data[i][5], "\t\t"  , data[i][6], "\t\t" ,
               
     except MySQLdb.Error,e:
            print e
            db.rollback()

     

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
###############################################################
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
    if(choice)==5:
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
        print "\n", data[i][0], "\t "  , data[i][1], "\t"  , data[i][2], "\t"  , data[i][3], "\t\t"  , data[i][4], "\t\t" , data[i][5], "\t\t"  , data[i][6]   
     
    print("1. Item Name")
    print("2. Price")
    print("3. Quantity")
    print("4. Expiry date")
    print("5. GST")
    print("6. Go Back")
    choice = int(input("What field would you like to edit?:"))

    if choice == 1:
        newitemname(slno)
    if choice == 2:
        newitemprice(slno)  
    if choice == 3:
        newitemquantity(slno)
    if choice == 4:
        newitemexpdate(slno)
    if choice == 5:
        newitemGST(slno)
    if choice == 6:
        inventory()

def newitemGST(slno):
       print(slno)
       newgst = float(input("Enter the new item GST:"))
       try:
           sql = "Update itemdetails set GST = %f where slno=%d" % (newgst,slno)
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
           newprice = (data[0][2]*(newgst/100))+data[0][2]
           print(newprice)
           time.sleep(5)
           sql = "update itemdetails set Total = %f where slno =%d" %(newprice,slno)
           cursor.execute(sql)
           db.commit()
           print newprice
           for i in range(0,l):
               print  data[i][0], "\t "  , data[i][1], "\t"  , data[i][2], "\t"  , data[i][3], "\t\t"  , data[i][4], "\t\t" , data[i][5], "\t\t"  , data[i][6]
       except MySQLdb.Error,e:
            print e
            db.rollback()
       time.sleep(3)
       inventory()

def newitemexpdate(slno):
       print(slno)
       newexpydate = raw_input("Enter the new item expiry date YYYY-MM-DD:")
       try:
           sql = "Update itemdetails set ExpiryDate = '%s' where slno=%d" % (newexpydate,slno)
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
       time.sleep(3)
       inventory()

def newitemquantity(slno):
       print(slno)
       newquantity = float(input("Enter the new item quantity:"))
       try:
           sql = "Update itemdetails set Quantity = %d where slno=%d" % (newquantity,slno)
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
       time.sleep(3)
       inventory()
        
def newitemprice(slno):
       print(slno)
       newprice = float(input("Enter the new item Price:"))
       try:
           sql = "Update itemdetails set Price = %d where slno= %d" %(newprice,slno)
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
           sql = "update itemdetails set Total = %f where slno =%d" %(newprice,slno)
           cursor.execute(sql)
           db.commit()
           for i in range(0,l):
               print  data[i][0], "\t "  , data[i][1], "\t"  , data[i][2], "\t"  , data[i][3], "\t\t"  , data[i][4], "\t\t" , data[i][5], "\t\t"  , newprice
       except MySQLdb.Error,e:
            print(sql)
            print e
            db.rollback()
       time.sleep(3)
       inventory()

def newitemname(slno):
       print(slno)
       newitemname = raw_input("Enter the new item Name:")
       try:
           sql = "Update itemdetails set itemname = '%s' where slno=%d" % (newitemname,slno)
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
       time.sleep(3)
       inventory()

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
            

        