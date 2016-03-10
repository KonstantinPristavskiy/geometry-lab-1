# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 16:39:38 2016

@author: Konstantin
"""

""" Програма для визначення точки перетину двох відрізків і визначення кута
    між двома відрізками"""

import numpy
from math import sqrt, acos, degrees
eps = 10**-6

class Segment: #описывает класс отрезка на плоскости
    def __init__(self,x1,y1,x2,y2): # в качестве первой точки выбирается либо самая левая,
        self.parralell_to_Oy = False
        if x1<x2:                   # либо если точки совпадают по оси X, самая верхняя
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
        elif x1>x2:
            self.x1 = x2
            self.y1 = y2
            self.x2 = x1
            self.y2 = y1
        else:
            self.parralell_to_Oy = True
            if y1>=y2:
                self.x1 = x1
                self.y1 = y1
                self.x2 = x2
                self.y2 = y2
            else:
                self.x1 = x2
                self.y1 = y2
                self.x2 = x1
                self.y2 = y1

        self.A=self.y2-self.y1 # считает уравнение прямой
        self.B=-(self.x2-self.x1)
        self.C=-self.x1*(self.y2-self.y1)+self.y1*(self.x2-self.x1)

        self.x= self.x2-self.x1 #считает координаты вектора
        self.y=self.y2-self.y1

    def __str__(self):
        return "((" + str(self.x1)+","+str(self.y1)+"),(" +str(self.x2)+","+str(self.y2)+"))"

    def is_parrarel(self, segm): #находятся ли отрезки на паралельные линиях
        return numpy.linalg.det([[self.A, self.B], [segm.A, segm.B]])==0
    def is_same(self,segm): #находятся ли отрезки на одной линии
             return numpy.linalg.det([[self.A, self.C], [segm.A, segm.C]])==0 and numpy.linalg.det([[self.B, self.C], [segm.B, segm.C]])==0
    def point_in(self,x,y): # проверка, принадлежит ли точка отрезку
    #проверка отдельно по оси X (точка х1 всегда меньше x2), и отдельно по оси Y.
        
        
        return self.x1-eps<=x<=self.x2+eps and (self.y1-eps<=y<=self.y2+eps or self.y1+eps>=y>=self.y2-eps)

    def intersect(self, segm):
        if self.is_point() and segm.is_point(): #если оба отрезка выражены в точку
            return self.intersect_points(segm)
        elif self.is_point(): #если первый отрезок выраженый в точку
            return segm.intersect_with_point(self.x1,self.y1)
        elif segm.is_point(): #если второй отрезок выражен в точку
            return self.intersect_with_point(segm.x1, segm.y1)
        else:
            if self.is_parrarel(segm): #если прямые, построенные на отрезках паралельны
                if self.is_same(segm): # и совпадают
                    return self.find_intersected_segm_on_same_line(segm)
                else:  #если паралельны и не совпадают
                    return False
            else:  #если не паралельны, ищем точку пересечения
                point = self.line_intersect(segm)
                if self.point_in(point[0],point[1]) and segm.point_in(point[0],point[1]):
                    return point
                else:
                    return  False

    def line_intersect(self, segm): #возвращает точку пересечения двух прямых
         X = -numpy.linalg.det([[self.C, self.B], [segm.C, segm.B]])/numpy.linalg.det([[self.A, self.B], [segm.A, segm.B]])
         Y = -numpy.linalg.det([[self.A, self.C], [segm.A, segm.C]])/numpy.linalg.det([[self.A, self.B], [segm.A, segm.B]])
         print (X,Y)
         return(X,Y)

    def is_point(self): # проверяет, производится ли отрезок в точку
        return self.x1==self.x2 and self.y1==self.y2

    def intersect_points(self, segm): # совпадают ли две точки
        if self.x1==segm.x1 and self.y1 == segm.y1:
            return (self.x1,self.y1)
        else:
            return False

    def intersect_with_point(self, X,Y): # пересечь отрезок и точку
        if self.A*X+self.B*Y+self.C==0:
            if self.point_in(X,Y):
                return (X,Y)
            else:
                return False
        else:
            return False

    def find_intersected_segm_on_same_line(self,segm): # найти пересечение отрезков, если они на одной line
       if self.parralell_to_Oy: #если линия, на которой находятся оба отрезка, паралельна оси Y
           if self.y1<segm.y2 or self.y2>segm.y1:
               #если не совпадают
               return False
           elif self.y1==segm.y2: #если пересекаются по одной точке
               return (self.x1,self.y1)
           elif segm.y1==self.y2: #если пересекаются по второй точке
               return (segm.x1,segm.y1)
           else:
               return ((self.x1, min(self.y1,segm.y1)),(self.x1,max(self.y2,segm.y2)))
       else: #все остальные случаи
           if self.x1>segm.x2 or self.x2<segm.x1:  #если не совпадают
               return False
           elif self.x1==segm.x2: # если пересекаются по одной точке
               return (self.x1,self.y1)
           elif segm.x1==self.x2:
               return (segm.x1,segm.y1)
           else:  # возвращается отрезок из максимальной точки среди левых и минимальной среди правых
               if self.x1 == max(self.x1,segm.x1):
                   min_point = (self.x1,self.y1)
               else:
                   min_point = (segm.x1,segm.y1)
               if self.x2== min(self.x2,segm.x2):
                   max_point = (self.x2,self.y2)
               else:
                   max_point = (segm.x2,segm.y2)
               return (min_point, max_point)

    def find_angle(self,segm):
        if self.is_point() or segm.is_point():
            return False
        elif self.is_parrarel(segm):
            return 0 
        else:
            cos_between_vectors = (self.x*segm.x+self.y*segm.y)/(sqrt(self.x**2+self.y**2)*sqrt(segm.x**2+segm.y**2))
            print(cos_between_vectors)         
            if numpy.linalg.det([[self.x, self.y], [segm.x, segm.y]])>0:
                return degrees(acos(cos_between_vectors))
            else:
                return 360-degrees(acos(cos_between_vectors))




s1 = Segment(-1,2,1,4)
s2 = Segment(-2,3,4,5)
print(s1, " пересекается с ", s2, " в ", s1.intersect(s2))
#print("Угол между ", s1, " и ", s2, " равен ", s1.find_angle(s2))
#s3 = Segment(2,2,3,3)
#print(s1, " пересекается с ", s3, " в ", s1.intersect(s3))
#s4=Segment(1,0,1,3)
#print(s2, " пересекается с ", s4, " в ", s2.intersect(s4))
p1=Segment(-5.00000000000001,2,1,4)
p2=Segment(-2,3,4,5)
print("Угол между ", p1, " и ", p2, " равен ", p1.find_angle(p2))

#
