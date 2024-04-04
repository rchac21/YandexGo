import random
import os

class YandexGo:
    user_id = 0
    users = []
    current_calls = {} # economy : [], comfort : [], business : [];
    current_taxi_drivers = []
    orderer_and_taxi_driver = {} # key : orderer , value : taxi_driver
    distances = {}  # key : orderer , value : distance
    service_types = ['Economy','Comfort','Business']

    def __init__(self):
        self.Declare_Service_Types()
        self.Take_Data()

    def __repr__(self):
        return str(self.users)
    
    # add user in users list.
    def add_user(self, user):
        found = False
        for u in self.users:
            if u.personal_id == user.personal_id or u.phone_num == user.phone_num:
                found = True
                break
        if not found:
            user.set_user_id(self.user_id)
            self.users.append(user)
            self.user_id += 1
        else:
            if u.personal_id == user.personal_id:
                print('User with peronal id: {} already exists'.format(str(user.personal_id)))
            if u.phone_num == user.phone_num:
                print('User with phone number: {} already exists'.format(str(user.phone_num)))
    
    def login_user(self, personal_id):
        for u in self.users:
            if u.personal_id == personal_id:
                return True
        return False
    
    # Returns the user corresponding to the given personal_id.
    def get_user(self, personal_id):
        for u in self.users:
            if u.personal_id == personal_id:
                return u
        return -1
    
    # Deletes the given user from users list.
    def remove_user(self,user):
        self.users.remove(user)
        if user.status == 'orderer':
               if self.Is_user_current(user):
                  self.remove_current_calls(user)
               self.remove_Taxi_Driver_Recieve_Call(user.personal_id)
               self.remove_distance(user.personal_id)
        else:
            if self.Is_user_current(user):
                self.remove_current_taxi_drivers(user)

    # add the given user in current_taxi_drivers list.       
    def add_current_taxi_drivers(self,user):
        if user.personal_id != '':
           self.current_taxi_drivers.append(user)
   
   # remove the given user from current_taxi_drivers list.
    def remove_current_taxi_drivers(self,user):
        self.current_taxi_drivers.remove(user)
    
    # Returns the current drivers.
    def get_current_taxi_drivers(self):
        return self.current_taxi_drivers
    
    # Adds the user to the list of taxi callers.
    def add_current_calls(self,user,service_type):
            if user.personal_id != '':
               self.current_calls[service_type] += [user]
    
    # Remove the user to the list of taxi callers
    def remove_current_calls(self,user):
        service_type = self.get_srvice_type(user)
        list = self.current_calls[service_type]
        list.remove(user)
        self.current_calls[service_type] = list
        
    
    # Return dictionary of current calls.
    def get_current_calls(self):
        return self.current_calls
    
    # Returns the service provided by the corresponding user, 
    # 'Economy' or 'Comfort' or 'Business'.
    def get_srvice_type(self,user):
        for i in self.current_calls:
            for j in self.current_calls[i]:
                if j.personal_id == user.personal_id:
                    return i

    # Returns whether the given user is currently in calls or taxi drivers.               
    def Is_user_current(self,user):
        if user.status == 'orderer':
            current_users = self.get_current_calls()
            for i in current_users:
                for j in current_users[i]:
                    if j.personal_id == user.personal_id:
                        return True
        else:
            current_users = self.get_current_taxi_drivers()
            for i in current_users:
                if i.personal_id == user.personal_id:
                    return True
        return False
    
    # Adds in distance dictionary key - personal_id(orderer) and value - distance. 
    def add_distance(self,personal_id,distance):
        if personal_id != '':
           self.distances[personal_id] = distance
    
    # Returns the distance corresponding to the passed personal_id from distance dictionary.
    def get_distance(self,personal_id):
        return self.distances[personal_id]
    
    def remove_distance(self,personal_id):
        if personal_id in self.distances:
            self.distances.pop(personal_id)
    
    # orderer_and_taxi_driver in this dictionary, the orderer's personal_id,
    # which is a key, and the taxi driver's personal_id, which is a value.
    def set_received_calls(self,taxi_driver_id,orderer_id):
        if taxi_driver_id != '' and orderer_id != '':
           self.orderer_and_taxi_driver[orderer_id] = taxi_driver_id

    # The personal_id of a specific customer is transferred and returns 
    # its value, which is the personal_id of the taxi driver.
    def get_received_call(self,orderer_id):
        return self.orderer_and_taxi_driver[orderer_id]
    
    def remove_Taxi_Driver_Recieve_Call(self,personal_id):
        if personal_id in self.orderer_and_taxi_driver:
           self.orderer_and_taxi_driver.pop(personal_id)
    
    # If the personal_id of a particular orderer is orderer_and_taxi_driver 
    # in this dictionary then it will return true otherwise false.
    def exist_orderer_received_calls(self,orderer_id):
        if orderer_id in self.orderer_and_taxi_driver:
            return True
        return False
    
    # Makes service type declarations.
    def Declare_Service_Types(self):
        for i in self.service_types:
           self.current_calls[i] = []

    # Extracts data from files and writes them to appropriate data types.
    def Take_Data(self):
        self.Take_Users()
        self.Take_Current_Calls()
        self.Take_Current_Taxi_Drivers()
        self.Take_Orderer_And_Taxi_Driver()
        self.Take_Distances()

    # Reads data from the users.txt file and writes it to the users list.
    def Take_Users(self):
        if os.path.getsize("users.txt") != 0:
            name = ''
            personal_id = ''
            phone = ''
            status = ''
            car_series = '' 
            car_num = ''
            car_color = ''
            service_type = ''

            with open("users.txt","r") as file:
                for line in file:
                    i = 6
                    s = line[i:len(line)]
                    name = parse_string(s)

                    i += len(name) + 7
                    s = line[i:len(line)] 
                    personal_id = parse_string(s)

                    i += len(personal_id) + 10
                    s = line[i:len(line)]
                    phone = parse_string(s)

                    i += len(phone) + 11
                    s = line[i:len(line)]
                    status = parse_string(s)

                    if status == 'taxi_driver':
                        i += len(status) + 15
                        s = line[i:len(line)]
                        car_series = parse_string(s)

                        i += len(car_series) + 12
                        s = line[i:len(line)]
                        car_num = parse_string(s)

                        i += len(car_num) + 14
                        s = line[i:len(line)]
                        car_color = parse_string(s)

                        i += len(car_color) + 17
                        s = line[i:len(line)]
                        service_type = parse_string(s)
                    
                    user = User(name,personal_id,phone,status,car_series,car_num,car_color,service_type)
                    self.users.append(user)
                    car_series = '' 
                    car_num = ''
                    car_color = ''
                    service_type = ''
                
    # Reads data from the current_calls.txt file and writes it to the current_calls dictionary.
    def Take_Current_Calls(self):
        if os.path.getsize("current_calls.txt") != 0:
            k = 0
            service_type = ''
            with open("current_calls.txt","r") as file:
                for line in file:
                    k += 1
                    if k == 1:
                      s = line[8 : len(line) - 1]
                      service_type = 'Economy'
                    elif k == 2:
                        s = line[8 : len(line) - 1]
                        service_type = 'Comfort'
                    else:
                      s = line[9 : len(line) - 1]
                      service_type = 'Business'
                    
                    list = get_list(s)
                    for i in list:
                        user = self.get_user(i)
                        if user != -1:
                           self.add_current_calls(user,service_type)

    # Reads data from the current_taxi_drivers.txt file and writes it to the current_taxi_drivers list.
    def Take_Current_Taxi_Drivers(self):
         if os.path.getsize("current_taxi_drivers.txt") != 0:
            with open("current_taxi_drivers.txt","r") as file:
                for line in file:
                    list = get_list(line)
                    for i in list:
                        user = self.get_user(i) 
                        if user != -1:
                           self.add_current_taxi_drivers(user)
    
    # Reads data from the orderer_and_taxi_driver.txt file and 
    # writes it to the current_taxi_drivers dictionary.
    def Take_Orderer_And_Taxi_Driver(self):
        if os.path.getsize("orderer_and_taxi_driver.txt") != 0:
          with open("orderer_and_taxi_driver.txt","r") as file:
              for line in file:
                  if len(line.strip()) != 0:
                    orderer_pers_id = get_pers_id(line)
                    tax_driver_pers_id = line[len(orderer_pers_id)+1:len(line)-1]
                    self.set_received_calls(tax_driver_pers_id,orderer_pers_id)
    
    # Reads data from the distances.txt file and writes 
    # it to the current_taxi_drivers dictionary.
    def Take_Distances(self):
        if os.path.getsize("distances.txt") != 0:
           with open("distances.txt","r") as file:
               for line in file:
                  if len(line.strip()) != 0:
                    orderer_pers_id = get_pers_id(line)
                    v_distance = line[len(orderer_pers_id)+1:len(line)-1]
                    self.add_distance(orderer_pers_id,v_distance)


