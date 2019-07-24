import tensorflow as tf
import matplotlib.pyplot as plt
from pandas import DataFrame
from lxml.html import parse
from io import StringIO
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm
import matplotlib
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

connection = pymysql.connect(host='localhost',user='root',password='123123',db='abc_db',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
matplotlib.rc('font', family = fm.FontProperties(fname = 'C:/Windows/Fonts/HBATANG.ttf').get_name())
cursor = connection.cursor()

class loggin(): #로그인창 완성 일부러 loggin한거니까 태클 ㄴㄴ
    def __init__(self,window):
        self.window=window
        self.window.title("과일분류 프로그램 - 로그인창")
        self.window.geometry("300x150+800+300")

        self.ID_data = StringVar()
        self.password_data = StringVar()

        self.login_info = Label(window, text="아이디 비번입력 ㄱ")
        self.login_info.pack()
        self.login_id_label = Label(window, text="ID입력창").pack()
        self.username_login_entry = Entry(window, textvariable=self.ID_data)
        self.username_login_entry.pack()
        self.login_pass_label = Label(window, text="비밀번호 입력창").pack()
        self.password__login_entry = Entry(window, textvariable=self.password_data, show='*')
        self.password__login_entry.pack()
        self.login_btn = Button(window, text="Login", width=10, command=self.Check_ID).pack()

    def Check_ID(self):
        try:
            sql = 'SELECT * FROM `ID` WHERE `Username` = %s'
            cursor.execute(sql, (self.ID_data.get()), )
            result = cursor.fetchone()
            if result['Password'] == self.password_data.get():
                self.window.withdraw()
                self.newWindow = Toplevel(self.window)
                Sub = main_gui(self.newWindow)

            else:
                print('비번오류')

        except:
            print('아이디 오류')

    def newWindow(self):
        self.window.withdraw()
        self.newWindow = Toplevel(self.window)


class main_gui():
    active=0
    num=0
    def __init__(self, newWindow):
        self.page_index = 0
        self.page_num=[1,2,3]
        self.window = newWindow
        self.window.title("과일분류 프로그램")
        self.window.geometry("800x800+600+100")
        self.button_befo = Button(self.window, text=' < ', font=20, command=self.change_page_befo)
        self.button_next = Button(self.window, text=' > ', font=20, command=self.change_page_next)
        self.button_befo.pack(side='left')
        self.button_next.pack(side='right')

        self.top_frame1 = Frame(self.window)
        self.top_frame1.pack(expand=True, fill='both')

        self.frame1 = Frame(self.top_frame1)
        self.frame2 = Frame(self.top_frame1)
        self.frame3 = Frame(self.top_frame1)
        self.frame4 = Frame(self.top_frame1)
        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.frame4.pack()

        self.label1 = Label(self.frame1, text='과일 판독기',font=20 ,pady=10 )
        self.label4 = Label(self.frame1, text='입력:')
        self.label5 = Label(self.frame1, text='검색결과없음')
        self.input = Entry(self.frame1, width=50, text='')
        self.button2 = Button(self.frame1, text='검색', command=self.crawling)
        self.label1.grid(row=0, columnspan=3)
        self.label4.grid(row=1, column=0)
        self.input.grid(row=1, column=1)
        self.button2.grid(row=1, column=2)
        self.label5.grid(row=2, columnspan=3)

        self.frame2_1 = Frame(self.frame2, height=283, width=500)
        self.label2 = Label(self.frame2, image=None, text='불러오기중')
        self.frame2_1.pack(fill='y', expand=True)
        self.label2.pack()

        self.button1 = Button(self.frame3, width=15, command=self.image_change, text='크롤링or눌러주세요')
        self.label3 = Label(self.frame3, text='이미지 안넣어서 오류뜰거임')
        self.button1.pack()
        self.label3.pack()

        self.top_frame2 = Frame(self.window)
        self.labelf2_1= Label(self.top_frame2,text='관리자 데이터베이스',font=20,pady=10)
        self.labelf2_1.pack()

        self.labelf2_2 = Label(self.top_frame2, text='관리자',padx=10)
        self.labelf2_3 = Label(self.top_frame2, text='지역',padx=10)
        self.labelf2_4 = Label(self.top_frame2, text='지점명',padx=10)
        self.labelf2_1.grid(row=0,columnspan=2)
        self.labelf2_2.grid(row=1, column=0)
        self.labelf2_3.grid(row=2, column=0)
        self.labelf2_4.grid(row=3, column=0)
        self.Entryf2_1 = Entry(self.top_frame2, width=50)
        self.Entryf2_2 = Entry(self.top_frame2, width=50)
        self.Entryf2_3 = Entry(self.top_frame2, width=50)
        self.Entryf2_1.insert(0, 'admin')
        self.Entryf2_2.insert(0, 'Null')
        self.Entryf2_3.insert(0, 'Null')
        self.Entryf2_1.grid(row=1, column=1)
        self.Entryf2_2.grid(row=2, column=1)
        self.Entryf2_3.grid(row=3, column=1)
        self.Entryf2_1.config(state='readonly')
        self.Entryf2_2.config(state='readonly')
        self.Entryf2_3.config(state='readonly')
        self.framef2_buttonframe = Frame(self.top_frame2,pady=10)
        self.buttonf2_1=Button(self.framef2_buttonframe,text='새로고침',command=self.f2_renew)
        self.framef2_buttonframe.grid(row=4,columnspan=2)
        self.buttonf2_1.pack()
        # self.lable2_logo=Label(self.top_frame2,image=None,bg='red')
        # self.lable2_logo.grid(row=1,column=2,rowspan=3)

        self.Treeviewf2_1_frame=Frame(self.top_frame2, padx=10)
        self.Treeviewf2_1_frame.grid(row=5,columnspan=2)
        self.Treeviewf2_1_info = ['ID', '실제과일', '예측과일', '인식률']
        self.Treeviewf2_1 = ttk.Treeview(self.Treeviewf2_1_frame, columns=self.Treeviewf2_1_info)
        self.ysb = ttk.Scrollbar(self.Treeviewf2_1_frame,orient=VERTICAL, command=self.Treeviewf2_1.yview)
        self.xsb = ttk.Scrollbar(self.Treeviewf2_1_frame,orient=HORIZONTAL, command=self.Treeviewf2_1.xview)
        self.Treeviewf2_1['yscroll'] = self.ysb.set
        self.Treeviewf2_1['xscroll'] = self.xsb.set
        self.Treeviewf2_1.heading('#0', text='ID')
        self.Treeviewf2_1.heading('#1', text='실제과일')
        self.Treeviewf2_1.heading('#2', text='예측과일')
        self.Treeviewf2_1.heading('#3', text='인식률')
        self.Treeviewf2_1.column('#0', stretch=YES,minwidth=50,width=50)
        self.Treeviewf2_1.column('#1', stretch=YES,minwidth=100,width=150)
        self.Treeviewf2_1.column('#2', stretch=YES,minwidth=100,width=150)
        self.Treeviewf2_1.column('#3', stretch=YES,minwidth=100,width=150)
        self.ysb.pack(side='right', fill='y', expand=True)
        self.xsb.pack(side='bottom', fill='x', expand=True)
        self.Treeviewf2_1.pack()
        self.Treeviewf2_1.rowconfigure(0, weight=1)
        self.Treeviewf2_1.columnconfigure(0, weight=1)

        self.top_frame3 = Frame(self.window)
        self.labelf3_1 = Label(self.top_frame3, text='현재 대상의 모든 확률그래프',font=20,pady=10)
        self.labelf3_1.pack()
        self.framef3_1 = Frame(self.top_frame3)
        self.framef3_2 = Frame(self.framef3_1)
        self.framef3_1.pack()
        self.labelf3_2 = Label(self.framef3_1, text='설명 ㄱㄱ')
        self.labelf3_2.pack()
        self.buttonf3_1 = Button(self.framef3_1,text='새로 고침',command=self.f3_renew)
        self.buttonf3_1.pack()


    def f3_renew(self):

        self.figure = plt.Figure(figsize=(7, 4))
        self.chart_type = FigureCanvasTkAgg(self.figure, self.framef3_2)
        self.chart = self.chart_type.get_tk_widget()
        self.chart.grid(row=0, column=0)
        self.df.set_index('name')

        ax1 = self.figure.add_subplot(122)

        self.df.plot(kind='pie',y='score',subplots=True, figsize=(5, 4),ax=ax1,autopct='%1.1f%%', startangle=90, labels=self.df['name'], legend = True, fontsize=10)
        ax1.set_title('All Predict')
        ax1.set_ylabel(None)
        ax1.legend(bbox_to_anchor=(-0.6, 1.1),loc=1, ncol=2, mode="expand", borderaxespad=0.)
        # ax2 = self.figure.add_subplot(122)

        # self.df.plot(kind='pie',y='score',subplots=True, figsize=(0, 0),ax=ax2,labels=self.df['name'], legend = True)
        # ax2.axis('off')
        self.framef3_2.pack()

    def f2_renew(self):
        self.Treeviewf2_1.delete(*self.Treeviewf2_1.get_children())
        sql = 'SELECT * FROM `fruits1`'
        cursor.execute(sql)
        self.rows1 = cursor.fetchall()
        sql = 'SELECT * FROM `fruits2`'
        cursor.execute(sql)
        self.rows2 = cursor.fetchall()

        for x in range(len(self.rows1)):
               self.Treeviewf2_1.insert('', 'end', text=self.rows1[x].get('num'), values=(self.rows2[x].get('keyword'),self.rows1[x].get('name'),self.rows1[x].get('score')))


    def change_page_next(self):
        self.page_index=(self.page_index+1) %3
        eval('self.top_frame%s.pack()'%(self.page_num[self.page_index]))
        try:
            eval(str('self.top_frame%s.forget()' % str(self.page_num[(self.page_index + 1) % 3])))
            eval(str('self.top_frame%s.forget()' % str(self.page_num[(self.page_index - 1) % 3])))
        except:
            print('error')


    def change_page_befo(self):
        self.page_index = (self.page_index-1) % 3
        eval('self.top_frame%s.pack()'%(self.page_num[self.page_index]))
        try:
            eval(str('self.top_frame%s.forget()' % str(self.page_num[(self.page_index + 1) % 3])))
            eval(str('self.top_frame%s.forget()' % str(self.page_num[(self.page_index - 1) % 3])))
        except:
            print('error')



    def crawling(self):
        self.keyword = self.input.get()
        self.outpath = "C:/test/"
        self.label5.config(text=self.keyword + ' 검색중')
        self.url = 'https://www.google.co.kr/search?q=' + self.keyword + '&source=lnms&tbm=isch&sa=X&ved=0ahUKEwic-taB9IXVAhWDHpQKHXOjC14Q_AUIBigB&biw=1842&bih=990'
        self.imgs = parse(StringIO(requests.get(self.url).text)).getroot().findall('.//img')
        self.t = 0
        try:
            self.label2.config(image=None)
            for file in os.scandir(self.outpath):
                os.remove(file.path)
        except:
            None
        for a in self.imgs:
            self.url = a.get('src')
            if not os.path.isdir(self.outpath):
                os.makedirs(self.outpath)
            self.outfile = self.keyword + str(self.t) + '.jpg'
            try:
                if self.url != None:
                    urllib.request.urlretrieve(self.url, self.outpath + self.outfile)
            except:
                None
            self.t += 1
        self.image_dir = alpha.random_file()
        self.image = alpha.fileload(self.image_dir)
        self.frame2_1.forget()
        self.label2.config(image=self.image)
        self.label5.config(text=self.keyword + ' - 검색 완료')
        self.label3.config(text='확인을 누르세요')

    def image_change(self):


        if self.active == 0:

            self.button1.config(text='다음 사진')

            try:

                connection.commit()


                a, b = self.main(self.image_dir)
                b_max_index = b.index(max(b))
                self.label3.config(text='%s  %.2f%%' % (a[b_max_index], b[b_max_index]), font=(60))
                self.df = DataFrame({'name': a, 'score': b}).sort_values(by=['score', 'name'], ascending=[False, True])
                self.mat_plot(self.df)
                try:
                    sql = "Insert into `fruits1` (`name`, `score`) values (%s, %s) "
                    cursor.execute(sql, (str(a[b_max_index]), str(b[b_max_index])))
                    sql = "Insert into `fruits2` (`name`, `keyword`, `dir`) values (%s, %s, %s) "
                    tmp1 = self.image_dir.lstrip('C:/test/').rstrip('.jpg')
                    tmp2 = re.findall('\d+', tmp1)[0]
                    tmp1 = tmp1.rstrip(tmp2)
                    cursor.execute(sql, (str(a[b_max_index]), str(tmp1), str(tmp2)))
                    sql = "Insert into `fruits3` (`name`, `score`) values (%s, %s) "
                    # Execute sql.
                    for i in range(self.df.shape[0]):
                        cursor.execute(sql, (self.df.values[i][0], self.df.values[i][1]))
                    connection.commit()
                except:
                    self.label3.config(text='DB 테이블에 중복 다음사진을 누르세요')
            except:
                self.label3.config(text='이미지오류 다음 사진을 누르셈')
            self.active = 1
            self.num = self.num + 1


        else:
            self.image_dir = alpha.random_file()
            self.image =  alpha.fileload(self.image_dir)
            self.button1.config(text='확 인')
            self.frame2_1.forget()
            self.active = 0
            self.label2.config(image=self.image, text=None)


    def main(self,image_dir):
        labels = [line.rstrip() for line in tf.gfile.GFile("./tmp/output_labels.txt")]
        try:
            with tf.gfile.FastGFile("./tmp/output_graph.pb", 'rb') as fp:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(fp.read())
                tf.import_graph_def(graph_def, name='')
            with tf.Session() as sess:
                logits = sess.graph.get_tensor_by_name('final_result:0')
                image = tf.gfile.FastGFile(image_dir, 'rb').read()
                prediction = sess.run(logits, {'DecodeJpeg/contents:0': image})
            self.name = []
            self.score = []
            for i in range(len(labels)):
                self.name.append(labels[i])
                self.score.append(prediction[0][i] * 100)
        except:
            self.label3.config(text='인공지능이 작동하지 않습니다')
        return self.name, self.score

    def mat_plot(self,df):
        df = df[['name', 'score']].groupby('name').sum().sort_values(by=['score', 'name'],ascending=[False, True]).head(4)
        self.figure = plt.Figure(figsize=(5, 3))
        ax = self.figure.add_subplot(111)
        self.chart_type = FigureCanvasTkAgg(self.figure, self.frame4)
        self.chart = self.chart_type.get_tk_widget()
        self.chart.grid(row=0, column=0)
        df.plot(kind='bar', ax=ax, color='red', legend=False)
        ax.set_title('최고 확률이 나온 탑4')
        ax.set_xticklabels(df.index.tolist(), rotation=0)
        ax.set_xlabel(None)
        yticks = ax.get_yticks()
        ax.set_yticklabels(['{}%'.format(int(x)) for x in yticks])
        for a, b in enumerate(df.values):
            ax.text(a - 0.18, 15, (str(round(float(b), 1)) + '%'), color='black')
        self.frame4.pack()

class alpha:
    def random_file():
        randomfile_path = "C:/test"
        random_filename = random.choice(
            [x for x in os.listdir(randomfile_path) if os.path.isfile(os.path.join(randomfile_path, x))])
        image_dir = "C:/test/" + str(random_filename)
        return image_dir

    def fileload(image_dir):
        befo_resize = Image.open(image_dir)
        befo_resize = befo_resize.resize((int(befo_resize.width / befo_resize.height * 300), 300))
        image = ImageTk.PhotoImage(befo_resize)
        return image

    def init_sql():
        sql = "DROP TABLE IF EXISTS `ID`"
        cursor.execute(sql)
        sql = "DROP TABLE IF EXISTS `fruits1`"
        cursor.execute(sql)
        sql = "DROP TABLE IF EXISTS `fruits2`"
        cursor.execute(sql)
        sql = "DROP TABLE IF EXISTS `fruits3`"
        cursor.execute(sql)
        sql = """ CREATE TABLE `ID` (`id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,`Username` VARCHAR(45) NOT NULL,`Password` VARCHAR(45) NOT NULL);"""
        cursor.execute(sql)
        sql = """INSERT INTO `ID` (`Username`, `Password`) VALUES('admin', '1234');"""
        cursor.execute(sql)
        sql = """ CREATE TABLE `fruits1` (`num` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,`name` VARCHAR(45) NOT NULL,`score` DOUBLE NOT NULL);"""
        cursor.execute(sql)
        sql = """ CREATE TABLE `fruits2` (`num` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,`name` VARCHAR(45) NOT NULL,`keyword` VARCHAR(45) NOT NULL,`dir` VARCHAR(45) NOT NULL);"""
        cursor.execute(sql)
        sql = """ CREATE TABLE `fruits3` (`name` VARCHAR(45) NOT NULL,`score` DOUBLE NOT NULL,PRIMARY KEY(`name`, `score`));"""
        cursor.execute(sql)




def main():
    alpha.init_sql()
    window = Tk()
    loggin(window)
    window.mainloop()

if __name__ == "__main__":
    main()</pre>