# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 13:51:32 2022

@author: crf005r
"""
class Restaurant():
    
    def __init__(self, restaurant_name, cuisin_type):
        self.restaurant_name = restaurant_name
        self.cuisin_type = cuisin_type
        self.schedule = 9
        self.clients = 0
        self.first_name = ''
        self.last_name = ''   
        
    def describe_restaurant(self):
        """Descripcion del restarurante"""
        print("Welcome the Restaurant {}, we have {}".format(self.restaurant_name, self.cuisin_type))

    def update_schedule(self, new_schedule):
        try:
            if new_schedule >= self.schedule:
                print("We open later, the new schedule is {}".format(new_schedule))
            else:
                print("We open earlier, the new schedule is {}".format(new_schedule))
            self.schedule = new_schedule
        except:
            print("Colocate new schedule in format numerical")
            
    def open_restaurant(self):
        print("The Horari is {}:00 am a 20:00 pm".format(self.schedule))
    
    def sum_clients(self, clients):
        self.clients += clients
        print("How many customers were serverd in day of bussines {}".format(self.clients))
        
    def restart_orders(self,d_clients):
        if self.clients > 0:
            self.clients -= d_clients
        else: print("You can´t have number of negative customers")
        
    def greet_user(self, first_name):
        self.first_name = first_name
        print("Hello! {}".format(first_name))
        
    pass

pizza = Restaurant()
        
lissu = Restaurant('Lissu', 'Vegetarian')
lissu.__dict__ #Atributos de la clase
lissu.__dir__() #Atributos y metodos
lissu.__sizeof__()
lissu.describe_restaurant()
lissu.update_schedule('')
lissu.update_schedule(1)
lissu.schedule

dir(lissu)
help(lissu)

class Employee:
    # Create __init__() method
    def __init__(self, name = '', salary = 0):
        # Create the name and salary attributes
        self.name = name
        self.salary = salary
    
    # From the previous lesson
    def give_raise(self, amount):
        self.salary += amount

    def monthly_salary(self):
        return self.salary/12
        
emp = Employee("Korel Rossi", 50000)
print(emp.name)
print(emp.salary)     

emp = Employee()
emp.name = 'Korel Rossi'
emp.salary = 50000
print(emp.name)
print(emp.salary)     

# Write the class Point as outlined in the instructions
# For use of np.sqrt
import numpy as np

class Point:
    """ A point on a 2D plane
    
   Attributes
    ----------
    x : float, default 0.0. The x coordinate of the point        
    y : float, default 0.0. The y coordinate of the point
    """
    def __init__(self, x=0.0, y=0.0):
      self.x = x
      self.y = y
      
    def distance_to_origin(self):
      """Calculate distance from the point to the origin (0,0)"""
      return np.sqrt(self.x ** 2 + self.y ** 2)
    
    def reflect(self, axis):
      """Reflect the point with respect to x or y axis."""
      if axis == "x":
        self.y = - self.y
      elif axis == "y":
        self.x = - self.x
      else:
        print("The argument axis only accepts values 'x' and 'y'!")

pt = Point(x=3.0)
pt.reflect("y")
print((pt.x, pt.y))
pt.y = 4.0
print(pt.distance_to_origin())