class User:
    user_id = 0
    status = ''  # orderer or taxi_driver
    name = ''
    personal_id = ''
    phone_num = ''  
    car_series = ''
    car_num = ''
    car_color = ''
    service_type = ''

    def __init__(self, name, personal_id, phone_num, status, car_series, car_num, car_color,service_type):
        self.name = name
        self.personal_id = personal_id
        self.phone_num = phone_num
        self.status = status
        self.car_series = car_series
        self.car_num = car_num
        self.car_color = car_color
        self.service_type = service_type
    
    # Returns a user based on its corresponding characteristics.
    def __repr__(self):
        if self.status == 'orderer':
           return 'Name: ' + self.name + ' - Id: ' + str(self.personal_id) + ' - Phone: ' + str(self.phone_num) + ' - status: ' + self.status
        else:
            return 'Name: ' + self.name + ' - Id: ' + str(self.personal_id) + ' - Phone: ' + str(self.phone_num) + ' - status: ' + self.status + ' - car_series: ' + self.car_series + ' - car_num: ' + self.car_num + ' - car_color: ' + self.car_color + ' - service_type: ' + self.service_type

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_personal_id(self):
        return self.personal_id
    
    def get_status(self):
        return self.status

# Main Function.
def main():
    yandex = YandexGo()
    inside_yandex = True
    while inside_yandex:

        print('Register new user: type 1, \
            Login as a user: type 2, \
            Remove account: type 3, \
            Exit: type 4')
        inp = input("please enter 1 or 2 or 3: ")
        
        if inp == '1':
            Register_user(yandex)
        elif inp == '2':
            Logged_In_User(yandex)
        elif inp == '3':
            Remove_Account(yandex)
        elif inp == '4':
            inside_yandex = False
            Save_Data(yandex)
        else:
            print('Invalid input')

