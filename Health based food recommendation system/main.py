from tkinter  import *
from tkinter import ttk
# from tkinterttk import Combobox, Style
from PIL import Image, ImageTk
import tkinter as tk
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
def getvals():
    
      # open_secondary_gui(main_win)
      result_text.delete(1.0, tk.END)  # Clear previous text
      
     
      
      for i,j in my_dict.items():
        if(j==e6.get()):
          print("Selected Region:- ","(",i,")",e6.get())
          Region_para = i


      height=float(e1.get())
      # print("h",height)
      weight=float(e2.get())
      # print("w",weight)
      age=int(e3.get())
      # print("a",age)
      gender= e4.get()
      # print(gender)
      activity_level = e5.get()
      # activity_level = StringVar(e5)

      isVegpara = var.get()  #veg/non-veg
      
      height_m = height / 100
      bmi = weight / (height_m ** 2)
      bmi = round(bmi, 2)

      
      # Calculate BMR  (kcal/day)
      if gender == 'male':
        desired_calorie_intake = 2500
        bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
        bmr=round(bmr, 2)

    
      else:
        desired_calorie_intake = 2000
        bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)  
        bmr=round(bmr, 2)

       
      print("welcome dear", e0.get())
      result_text.insert(tk.END, f"welcome Dear {e0.get()}\n")


      #conditions
      print("Your body mass index is: ", bmi)
      result_text.insert(tk.END, f"Your body mass index is: {bmi}\n")

      if ( bmi < 16):
        print("Acoording to your BMI, you are Severely Underweight")
        result_text.insert(tk.END, f"Acoording to your BMI, you are Severely Underweight\n")
         
      elif ( bmi >= 16 and bmi < 18.5):
        print("Acoording to your BMI, you are Underweight")
        result_text.insert(tk.END, f"Acoording to your BMI, you are Severely Underweight\n")

        
      elif ( bmi >= 18.5 and bmi < 25):
        print("Acoording to your BMI, you are Healthy")
        result_text.insert(tk.END, f"Acoording to your BMI, you are Severely Healthy\n")

        
      elif ( bmi >= 25 and bmi < 30):
        print("Acoording to your BMI, you are Overweight")
        result_text.insert(tk.END, f"Acoording to your BMI, you are Severely Overweight\n")

        
      elif ( bmi >=30):
        print("Acoording to your BMI, you are Severely Overweight")
        result_text.insert(tk.END, f"Acoording to your BMI, you are Severely Overweight\n")


        


# Calculate calories i.e tdee /day


# tdee = bmr * physical activity level factor   #total daily energe expendeture genral equation 

#REFRANCE :- https://www.omnicalculator.com/health/tdee
        
      result_text.insert(tk.END, f"{activity_level}\n") 

      if activity_level == 'sedentary':
       tdee = bmr * 1.2   #tdee
      elif activity_level == 'lightly_active':
       tdee = bmr * 1.375    #tdee
      elif activity_level == 'moderately_active':
        tdee = bmr * 1.55    #tdee
      elif activity_level == 'very_active':
       tdee = bmr * 1.725    #tdee
      elif activity_level == 'hard exercise':
       tdee = bmr * 1.9     #tdee
      elif activity_level == 'professional athlete':
       tdee = bmr * 2.4     #tdee
       
    
      # print(tdee)

      df = pd.read_csv(r"HBRS.csv", encoding='unicode_escape')

      
      print("total daily energe expendeture",round(tdee, 2))
      result_text.insert(tk.END, f"total daily energe expendeture {round(tdee, 2)}\n")


      calories_to_burn= tdee-desired_calorie_intake
      calories_to_burn= calories_to_burn * (-1)

      calorie_difference = desired_calorie_intake 


      print("calories should be (-)burned/(+)gain",round(calories_to_burn, 2))
      result_text.insert(tk.END, f"calories should be (-)burned/(+)gain {round(calories_to_burn, 2)}\n")


      num_predictions = 6  
      predictions = []

      for _ in range(num_predictions):
        df_filtered = df[(df['isVeg'] == isVegpara) & (df['Regions'] == Region_para) &(df['totalCaloriesInCal'] <= calorie_difference) ]
        
    
        if df_filtered.empty:
          print("No more suitable food items available.")
          break
    
        features = df_filtered[['totalCaloriesInCal' , 'Regions' , 'isVeg' ]]
        target = df_filtered[['name', 'cuisine', 'course']]
        dt = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=0)
        dt.fit(features, target)

        prediction = dt.predict(features.iloc[[0]])
        food_name = prediction[0][0]
        food_calories = df[df['name'] == food_name]['totalCaloriesInCal'].values[0]
        food_cuisine = df[df['name'] == food_name]['cuisine'].values[0]
        food_time = df[df['name'] == food_name]['course'].values[0]
        food_isVeg = df[df['name'] == food_name]['isVeg'].values[0]
        food_Regpara = df[df['name'] == food_name]['Regions'].values[0]
        predictions.append((food_name, food_calories, food_cuisine, food_time, food_isVeg , food_Regpara))


        df = df[df['name'] != food_name]

        calorie_difference -= food_calories

      print("Recommended Food:")
      result_text.insert(tk.END, f"Recommended Food:\n")


      
      
      for food_name, food_calories, food_cuisine, food_time ,food_isVeg , food_Regpara in predictions:  
        
        # print("Dish name-",food_name, ",food calories-", food_calories, ",Food Type-", food_cuisine, ",Food Time-", food_time,",veg(1)/non-veg(0)", food_isVeg, ",Region parameter-", food_Regpara)
        
        print("\n","Dish name-",food_name, "|| food calories-", food_calories, "|| Food Type-", food_cuisine, "|| Dish Time/Type-", food_time )
        result_text.insert(tk.END, f"\nDish name-{food_name} || food calories-{food_calories}|| Food Type-{food_cuisine}||Dish Time/Type-{food_time}\n")

      
      exercise_tips(bmi)  #workout tips function call

    #   quit()   #exit 
    

