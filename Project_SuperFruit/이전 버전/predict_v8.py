'''
DB누적 입력+id테이블 추가
크롤링 폴더 초기화 추가

-----------------------------------------
'''
import tkinter,os, random,requests,urllib,pymysql,re
import tensorflow as tf
import matplotlib.pyplot as plt
from pandas import DataFrame
from PIL import Image, ImageTk
from lxml.html import parse
from io import StringIO
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm
import matplotlib

def random_file():
    randomfile_path = "C:/test"
    random_filename = random.choice([x for x in os.listdir(randomfile_path) if os.path.isfile(os.path.join(randomfile_path, x))])
    image_dir = "C:/test/" + str(random_filename)
    return image_dir

def fileload(image_dir):
    befo_resize=Image.open(image_dir)
    befo_resize = befo_resize.resize((int(befo_resize.width / befo_resize.height * 300), 300))
    image = ImageTk.PhotoImage(befo_resize)
    return image

def image_change():
    global active,image,image_dir,name,score,url,num

    if active==0:

        button1.config(text='다음 사진')

        try:
            a,b=main(image_dir)
            b_max_index=b.index(max(b))
            label3.config(text='%s  %.2f%%'%(a[b_max_index],b[b_max_index]),font=(60))
            df = DataFrame({'name': a, 'score': b}).sort_values(by=['score', 'name'], ascending=[False,True])
            mat_plot(df)
            try:
                sql = "Insert into `fruits1` (`name`, `score`) values (%s, %s) "
                cursor.execute(sql,(str(a[b_max_index]), str(b[b_max_index])))
                sql = "Insert into `fruits2` (`name`, `keyword`, `dir`) values (%s, %s, %s) "
                tmp1=image_dir.lstrip('C:/test/').rstrip('.jpg')
                tmp2=re.findall('\d+',tmp1)[0]
                tmp1=tmp1.rstrip(tmp2)
                cursor.execute(sql,(str(a[b_max_index]),str(tmp1), str(tmp2)))
                connection.commit()
            except:
                label3.config(text='DB 테이블에 중복 다음사진을 누르세요')
        except:
            label3.config(text='이미지오류 다음 사진을 누르셈')
        active=1
        num = num + 1


    else:
        image_dir=random_file()
        image = fileload(image_dir)
        button1.config(text='확 인')
        frame2_1.forget()
        label2.config(image=image,text=None)
        active = 0

def main(image_dir):
    global name,score
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
        name=[]
        score=[]
        for i in range(len(labels)):
            name.append(labels[i])
            score.append(prediction[0][i]*100)
    except:
        label3.config(text='인공지능이 작동하지 않습니다')
    return name, score

def crawling():
    global image, image_dir,url
    keyword = input.get()
    outpath = "C:/test/"
    label5.config(text=keyword+' 검색중')
    url = 'https://www.google.co.kr/search?q=' + keyword + '&source=lnms&tbm=isch&sa=X&ved=0ahUKEwic-taB9IXVAhWDHpQKHXOjC14Q_AUIBigB&biw=1842&bih=990'
    imgs = parse(StringIO(requests.get(url).text)).getroot().findall('.//img')
    t = 0
    try:
        label2.config(image=None)
        for file in os.scandir(outpath):
            os.remove(file.path)
    except:
        None
    for a in imgs:
        url = a.get('src')
        if not os.path.isdir(outpath):
            os.makedirs(outpath)
        outfile = keyword+str(t) + '.jpg'
        try:
            if url != None:
                urllib.request.urlretrieve(url, outpath + outfile)
        except:
            None
        t += 1
    image_dir = random_file()
    image = fileload(image_dir)
    label2.config(image=image)
    label5.config(text=keyword + ' - 검색 완료')
    label3.config(text='확인을 누르세요')

def mat_plot(df):
    global frame3,chart_type,chart,frame4
    df = df[['name', 'score']].groupby('name').sum().sort_values(by=['score', 'name'], ascending=[False,True]).head(4)
    figure = plt.Figure(figsize=(5,3))
    ax = figure.add_subplot(111)
    chart_type = FigureCanvasTkAgg(figure, frame4)
    chart=chart_type.get_tk_widget()
    chart.grid(row=0,column=0)
    df.plot(kind='bar', ax=ax, color='red',legend=False)
    ax.set_title('최고 확률이 나온 탑4')
    ax.set_xticklabels(df.index.tolist(),rotation=0)
    ax.set_xlabel(None)
    yticks = ax.get_yticks()
    ax.set_yticklabels(['{}%'.format(int(x)) for x in yticks])
    for a, b in enumerate(df.values):
        ax.text(a-0.18, 15, (str(round(float(b),1))+'%'),color='black')
    frame4.pack()


connection = pymysql.connect(host='localhost',user='root',password='123123',db='abc_db',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
matplotlib.rc('font', family = fm.FontProperties(fname = 'C:/Windows/Fonts/HBATANG.ttf').get_name())



def init_sql():
    sql = "DROP TABLE IF EXISTS `ID`"
    cursor.execute(sql)
    sql = "DROP TABLE IF EXISTS `fruits1`"
    cursor.execute(sql)
    sql = "DROP TABLE IF EXISTS `fruits2`"
    cursor.execute(sql)
    sql = """ CREATE TABLE `ID` (`id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,`Username` VARCHAR(45) NOT NULL,`Password` VARCHAR(45) NOT NULL);"""
    cursor.execute(sql)
    sql = """INSERT INTO `ID` (`Username`, `Password`) VALUES('admin', '1234');"""
    cursor.execute(sql)
    sql = """ CREATE TABLE `fruits1` (`num` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,`name` VARCHAR(45) NOT NULL,`score` DOUBLE NOT NULL);"""
    cursor.execute(sql)
    sql = """ CREATE TABLE `fruits2` (`num` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,`name` VARCHAR(45) NOT NULL,`keyword` VARCHAR(45) NOT NULL,`dir` VARCHAR(45) NOT NULL);"""
    cursor.execute(sql)

cursor = connection.cursor()
init_sql()

active=0
num=0
image_dir=None
window=tkinter.Tk()
window.title("과일분류 프로그램")
window.geometry("700x950")
label1 = tkinter.Label(window,text='과일 판독기')

frame1=tkinter.Frame(window)
label4 = tkinter.Label(frame1,text='입력:')
label5 = tkinter.Label(frame1,text='검색결과없음')
input=tkinter.Entry(frame1,width=50,text='')
button2 = tkinter.Button(frame1,text='검색',command=crawling)
label4.grid(row=0,column=0)
input.grid(row=0,column=1)
button2.grid(row=0,column=2)
label5.grid(row=1,columnspan=3)
frame2=tkinter.Frame(window)
frame2_1=tkinter.Frame(frame2,height=283)
frame2_1.pack(fill='y',expand=True)
label2 = tkinter.Label(frame2,image=None,text='불러오기중')
label2.pack()
frame3=tkinter.Frame(window)
button1 = tkinter.Button(frame3, width=15, command=image_change, text='크롤링or눌러주세요')
button1.pack()
frame4=tkinter.Frame(frame3)
label3 = tkinter.Label(frame3,text='이미지 안넣어서 오류뜰거임')
label3.pack()
frame4.pack(fill='both',expand=True)
label1.pack()
frame1.pack()
frame2.pack()
frame3.pack()

window.mainloop()