# Reads data from data types and writes to appropriate files.
def Save_Data(yandex):

    Save_Users(yandex)
    Save_Current_Calls(yandex)
    Save_Current_Taxi_Drivers(yandex)
    Save_Orderer_And_Taxi_Driver(yandex)
    Save_Distances(yandex)

# Reads data from the users list and writes it to the users.txt file.
def Save_Users(yandex):
    if len(yandex.users) > 0:
        with open("users.txt","w") as file:
            for user in yandex.users:
               file.write(f"{user.__repr__()} \n")
    else:
        with open("users.txt","w") as file:
            file.write('')

# Reads data from the current_calls dictionary and writes it to the current_calls.txt file.
def Save_Current_Calls(yandex):
    if len(yandex.current_calls) > 0:
        with open("current_calls.txt","w") as file:
            for key in yandex.current_calls:
                s = key + ':'
                for i in yandex.current_calls[key]:
                    s += i.personal_id + ','

                file.write(f'{s} \n')
    else:
        with open("current_calls.txt","w") as file:
            file.write('')

# Reads data from the current_taxi_drivers list and writes it to the current_taxi_drivers.txt file
def Save_Current_Taxi_Drivers(yandex):
    if len(yandex.current_taxi_drivers) > 0:
        with open("current_taxi_drivers.txt","w") as file:
            s = ''
            for i in yandex.current_taxi_drivers:
               s += i.personal_id + ','
            file.write(s)
    else:
        with open("current_taxi_drivers.txt","w") as file:
            file.write('')

