import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os



BACKGROUND_COLOR = "white"
FOREGROUND_COLOR = "Black"
ENTRYCOLOR ="Gray"
ENTRYWIDTH = 10
FONT = "LingWai TC"
DATAPASSWORD = os.environ.get("PASSWORD")

class Data:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=DATAPASSWORD,
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS drinksdata")
        self.cursor.execute("USE drinksdata")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS drinks(
              id INT  AUTO_INCREMENT PRIMARY KEY,
               store_name VARCHAR(255),
               drinks  VARCHAR(255),
               size VARCHAR(50),
               price DECIMAL(10))""")


class TitleBottom:
    def __init__(self,root):
        self.title_section = tk.Frame(root)
        self.title_section.configure(bg="white")
        self.title_section.grid(column=0,columnspan=2,row=0, pady=20, padx=20)
        self.title_text = tk.Label(self.title_section,
                              text="飲料查詢系統",
                              font=("LingWai TC", 50, "bold"),
                              fg="Black",
                              bg=BACKGROUND_COLOR)
        self.title_text.grid(column=1,row=0,padx=5, pady=5)
        self.set_title_img()

        self.bottom_section = tk.Frame(root)
        self.bottom_section.configure(bg=BACKGROUND_COLOR)
        self.bottom_section.grid(column=0,columnspan=2,row=3)
        self.set_bottom_img()
        self.switch_bottom_picture()
    def set_title_img(self):
        self.images = [
            Image.open("背景圖片/drink_shiso_juice.png").resize((50, 50)),
            Image.open("背景圖片/drink_ume_juice.png").resize((50, 50))]

        self.current_index_left = 0
        self.current_index_right = 1

        self.current_image_left = ImageTk.PhotoImage(self.images[self.current_index_left])
        self.current_picture_left = tk.Label(self.title_section,image=self.current_image_left,background="White" )
        self.current_picture_left.grid(column=0,row=0,padx=5)

        self.current_image_right = ImageTk.PhotoImage(self.images[self.current_index_right])
        self.current_picture_right = tk.Label(self.title_section,image=self.current_image_right,background="White" )
        self.current_picture_right.grid(column=2,row=0,padx=5)
        self.switch_title_picture()

    def switch_title_picture(self):

        self.current_index_left = (self.current_index_left+1)% len(self.images)
        self.current_image_left=ImageTk.PhotoImage(self.images[self.current_index_left])
        self.current_picture_left.config(image=self.current_image_left,background="White",padx=5)

        self.current_index_right = (self.current_index_right + 1) % len(self.images)
        self.current_image_right= ImageTk.PhotoImage(self.images[self.current_index_right])
        self.current_picture_right.config(image=self.current_image_right, background="White",padx=5)
        self.title_section.after(1500, self.switch_title_picture)

    def set_bottom_img(self):
        self.bottom_images=[
            Image.open("背景圖片/drink_tapioca_pink.png").resize((30, 55)),
            Image.open("背景圖片/drink_tapioca_green.png").resize((30, 55)),
            Image.open("背景圖片/drink_tapioca_white.png").resize((30, 55)),
            Image.open("背景圖片/drink_tapioca_brown.png").resize((30, 55))]
        self.bottom_picture=[]
        self.bottom_items = []
        for i in range(10):
            self.index = i % len(self.bottom_images)
            self.bottom_picture.append(ImageTk.PhotoImage(self.bottom_images[self.index]))
            self.label = tk.Label(self.bottom_section,
                                  image=self.bottom_picture[i],background=BACKGROUND_COLOR)
            self.bottom_items.append(self.label)
            self.bottom_items[i].grid(column=i,row=0,padx=20,pady=5)
        self.current_index = 0
    def switch_bottom_picture(self):
        self.current_index = (self.current_index - 1) % len(self.bottom_picture)
        for i,label in enumerate(self.bottom_items):
            picture_index =(i+self.current_index) % (len(self.bottom_picture))
            label.configure(image=self.bottom_picture[picture_index])

        self.bottom_section.after(1000, self.switch_bottom_picture)


class System:
    def __init__(self, root,data):
        self.data = data
        self.search_section = tk.Frame(root)
        self.search_section.grid(column=0,columnspan=2,row=1,pady=10,padx=5,sticky="ew")
        self.search_form()


        self.insert_section = tk.Frame(root)
        self.insert_section.grid(column=0, row=2,pady=20,padx=5)
        self.insert_form()


        self.update_section = tk.Frame(root)
        self.update_section.grid(column=1, row=2, pady=20,padx=5)
        self.update_form()
    def search_form (self):

        self.search_section.configure(background=BACKGROUND_COLOR)
        self.data.cursor.execute("SELECT * FROM drinks")
        alls = self.data.cursor.fetchall()
        values = []
        for item in alls:
            if item[1] not in values:
                values.append(item[1])

        self.store_label = tk.Label(self.search_section, text="店家查詢",font=(FONT,30),
                                    background=BACKGROUND_COLOR,foreground=FOREGROUND_COLOR)
        self.store = ttk.Combobox(self.search_section, values=values)
        self.store_label.grid(column=0, row=0, pady=5)
        self.store.grid(column=1, row=0)
        self.search_button = tk.Button(self.search_section, text="查詢",font=(FONT,20),
                                        highlightbackground=BACKGROUND_COLOR,command=self.search)
        self.search_button.grid(column=2, row=0, ipadx=15)

        self.explain = tk.Label(self.search_section,
                    text="使用上方選項挑選店家查詢各家飲料價格\n如欲修改資料，點選表格中的項目後按下「修改資料」\n即可在最下方表單進行修改。",
                    bg=BACKGROUND_COLOR,
                    font=(FONT,20),
                    foreground="Gray")
        self.explain.grid(column=1, row=1)

        self.explain_image =Image.open("背景圖片/mark_manpu11_kirakira.png").resize((50, 50))
        self.explain_picture = ImageTk.PhotoImage(self.explain_image)
        self.picture_left = tk.Label(self.search_section,
                                     image=self.explain_picture,background=BACKGROUND_COLOR)
        self.picture_left.grid(column=0,row=1)
        self.picture_right = tk.Label(self.search_section,
                                     image=self.explain_picture,background=BACKGROUND_COLOR)
        self.picture_right.grid(column=2, row=1)



        self.tree_top_image = Image.open("背景圖片/line_dots3_yellow.png").resize((700, 5))
        self.tree_top_picture = ImageTk.PhotoImage(self.tree_top_image)
        self.tree_top = tk.Label(self.search_section,
                                       image=self.tree_top_picture,background=BACKGROUND_COLOR)
        self.tree_top.grid(column=0,columnspan=3,row=2)

        self.tree_bottom_image = Image.open("背景圖片/line_dots3_yellow.png").resize((700, 5))
        self.tree_bottom_picture = ImageTk.PhotoImage(self.tree_bottom_image)
        self.tree_bottom_ = tk.Label(self.search_section,
                                 image=self.tree_bottom_picture, background=BACKGROUND_COLOR)
        self.tree_bottom_.grid(column=0, columnspan=3, row=4)

        self.tree = ttk.Treeview(self.search_section,
                                 columns=("店家名稱", "飲料名稱", "飲料大小", "飲料價格"),
                                 show='headings' ,style="Treeview")
        self.tree.heading("店家名稱", text="店家名稱")
        self.tree.column("店家名稱", width=100, anchor="center")
        self.tree.heading("飲料名稱", text="飲料名稱")
        self.tree.column("飲料名稱", width=100, anchor="center")
        self.tree.heading("飲料大小", text="飲料大小")
        self.tree.column("飲料大小", width=100, anchor="center")
        self.tree.heading("飲料價格", text="飲料價格")
        self.tree.column("飲料價格", width=100, anchor="center")
        self.tree.grid(column=0, columnspan=3, row=3,ipadx=140,pady=5)

        for item in alls:
            self.tree.insert(
                "",
                tk.END,
                values=item[1:])
        self.update_button = tk.Button(self.search_section, text="修改資料", font=(FONT, 20),
                                       highlightbackground=BACKGROUND_COLOR, command=self.update)
        self.update_button.grid(column=0, row=5,pady=1)
        self.delete_button = tk.Button(self.search_section, text="刪除該筆資料",font=(FONT,20),
                                       highlightbackground=BACKGROUND_COLOR,command=self.delete)
        self.delete_button.grid(column=1, row=5, pady=1)
        self.search_all_button = tk.Button(self.search_section, text="顯示全部資料",font=(FONT,20),
                                           highlightbackground=BACKGROUND_COLOR,
                                           command=self.show_all)
        self.search_all_button.grid(column=2, row=5, pady=1)
    def update_form(self):
        self.update_section.configure(background=BACKGROUND_COLOR)
        self.update_title = tk.Label(self.update_section,
                                     text="修改",
                                     font=(FONT, 30),
                                     fg="black",
                                     background=BACKGROUND_COLOR)
        self.update_title.grid(column=1, row=0)
        self.update_store_name = tk.Entry(self.update_section, background=ENTRYCOLOR, borderwidth=0, font=(FONT, 20),
                                          highlightthickness=0, foreground=FOREGROUND_COLOR)
        self.update_store_name_label = tk.Label(self.update_section, text="店家名稱", font=(FONT, 20),
                                                background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
        self.update_store_name_label.grid(column=0, row=1, padx=5, pady=5)
        self.update_store_name.grid(column=1, columnspan=2, row=1, pady=5,padx=10)

        self.update_drink_name = tk.Entry(self.update_section, background=ENTRYCOLOR, borderwidth=0, font=(FONT, 20),
                                          highlightthickness=0, foreground=FOREGROUND_COLOR)
        self.update_drink_name_label = tk.Label(self.update_section, text="飲料名稱", font=(FONT, 20)
                                                , background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
        self.update_drink_name_label.grid(column=0, row=2, padx=5, pady=5)
        self.update_drink_name.grid(column=1, columnspan=2, row=2, pady=5,padx=10)

        self.update_drink_size = tk.Entry(self.update_section, background=ENTRYCOLOR, borderwidth=0, font=(FONT, 20)
                                          , highlightthickness=0, foreground=FOREGROUND_COLOR)
        self.update_drink_size_label = tk.Label(self.update_section, text="飲料大小", font=(FONT, 20),
                                                background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
        self.update_drink_size_label.grid(column=0, row=3, padx=5, pady=5)
        self.update_drink_size.grid(column=1, columnspan=2, row=3, pady=5,padx=10)

        self.update_drink_price = tk.Entry(self.update_section, background=ENTRYCOLOR, borderwidth=0, font=(FONT, 20),
                                           highlightthickness=0, foreground=FOREGROUND_COLOR)
        self.update_drink_price_label = tk.Label(self.update_section, text="飲料價格", font=(FONT, 20),
                                                 background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
        self.update_drink_price_label.grid(column=0, row=4, padx=5, pady=5)
        self.update_drink_price.grid(column=1, columnspan=2, row=4,padx=10,pady=5)

        self.save_buttion = tk.Button(self.update_section,text="儲存",font=(FONT,20),
                                      highlightbackground=BACKGROUND_COLOR,command=self.save)
        self.save_buttion.grid(column=1, row=5, padx=10)
    def insert_form(self):
        self.insert_section.configure(background=BACKGROUND_COLOR)
        self.insert_title = tk.Label(self.insert_section,
                                     text="新增", font=(FONT,30),
                                     fg="Black",
                                     background=BACKGROUND_COLOR)
        self.insert_title.grid(column=1, row=0)
        self.insert_store_name = tk.Entry(self.insert_section, background=ENTRYCOLOR, borderwidth=0, font=(FONT, 20),
                                          highlightthickness=0, foreground=FOREGROUND_COLOR,width=ENTRYWIDTH)
        self.insert_store_name_label = tk.Label(self.insert_section, text="店家名稱", font=(FONT, 20)
                                                , background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
        self.insert_store_name_label.grid(column=0, row=1, padx=5, pady=5)
        self.insert_store_name.grid(column=1,columnspan=2,row=1, pady=5,padx=10)

        self.insert_drink_name = tk.Entry(self.insert_section, background=ENTRYCOLOR, borderwidth=0, font=(FONT, 20),
                                          highlightthickness=0, foreground=FOREGROUND_COLOR,width=ENTRYWIDTH)
        self.insert_drink_name_label = tk.Label(self.insert_section, text="飲料名稱", font=(FONT, 20)
                                                , background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
        self.insert_drink_name_label.grid(column=0, row=2, padx=5, pady=5)
        self.insert_drink_name.grid(column=1,columnspan=2, row=2, pady=5,padx=10)

        self.insert_drink_size = tk.Entry(self.insert_section, background=ENTRYCOLOR, borderwidth=0, font=(FONT, 20)
                                          , highlightthickness=0, foreground=FOREGROUND_COLOR,width=ENTRYWIDTH)
        self.insert_drink_size_label = tk.Label(self.insert_section, text="飲料大小", font=(FONT, 20),
                                                background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
        self.insert_drink_size_label.grid(column=0, row=3, padx=5, pady=5)
        self.insert_drink_size.grid(column=1,columnspan=2, row=3, pady=5,padx=10)

        self.insert_drink_price = tk.Entry(self.insert_section, background=ENTRYCOLOR, borderwidth=0, font=(FONT, 20),
                                           highlightthickness=0, foreground=FOREGROUND_COLOR,width=ENTRYWIDTH)
        self.insert_drink_price_label = tk.Label(self.insert_section, text="飲料價格", font=(FONT, 20),
                                                 background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
        self.insert_drink_price_label.grid(column=0, row=4, padx=5, pady=5)
        self.insert_drink_price.grid(column=1,columnspan=2, row=4, pady=5,padx=10)

        self.insert_add_buttion = tk.Button(self.insert_section, text="新增", font=(FONT, 20),
                                            highlightbackground=BACKGROUND_COLOR, command=self.add)
        self.insert_add_buttion.grid(column=1, row=5, padx=10)
    def add(self):
        store_name = self.insert_store_name.get()
        drink_name = self.insert_drink_name.get()
        drink_size = self.insert_drink_size.get()
        drink_price = self.insert_drink_price.get()
        if store_name and drink_name and drink_size and drink_price:
            sql = "INSERT INTO drinks ( store_name,drinks,size,price) VALUES (%s,%s,%s,%s)"
            val = (store_name, drink_name, drink_size, drink_price)
            self.data.cursor.execute(sql, val)
            self.data.conn.commit()
            messagebox.showinfo("成功", "資料已新增。")
            self.load_data()
            self.insert_store_name.delete(0, tk.END)
            self.insert_drink_name.delete(0, tk.END)
            self.insert_drink_size.delete(0, tk.END)
            self.insert_drink_price.delete(0, tk.END)
        else:
            messagebox.showinfo(title="錯誤", message="資料不得為空！")
    def load_data(self):
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        self.data.cursor.execute("SELECT * FROM drinks")
        rows = self.data.cursor.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row[1:])
        values = []
        for item in rows:
            if item[1] not in values:
                values.append(item[1])
        self.store.configure(values=values)
    def show_all(self):
        self.data.cursor.execute("SELECT * FROM drinks")
        alls = self.data.cursor.fetchall()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in alls:
            print(item)
            self.tree.insert(
                "",
                tk.END,
                values=item[1:])
    def search(self):
        store = self.store.get()
        sql = "SELECT * FROM drinks WHERE store_name = %s"
        self.data.cursor.execute(sql, (store,))
        alls = self.data.cursor.fetchall()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in alls:
            print(item)
            self.tree.insert(
                "",
                tk.END,
                values=(item[1:]))
    def delete(self):
        item = self.tree.focus()
        if item:
            values = self.tree.item(item, "values")
            store_name, drink_name, size, price = values

            sql = "DELETE FROM drinks WHERE store_name=%s AND drinks=%s AND size=%s AND price=%s"
            value = (store_name, drink_name, size, price)
            self.data.cursor.execute(sql, value)
            self.data.conn.commit()

            self.tree.delete(item)
            messagebox.showinfo("成功刪除", "已成功刪除該筆資料！")
            self.data.cursor.execute("SELECT * FROM drinks")
            alls = self.data.cursor.fetchall()
            values = []
            for item in alls:
                if item[1] not in values:
                    values.append(item[1])
            self.store.configure(values=values)

        else:
            messagebox.showinfo("錯誤", "未刪除資料！")
    def update(self):
        if not self.tree.focus():
            messagebox.showinfo("注意","請點選要修改的品項！\n 並在下方修改")
        else:
            item = self.tree.focus()
            values = self.tree.item(item,"values")
            self.original_store,self.original_drink,self.original_size,self.original_price = values
            print(self.update_store_name.insert(0,self.original_store))
            self.update_drink_name.insert(0,self.original_drink)
            self.update_drink_size.insert(1,self.original_size)
            self.update_drink_price.insert(0,self.original_price)
    def save(self):
        sql="""
            UPDATE drinks
            SET store_name = %s, drinks =%s, size = %s, price = %s
            WHERE  store_name = %s AND drinks =%s AND size = %s AND price = %s
        """
        values = (self.update_store_name.get(),self.update_drink_name.get(),self.update_drink_size.get(),self.update_drink_price.get(),
                  self.original_store, self.original_drink, self.original_size, self.original_price)
        self.data.cursor.execute(sql,values)
        self.data.conn.commit()
        self.load_data()
        self.update_store_name.delete(0,tk.END)
        self.update_drink_name.delete(0,tk.END)
        self.update_drink_size.delete(0,tk.END)
        self.update_drink_price.delete(0,tk.END)