def exercise_tips(bmi):
  result_text.insert(tk.END, f"\nRecommended Workout Tips:\n")

  if(bmi<18.5):
   result_text.insert(tk.END, f'''Focus on building muscle and strength rather than calorie burning.
   Try low-impact exercises like swimming, yoga, or Pilates.
   Use light weights or resistance bands for strength training.\n''')
  elif ( bmi >= 18.5 and bmi < 25):
        result_text.insert(tk.END, f'''You have the most flexibility in terms of exercise choices.
        Aim for at least 150 minutes of moderate-intensity aerobic activity or 75 minutes of vigorous-intensity aerobic activity per week.
        Include strength training exercises for all major muscle groups at least twice a week.\n''')

        
  elif ( bmi >= 25 and bmi < 30):
        result_text.insert(tk.END, f'''Choose moderate-intensity exercises that are comfortable for you, such as brisk walking, biking, or swimming.
        Gradually increase the intensity and duration of your workouts as you get fitter.
        Add strength training exercises to help build muscle and burn more calories.\n''')

        
  elif ( bmi >=30):
        result_text.insert(tk.END, f'''It's important to start with low-impact exercises to avoid putting too much stress on your joints.
        Water-based exercises like swimming or water aerobics are a great option.
        You can also try stationary biking, elliptical training, or gentle yoga.
        As you get fitter, you can gradually add more weight-bearing exercises.\n''')
        

def quit():  
    quit