# Reads data from the orderer_and_taxi_driver dictionary and 
# writes it to the orderer_and_taxi_driver.txt file.
def Save_Orderer_And_Taxi_Driver(yandex):
    if len(yandex.orderer_and_taxi_driver) > 0:
        with open("orderer_and_taxi_driver.txt","w") as file:
            for key in yandex.orderer_and_taxi_driver:
                s = str(key) + ':' + str(yandex.orderer_and_taxi_driver[key])
                file.write(s + '\n')
    else:
        with open("orderer_and_taxi_driver.txt","w") as file:
            file.write('')

# Reads data from the distances dictionary and 
# writes it to the distances.txt file.
def Save_Distances(yandex):
    if len(yandex.distances) > 0:
        with open("distances.txt","w") as file:
            for key in yandex.distances:
                s = str(key) + ':' + str(yandex.distances[key])
                file.write(s + '\n')
    else:
        with open("distances.txt","w") as file:
            file.write('')

def get_pers_id(s):
    s1 = ''
    for i in s:
        if i == ':':
            break
        s1 += i
    return s1
# The string must be cut from index 0 to the first space encountered.
def parse_string(s):
      k = 0
      for i in s:
        if i == ' ':
           break
        k += 1
      return s[0:k].strip()

# Given the string e.g. 12,2,4, and returns list [12,2,4].
def get_list(s):
    list = []
    s1 = ''
    for i in s:
      if i == ',':
          list.append(s1)
          s1 = ''
      else:
        s1 += i
    return list

# It asks the user to register as a taxi driver or as a customer.
def get_status():
    inside_status = True

    while inside_status:
        print('Register as a taxi driver: type 1, \
              Register as a orderer: type 2')
        inp_status = input("please enter 1 or 2: ")

        if inp_status == '1' or inp_status == '2':
            inside_status = False
            if inp_status == '1':
                inp_status = 'taxi_driver'
            else:
                inp_status = 'orderer'
        else:
            print('Invalid input')

    return inp_status

# Registers the user
def Register_user(yandex):
    inp_status = get_status()
    inp_name = get_name()
    inp_peronal_id = get_personal_id() 
    inp_phone_num = get_phone_num()
    
    car_series = ''
    car_num = ''
    car_color = ''
    service_type = ''
    if inp_status == 'taxi_driver':
        car_series = get_car_series()
        car_num = get_car_num() 
        car_color = get_car_color()
        text = 'Please choose which service you want to work with: '
        service_type = Choice_Service_Type(yandex,'taxi_driver',text)

    user = User(inp_name, inp_peronal_id, inp_phone_num, inp_status, car_series, car_num, car_color,service_type)
    yandex.add_user(user)

def get_name():
    s = 'Enter your name: '
    return(get_func(s))

def get_car_series():
    s = 'Enter your car series: '
    return(get_func(s))

def get_car_num():
    s = 'Enter your car number: '
    return(get_func(s))

def get_car_color():
    s = 'Enter your car color: ' 
    return(get_func(s))

