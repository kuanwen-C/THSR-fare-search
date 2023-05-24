import numpy as np
import pandas as pd
import csv
import flet as ft

ticket_df = pd.read_csv('tickets.csv', header=None)
ticket = ticket_df.values
ticket_df

southbound_dict = {}
for i in range(len(ticket[0])):
    for j in range(i+1, len(ticket[0])-1):
        station_1 = str(ticket[0][i+1])
        station_2 = str(ticket[0][j+1])
        southbound_dict[(station_1, station_2)] = (ticket[j+1][i+1], ticket[i+1][j+1])

northbound_dict = {}
for i in range(len(ticket[0])):
    for j in range(i+1, len(ticket[0])-1):
        station_1 = str(ticket[0][-i-1])
        station_2 = str(ticket[0][-j-1])
        northbound_dict[(station_1, station_2)] = (ticket[-i-1][-j-1], ticket[-j-1][-i-1])      
        
station = []
for i in range(1, len(ticket[0])):
    station.append(str(ticket[0][i]))
    
#GUI design
def main(page: ft.Page):
    global start_station, end_station


page.title = "Taiwan High Speed Rail Fare System"
page.window_width = 750
page.window_height = 600
page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

start_station = ""
end_station = ""
Start_button_list=[]       #用於設定12個出發車站的按鈕
End_button_list=[]         #用於設定12個到達車站的按鈕
temp_end=[]                #用於暫存要顯示的每行到達車站選項
temp_sta=[]                #用於暫存要顯示的每行出發車站選項

# 按鈕的function
def start_station_click(aaa):
  global start_station
  start_station=aaa.control.data                                            #取得START STATION
page.add(ft.Text(f'The start station of your choice:{start_station}'))    #輸出確認為哪站的TEXT

def end_station_click(aaa):
        global end_station
        end_station=aaa.control.data  
        page.add(ft.Text(f'The end station of your choice:{end_station}'))
    
def result_click(aaa):
        if southbound_dict.get((start_station, end_station)) is not None:
            page.add(ft.Text(f'The ticket fare of Standard Car is: {southbound_dict[start_station, end_station][0]}'))
            page.add(ft.Text(f'The ticket fare of Business Car is: {southbound_dict[start_station, end_station][1]}'))
        elif northbound_dict.get((start_station, end_station)) is not None:
            page.add(ft.Text(f'The ticket fare of Standard Car is: {northbound_dict[start_station, end_station][0]}'))
            page.add(ft.Text(f'The ticket fare of Business Car is: {northbound_dict[start_station, end_station][1]}'))
        else:
            page.add(ft.Text(f'The destination from {start_station} to {end_station} is not found'))
    
start_text = ft.Text("Please select a start station", size=18)
end_text = ft.Text("Please select a end station", size=18)
    
for i in range (12):                                                  
        Start_button_list.append(ft.ElevatedButton(text=f"{station[i]}", data=f"{station[i]}", width=150, on_click=start_station_click))
for i in range (12):
        End_button_list.append(ft.ElevatedButton(text=f"{station[i]}", data=f"{station[i]}", width=150, on_click=end_station_click))

calculate=ft.ElevatedButton(text=f"Calculate the fare", width=630, on_click=result_click)
   


# ------將物件進行排版------
page.add(start_text)
   

st_button=ft.Row(
                  wrap=True,
                  spacing=10,                            #button左右兼具虛擬pixel
                  run_spacing=10,                        #button上下間距虛擬pixel
                  controls=Start_button_list,
                  width=750,                              #此種寫法可藉由控制width來調整排版
                  alignment=ft.MainAxisAlignment.CENTER
                )
page.add(st_button)
page.add(end_text)
for i in range(0,12,4):
        temp_end=ft.Row(End_button_list[i:i+4],alignment=ft.MainAxisAlignment.CENTER)
        page.add(temp_end)   

page.add(calculate)              #最終計算按鈕
    
ft.app(target=main)