if __name__ == '__main__':
    main_win = Tk()

    font_settings = ("Arial", 14, "bold")  # font details

    top_frame = tk.Frame(main_win, width=200, height=300)
    top_frame.grid(sticky= N, padx=10, pady=10)

    main_win__ = tk.Frame(main_win, width=200, height=300, bg=("#FFA844")) 
    main_win__.grid(sticky= SW ,  padx=10, pady=10)



    Label(main_win__,text="Enter your Name:",font=font_settings,background="#FFD580").grid(row=0,column=0,sticky=W,padx= 4,pady=6)
    Label(main_win__,text="Enter your Height (in cm):",font=font_settings,background="#FFD580").grid(row=1,column=0,sticky=W,padx= 4,pady=6)
    Label(main_win__,text="Enter your Weight (in kg):",font=font_settings,background="#FFD580").grid(row=2,column=0,sticky=W,padx= 4,pady=6)
    Label(main_win__,text="Age:",font=font_settings,background="#FFD580").grid(row=3,column= 0,sticky=W,padx= 4,pady=6)
    Label(main_win__,text="gender(male/female):",font=font_settings,background="#FFD580").grid(row=4,column=0,sticky=W,padx= 4,pady=6)
    Label(main_win__,text="physical activity level:",font=font_settings,background="#FFD580").grid(row=5,column=0,sticky=W,padx= 4,pady=6)
    Label(main_win__,text="what type of food you likes to eat ?:",font=font_settings,background="#FFD580").grid(row=6,column=0,sticky=W,padx= 4,pady=6)
    Label(main_win__,text="Are you vegeterian ?:",font=font_settings,background="#FFD580").grid(row=7,column=0,sticky=W,padx= 4,pady=6)
    

    e0 = Entry(main_win__, textvariable= StringVar() ,font=font_settings,background="#FFD580")  #user name
    e1 = Entry(main_win__ ,font=font_settings,background="#FFD580")
    e2 = Entry(main_win__ ,font=font_settings,background="#FFD580")
    e3 = Entry(main_win__ ,font=font_settings,background="#FFD580")
    e4 = Entry(main_win__, textvariable= StringVar(),background="#FFD580")
    e5 = Entry(main_win__, textvariable= StringVar(),background="#FFD580")

    e0.grid(row=0, column=1 ,sticky=W,pady=4)
    e1.grid(row=1, column=1 ,sticky=W,pady=4)
    e2.grid(row=2, column=1 ,sticky=W,pady=4)
    e3.grid(row=3, column=1 ,sticky=W,pady=4)

    var = IntVar()  # for radio button 
    e6 = StringVar()  #used in first for loop used for cusine and its not a entry variable




    # dropdown box  1
    my_dict={0:'Indian', 1:'South Indian', 2:'Andhra',3: 'Udupi', 4:'Mexican', 5:'Fusion', 6:'Continental', 7:'Bengali', 8:'Punjabi', 9:'Chettinad', 10:'Tamil Nadu', 11:'Maharashtrian', 12:'North Indian', 13:'Italian', 14:'Sindhi', 15:'Thai', 16:'Chinese', 17:'kerala', 18:'Gujarati ', 19:'Coorg', 20:'Rajasthani', 21:'Asian', 22:'Middle Eastern', 23:'Coastal Karnataka', 24:'European', 25:'Kashmiri', 26:'Karnataka', 27:'Lucknowi', 28:'Hyderabadi', 29:'Andaman', 30:'Goan', 31:'Assamese', 32:'Bihari', 33:'Malabar', 34:'Himachal', 35:'Awadhi', 35:'Cantonese', 36:'North East India', 37:'Pakistani', 38:'Mughlai', 39:'Japanese', 40:'Mangalorean', 41:'Vietnamese', 42:'British', 43:'North Karnataka', 44:'Parsi', 45:'Greek',46: 'Nepalese', 47:'oriya',+ 48:'French', 49:'Sichuan', 50:'Indo Chinese', 51:'Konkan', 52:'Mediterranean',53: 'Sri Lankan', 54:'Haryana', 55:'Gujarati', 56:'Uttar Pradesh', 57:'Malvani Indonesian', 58:'African', 59:'Shandong', 60:'Korean', 61:'American', 62:'Kongunadu', 63:'Caribbean', 64:'South Karnataka', 65:'Arab' }
    cuisine=list(my_dict.values())       # options region
    c1 = ttk.Combobox(main_win__, values=cuisine,width=18, textvariable=e6,font=font_settings) # Combobox
    # c1.configure(style="my.TCombobox")
    c1.grid(row=6,column=1,sticky=W,pady=4) # adding to grid
    c1.set('select anyone') # default selected option



    # dropdown box  2
    act =['sedentary','lightly_active','moderately_active','very_active','hard exercise' , 'professional athlete'] # options  Activity level
    e5 = ttk.Combobox(main_win__, values=act,width=18,font=font_settings) # Combobox
    e5.grid(row=5,column=1,sticky=W,pady=4) # adding to grid
    e5.set('select anyone') # default selected option

    # dropdown box  3
    gender =['male', 'female'] # options  gender
    e4 = ttk.Combobox(main_win__, values=gender,width=18,font=font_settings ) # Combobox
    e4.grid(row=4,column=1,sticky=W,pady=4) # adding to grid
    e4.set('select anyone') # default selected option




    #  Radiobutton
    R1 =  Radiobutton(main_win__, text="Yes" , pady=4  , variable= var , value= 1,font=font_settings,background="#FFD580").grid(row=7,sticky=W,column=1,pady=0) 
    R2 =  Radiobutton(main_win__, text="No" ,pady=4  , variable= var , value= 0 ,font=font_settings,background="#FFD580").grid(row=7,column=1,padx=80 ,sticky=W) #sticky=W,



    # output Text on tkinter
    result_text = tk.Text(top_frame, height=15, width=151 ,font=("Baskerville Old Face",15),background="#FFD580")
    result_text.grid(row=1, column=1 )  



    # Button
    Button(main_win__,fg="Black",background="green",text='ENTER',borderwidth=15,command=getvals).grid(row=8,column=1,sticky=E,pady=6)
    Button(main_win__,fg="Black",background="red",text='EXIT',borderwidth=15,command=main_win.quit).grid(row=8,column=0,sticky=W,pady=6)

    Label(main_win__,text="Copyright\n© 2024 PRMCEAM",font=("Arial",8),background="#FFD580").grid(row=9,column=4,padx= 100)#,pady=2)


    main_win.geometry("400x500")
    main_win.minsize(400,500)
    # main_win.maxsize(1000,350)
    main_win.configure(bg=("#FFA844"))   #background color of main win  bg=("#FFA844")

    main_win.wm_title("Health based food recommendation system by:- G5")


    main_win.mainloop()




