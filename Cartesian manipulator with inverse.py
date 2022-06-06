# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 00:51:15 2022

@author: USER
"""

import numpy as np
import math
import PySimpleGUI as sg
import pandas as pd
import roboticstoolbox as rtb
from roboticstoolbox import DHRobot, RevoluteDH, ERobot, ELink, ETS, PrismaticDH


# GUI code
sg.theme('BlueMono')
 
# Excel read code
EXCEL_FILE = 'Cartesian Manipulator Design Data.xlsx'
df = pd.read_excel(EXCEL_FILE)


#Layout of GUI

Main_layout = [
    [sg.Push(), sg.Text('Cartesian Manipulator Calculator', font=("Impact", 18)), sg.Push()],
    
    
    [sg.Frame('Fill out the following fields:',[[
    sg.Text('a1= '),sg.InputText('8',  key='a1', size=(10,1)),
     sg.Text('a2= '),sg.InputText('5', key='a2', size=(10,1)),
     sg.Text('a3= '),sg.InputText('5', key='a3', size=(10,1)),
     sg.Text('a4= '),sg.InputText('5', key='a4', size=(10,1)),
     sg.Text('d1= '),sg.InputText('3', key='d1', size=(10,1)),
     sg.Text('d2= '),sg.InputText('3', key='d2', size=(10,1)),
     sg.Text('d3= '),sg.InputText('3', key='d3', size=(10,1))]])],
    
    [sg.Button('Click This Before Solving Forward Kinematics',button_color=('white','red')), 
     sg.Text(('OR'),font = ("Comic San MS", 12)),
     sg.Button('Solve Inverse Kinematics', font = ("Comic San MS", 12), size=(20,0), button_color = ('black','orange')),],
    
    [sg.Frame('Postion Vector: ',
     [[sg.Text('X = '), sg.InputText(key='X', size=(10,1)),
       sg.Text('Y = '), sg.InputText(key='Y', size=(10,1)),
       sg.Text('Z = '), sg.InputText(key='Z', size=(10,1))]])],
    
    [sg.Button('Solve Forward Kinematics',disabled=True, font = ("Comic San MS", 12), size=(20,0), button_color=('white','green'))],
    
    [sg.Frame('H0_4 Transformation Matrix = ',[[sg.Output(size=(60,12))]]), sg.Push(), sg.Image('Cartesian_Manipulator.gif')],
   
    [sg.Submit(), sg.Button('Exit')],
     
    [sg.Push(), sg.Button('Jacobian Matrix', disabled=True, font=("Comic San MS", 12), size=(15,0), button_color=('purple','yellow')),
     sg.Button('Determinants', disabled=True,font = ("Comic San MS", 12), size=(15,0), button_color = ('purple','yellow')), 
     sg.Button('Inverse', disabled=True, font = ("Comic San MS", 12), size=(15,0), button_color = ('purple','yellow')),
     sg.Button('Transpose',disabled=True, font = ("Comic San MS", 12), size=(15,0), button_color = ('purple','yellow')), sg.Push()]
     
    ]

#Window code
window = sg.Window('Cartesian_Manipulator', Main_layout, resizable= True)

#Inverse Kinematics
def Inverse_Kinematics():
  sg.theme('BlueMono')  
 
  EXCEL_FILE = 'Cartesian Manipulator Inverse Kinematics Data.xlsx'
  IK_df = pd.read_excel(EXCEL_FILE)
  
  IK_layout = [
      
     [sg.Push(), sg.Text('Inverse Kinematics Calculator', font=("Impact", 18)), sg.Push()],
      
     [sg.Text ('Fill out the following fields:')],
      [sg.Text('a1= '),sg.InputText('0',  key='a1', size=(10,1)),
          sg.Text('mm',font=("Comic Sans MS", 10)),
          sg.Text('X= '),sg.InputText('0',  key='X', size=(10,1))],
      
      [sg.Text('a2= '),sg.InputText('0', key='a2', size=(10,1)),
          sg.Text('mm',font=("Comic Sans MS", 10)),
          sg.Text('Y= '),sg.InputText('0',  key='Y', size=(10,1))],
      
      [sg.Text('a3= '),sg.InputText('0', key='a3', size=(10,1)),
          sg.Text('mm',font=("Comic Sans MS", 10)),
          sg.Text('Z= '),sg.InputText('0',  key='Z', size=(10,1))],
       
      [sg.Text('a4= '),sg.InputText('0', key='a4', size=(10,1)),
           sg.Text('mm',font=("Comic Sans MS", 10))],
           
      [sg.Button('Solve Inverse Kinematics', font = ("Comic San MS", 12), size=(20,0), button_color = ('black','orange'))],
      
      [sg.Frame('Postion Vector:',
       [[sg.Text('d1 = '), sg.InputText(key='IK_d1', size=(10,1)),sg.Text('mm',font=("Comic Sans MS", 10)),
         sg.Text('d2 = '), sg.InputText(key='IK_d2', size=(10,1)), sg.Text('mm',font=("Comic Sans MS", 10)),
         sg.Text('d3 = '), sg.InputText(key='IK_d3', size=(10,1)),sg.Text('mm',font=("Comic Sans MS", 10))]])],
      
      [sg.Submit(), sg.Button('Exit')]
      ]
          
  #Window code
  Inverse_Kinematics_window =sg.Window('Inverse Kinematics Calculator',IK_layout)
  
  while True:
      event,values = Inverse_Kinematics_window.read()
      if event == sg.WIN_CLOSED or event == 'Exit':
          break
      elif event ==  'Solve Inverse Kinematics':
          a1 = float (values ['a1'])
          a2 = float (values ['a2'])
          a3 = float (values ['a3'])
          a4 = float (values ['a4'])
          
          #Position Vectors
          X = float (values ['X'])
          Y = float (values ['Y'])
          Z = float (values ['Z']) 
          
          try:
              d1 = a2 - Y
              
          except:
              d1 = -1 #NAN
              sg.popup('Warning! Present values cause error')
              sg.popup('Restatrt the GUI then assign proper values')
              break
          
          #d1
          d1 = (a2 - Y)
          
          #d2
          d2 = (X - a3)
          
          #d3
          d3 = (a1 - a4 - Z)
          
          #print ("d1 =", np.around(d1,3))
          #print ("d2 =", np.around(d2,3))
          #print ("d3 =", np.around(d3,3))
          
          d1 = Inverse_Kinematics_window['IK_d1'].Update(np.around(d1,3))
          d2 = Inverse_Kinematics_window['IK_d2'].Update(np.around(d2,3))
          d3 = Inverse_Kinematics_window['IK_d3'].Update(np.around(d3,3))
          
          
      elif event == 'Submit':
          IK_df = IK_df.append(values, ignore_index=True)
          IK_df.to_excel(EXCEL_FILE, index=False)
          sg.popup('Data saved!')

  Inverse_Kinematics_window.close()
          
                
            
#Disabling Codes
disable_FK = window['Solve Forward Kinematics']
disable_J = window['Jacobian Matrix']
disable_D = window['Determinants']
disable_I = window['Inverse']
disable_T = window['Transpose']

    

while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break 
    if event == 'Click This Before Solving Forward Kinematics':
        disable_FK.update(disabled=False)
        disable_J.update(disabled=True)
        disable_D.update(disabled=True)
        disable_I.update(disabled=True)
        disable_T.update(disabled=True)
        
    
    if event == 'Solve Forward Kinematics':
        # Foward Kinematic Codes
        # Link Lengths in cm
        a1 = float (values ['a1'])
        a2 = float (values ['a2'])
        a3 = float (values ['a3'])
        a4 = float (values ['a4'])
        d1 = float (values ['d1'])
        d2 = float (values ['d2'])
        d3 = float (values ['d3'])
       
        DHPT = [[0,(270.0/180.0)*np.pi,0,a1],
             [(270.0/180.0)*np.pi,(270.0/180.0)*np.pi,0,a2+d1],
             [(270.0/180.0)*np.pi,(90.0/180.0)*np.pi,0,a3+d2],
             [0,0,0,a4+d3]]

        #D-H Notation Formula for HTM

        i = 0
        H0_1 = [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.cos(DHPT[i][0])],
                [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.sin(DHPT[i][0])],
                [0,np.sin(DHPT[i][1]),np.cos(DHPT[i][1]),DHPT[i][3]],
                [0,0,0,1]]
        i = 1
        H1_2 = [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.cos(DHPT[i][0])],
                [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.sin(DHPT[i][0])],
                [0,np.sin(DHPT[i][1]),np.cos(DHPT[i][1]),DHPT[i][3]],
                [0,0,0,1]]
        i = 2
        H2_3 = [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.cos(DHPT[i][0])],
                [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.sin(DHPT[i][0])],
                [0,np.sin(DHPT[i][1]),np.cos(DHPT[i][1]),DHPT[i][3]],
                [0,0,0,1]]

        i = 3
        H3_4 = [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.cos(DHPT[i][0])],
                [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.sin(DHPT[i][0])],
                [0,np.sin(DHPT[i][1]),np.cos(DHPT[i][1]),DHPT[i][3]],
                [0,0,0,1]]

        # print("H0_1 = " )
        # print(np.matrix(H0_1))
        # print("H1_2 = " )
        #print(np.matrix(H1_2))
        # print("H2_3 = " )
        #print(np.matrix(H2_3))
        # print ("H3_4 = " )
        #print(np.matrix(H3_4))
        
        print("Transformation Matrix")
        H0_2 = np.dot(H0_1,H1_2)
        H0_3 = np.dot(H0_2,H2_3)
        H0_4 = np.dot(H0_3,H3_4)
        print("H0_4=",np.around(H0_4,3))
        print(np.matrix(H0_4))
        
        print("Position Vector")
        X0_4 = H0_4[0,3]
        print("X = ",np.around(X0_4,3))

        Y0_4 = H0_4[1,3]
        print("Y = ",np.around(Y0_4,3))

        Z0_4 = H0_4[2,3]
        print("Z = ",np.around(Z0_4,3))
        
        X = window['X'].Update(np.around(X0_4,3))
        Y = window['Y'].Update(np.around(Y0_4,3))
        Z = window['Z'].Update(np.around(Z0_4,3))
        
        
        disable_J.update(disabled=False)

        
    if event == 'Submit' :
        df = df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data saved!')
        
    if event == 'Jacobian Matrix' :
        Z_1= [[0],[0],[1]] #[0,0,1] vector
        
        # row 1-3, Column 1
        J1 = [[1,0,0],[0,1,0],[0,0,1]]
        J1 = np.dot(J1,Z_1)
        J1 = np.matrix (J1)
        #print(np.matrix(J1))
        #print('J1 = ')
        
        
        # row 1-3, Column 2
        try:
            H0_1 = np.matrix(H0_1)
        except:
            H0_1 = -1 #NAN
            sg.popup('Warning!')
            sg.popup('Restart the GUI, Click first "Click This Before Solving Forward Kinematics')        
            break
        
        J2 = H0_1[0:3,0:3]
        J2 = np.dot(J2,Z_1)
        J2 = np.matrix (J2)
        #print(np.matrix(J2))
        #print('J2 = ')
        
        
        # row 1-3, Column 3
        J3 = H0_2[0:3,0:3]
        J3 = np.dot(J3,Z_1)
        J3 = np.matrix (J3)
        #print(np.matrix(J3))
        #print('J3 = ')
        
        # row 1-3, Column 4
        J4 = H0_3[0:3,0:3]
        J4 = np.dot(J4,Z_1)
        J4 = np.matrix (J4)
        #print(np.matrix(J4))
        #print('J4 = ')
       
        
        J5 = [[0],[0],[0]]
        J5 = np.matrix(J5)
        # print("J5 = ")
        # print(J5)
        
        J6 = [[0],[0],[0]]
        J6 = np.matrix(J6)
        # print("J6 = ")
        # print(J6)
        
        J7 = [[0],[0],[0]]
        J7 = np.matrix(J7)
        # print("J7 = ")
        # print(J7)
        
        J8 = [[0],[0],[0]]
        J8 = np.matrix(J8)
        # print("J8 = ")
        # print(J8)
        
        
        ### 3. Concatenated Jaccobian Matrix
        JM1 = np.concatenate((J1,J2,J3,J4),1)
       # print(JM1)

        JM2 = np.concatenate((J5,J6,J7,J8),1)
       # print(JM2)

        J = np.concatenate((JM1,JM2),0)
        #print("J = ")
        #print(J)
        sg.popup('J = ', J)
        JJ = J[0:4,0:4]
        DJ = np.linalg.det(JJ)
        if DJ == 0.0 or DJ == -0.0:
          disable_J.update(disabled =True)
          sg.popup('Warning: Jacobian Matrix is Non-invertable!')
        
        elif DJ == 0.0 or DJ == -0.0:
            disable_I.update(disable=False)
           
        disable_J.update(disabled=True)
        disable_D.update(disabled=False)
        disable_I.update(disabled=True)
        disable_T.update(disabled=False)
        
    if event == 'Determinants':
        #singularity = D
        #np.linalg.D
        #Let JM1 become the 4X4 position matrix for obtaining the Determinant
        
        try:
            JM1 = np.concatenate((J1,J2,J3,J4),1)
        except:
            JM1 = -1 #NAN
            sg.popup('Warning!')
            sg.popup('Restart the GUI, Click first "Click This Before Solving Forward Kinematics')        
            break
        
        JJ = J[0:4,0:4]
        #print (JJ)
        DJ = np.linalg.det(JJ)
        #print("DJ = ", DJ)
        sg.popup('DJ = ',DJ)

        if DJ == 0.0 or DJ == -0.0:
          disable_J.update(disabled =True)
          sg.popup('Warning: Jacobian Matrix is Non-invertable!')
    
    if event == 'Inverse':
        
        try:
            JM1 = np.concatenate((J1,J2,J3,J4),1)
        except:
            JM1 = -1 #NAN
            sg.popup('Warning!')
            sg.popup('Restart the GUI, Click first "Click This Before Solving Forward Kinematics')        
            break
        
        JJ = J[0:4,0:4]
        I = np.linalg.inv(JJ)
        sg.popup('I = ', I)

    if event == 'Transpose':
        try:
            JM1 = np.concatenate((J1,J2,J3,J4),1)
        except:
            JM1 = -1 #NAN
            sg.popup('Warning!')
            sg.popup('Restart the GUI, Click first "Click This Before Solving Forward Kinematics')        
            break
        T = np.transpose(JJ)
        sg.popup('T = ', T)
        
    elif event == 'Solve Inverse Kinematics':
        Inverse_Kinematics()
        
    
window.close()