# personal_id will only enter a number eg '01' or 'abs1' is not a number.
def get_personal_id():
    inp = ''
    while True:
       inp = input('Enter your personal id: ')
       if is_number(inp):
           break
       else:
           print('invalid input')
    return inp

# Enter the phone number in the following format:5******** 
# That is, it should start with 5, it should be 9 digits and also a number.
def get_phone_num():
    inp = ''
    while True:
       inp = input('Enter your phone number: ')
       if is_number(inp) and inp[0] == '5' and len(inp) == 9:
           break
       else:
           print('invalid input')
    return inp

def get_func(s):
    inp = ''
    while True:
       inp = input(s).strip()
       if inp != '':
           break
       else:
           print('invalid input')
    return inp

# Checks whether the passed string is a number or not.
def is_number(inp):
    if (len(inp) > 1 and inp[0] == '0') or not inp.isdigit():
        return False
    return True

# Logging the user.
def Logged_In_User(yandex):
    inp_peronal_id = input('Enter your personal id: ')
    if yandex.login_user(inp_peronal_id):
        print('User logged in')
        user = yandex.get_user(inp_peronal_id)
        if user.get_status() == 'orderer':
            Call_Taxi(yandex,user)
        else:
            Work(yandex,user)
    else:
        print('No user was found with this personal ID')

# According to the given process, the user can call a taxi.
def Call_Taxi(yandex,user): 
    if Taxi_Driver_Recieve_Call(yandex,user): 
            Show_Driver_data(yandex,user)
            yandex.remove_Taxi_Driver_Recieve_Call(user.personal_id)
    else:
         if Is_user_current_calls(yandex,user):
            if Continue_Call():
                print("your order received,please wait...")
            else:
                yandex.remove_current_calls(user)
                print("Your call has been cancelled")
         else:
            if Is_call():
                text = "please choice any of them: "
                service_type = Choice_Service_Type(yandex,user.status,text)
                if service_type != 'no call': 
                    yandex.add_current_calls(user,service_type)
                    print("your order received,please wait...")

# According to the given process, the user can work as a taxi driver.
def Work(yandex,user): # taxi driver side
    if Is_user_current_taxi_drivers(yandex,user):
        if Continue_Work():
           process_for_taxi_driver(yandex,user)
        else:
            yandex.remove_current_taxi_drivers(user)
            print("Your work has been cancelled")
    else:
        if Is_work(): 
           yandex.add_current_taxi_drivers(user)
           process_for_taxi_driver(yandex,user)

# He asks the user if he wants to work.
def Is_work(): 
    s = "i want to work: type 1, \
         i don't want to work: type 2"
    return func(s)

# Asks the user if he wants to call a taxi.
def Is_call():  # ამის სახელი შესაცვლელია
    s = "i want to call a taxi: type 1, \
         i don't want to call a taxi: type 2"
    return func(s)

# Checks whether the taxi has been called by the user.
def Is_user_current_calls(yandex,user):
    return yandex.Is_user_current(user)

# Checks if the user is currently working as a taxi driver.
def Is_user_current_taxi_drivers(yandex,user):
    return yandex.Is_user_current(user)

# Asks the user who has been given an order to call a 
# taxi whether to continue the order or cancel it
def Continue_Call():
    s = "Continue Call: type 1, \
         Cancel Call: type 2"
    return func(s)

# Asks the user if they want to continue.
def Continue_Work():
    s = "Continue Work: type 1, \
         Cancel Work: type 2"
    return func(s)

def func(s):
    v_inside = True
    v_is = False

    while v_inside:
        print(s)
        inp_status = input("please enter 1 or 2: ")
        if inp_status == '1' or inp_status == '2':
            v_inside = False
            if inp_status == '1':
               v_is = True
        else:
             print('Invalid input')   
    return v_is

# This is the work process of taxi drivers.
def process_for_taxi_driver(yandex,user):
    if Is_Calls(yandex,user):
        v_call_user = Choice_Call(yandex,user)  
        if v_call_user != 'no call':
           yandex.remove_current_taxi_drivers(user)
           yandex.remove_current_calls(v_call_user)
           yandex.set_received_calls(user.personal_id,v_call_user.personal_id)
    else:
        print("There are no calls at the moment")
    
# Checks if any user has an order for a taxi call.
def Is_Calls(yandex,user):
    current_calls = yandex.get_current_calls()[user.service_type]
    if len(current_calls) > 0:
        return True
    return False

# Returns the user of the selected customer, and if the given 
# taxi driver has not selected any call then returns 'no call'
def Choice_Call(yandex,user):
    v_current_calls = yandex.get_current_calls()[user.service_type]
    v_num = 0
    v_inp = 0
    v_inside = True
    dicts_user = {}
    while v_inside:
        for i in v_current_calls:
            distance = random.randint(1,30)
            v_num += 1
            dicts_user[v_num] = [i,distance]
            print(f"type {v_num} - name : {i.name}, phone_number : {i.phone_num}, distance : {distance} km")
        v_num += 1
        print(f"type {v_num} - i don't want a work at this moment")
        v_inp = input(f"please enter from 1 to {v_num}: ")
        if is_valid(v_inp,v_num+1):
               v_inside = False
        else:
            dicts_user.clear()
            v_num = 0
            print("invalid input")
    
    if int(v_inp) != v_num:
       yandex.add_distance(dicts_user[int(v_inp)][0].personal_id,dicts_user[int(v_inp)][1])
       return dicts_user[int(v_inp)][0]
    return 'no call'

# Checks the validity of v_inp, i.e. if it is a number and sits in the right range.
def is_valid(v_inp,v_num):
    if len(v_inp) > 1 and v_inp[0] == '0':
       return False
    
    for i in v_inp:
        if i > '9' or i < '0':
            return False
        
    if int(v_inp) in range(1,v_num):
        return True
    
    return False
              
# Returns true if any taxi driver has taken the given user's call, otherwise false.
def Taxi_Driver_Recieve_Call(yandex,user):
    return yandex.exist_orderer_received_calls(user.personal_id)

# Shows the taxi driver data to the user.
def Show_Driver_data(yandex,user):
    taxi_driver = yandex.get_user(yandex.get_received_call(user.personal_id))
    distance = yandex.get_distance(user.personal_id)
    print(f"The driver is already on his way.")
    print(f'name : {taxi_driver.name}, phone_number : {taxi_driver.phone_num}, distance : {distance} km, service type : {taxi_driver.service_type}')
    print(f"{taxi_driver.car_series}, {taxi_driver.car_num}, {taxi_driver.car_color}")

# economy,comfort,business,I don't want to at this moment, 
# He will choose one of these four if he is 'orderer'
# If he is a 'taxi driver', he will choose only from these three: economy,comfort,business. 
def Choice_Service_Type(yandex,status,text):
    v_inside = True
    v_inp = ''
    service_types = yandex.service_types
    s = ''
    num = 0
    for i in service_types:
        num += 1
        s += '{}: type {},     '.format(i,str(num))
    if status == 'orderer':
       num += 1
       s += 'no call: type {},     '.format(str(num))

    while v_inside:
        print(s)
        v_inp = input(text)
        if is_valid(v_inp, num+1):
           v_inside = False
        else:
            print('Invalid input')  

    if status == 'orderer' and int(v_inp) == num:
       return 'no call'
    return service_types[int(v_inp) - 1]

# Remove account.
def Remove_Account(yandex):
    print('Enter your personal ID if you want to delete the account, if you change your mind, enter N')
    while True:
        personal_id = input("Please enter your personal id: ")
        user = yandex.get_user(personal_id)
        if user != -1:
           yandex.remove_user(user)
           print('Your account has been deleted')
           break
        elif personal_id == 'N':
            break
        else:
            print("incorrect personal id")



main()



