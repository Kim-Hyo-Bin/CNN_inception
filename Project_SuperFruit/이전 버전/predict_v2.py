'''
tkinter+predict
처음 시작할때 사진없이 시작(경로설정+문자열바꾸면 바뀜)
이미지파일 불러올때 자동 크기조절(높이300p기준)
predict과정에서 확률+해당명칭 인덱스로 다중으로 찾기가능
기본값으로 최대값으로 넣어둠
'''
import tkinter,os, random
import tensorflow as tf
from PIL import Image, ImageTk

def random_file():
    randomfile_path = "C:/Users/user/PycharmProjects/projectABC/abc/tmp/flower_photos/sunflowers"
    random_filename = random.choice([x for x in os.listdir(randomfile_path) if os.path.isfile(os.path.join(randomfile_path, x))])
    image_dir = "C:/Users/user/PycharmProjects/projectABC/abc/tmp/flower_photos/sunflowers/" + str(random_filename)
    return image_dir

def fileload(image_dir):
    befo_resize=Image.open(image_dir)
    befo_resize = befo_resize.resize((int(befo_resize.width / befo_resize.height * 300), 300))#높이를 300으로 고정시키고 가로크기만 바뀜
    image = ImageTk.PhotoImage(befo_resize)
    return image

def image_change():
    global active,image,image_dir

    if active==0:
        button1.config(text='다음 사진')
        try:
            a,b=main(image_dir)
            b_max_index=b.index(max(b))
            label2.config(text='%s  %.2f%%'%(a[b_max_index],b[b_max_index]))
        except:
            label2.config(text='이미지오류 다음 사진을 누르셈')
        active=+1

    else: #라벨1의 이미지가 교체
        image_dir=random_file()
        image = fileload(image_dir)
        button1.config(text='확 인')
        label1.config(image=image)
        active = 0

def main(image_dir):
    labels = [line.rstrip() for line in tf.gfile.GFile("./tmp/output_labels.txt")]#학습한 종류를 저장해놓음
    try:
        with tf.gfile.FastGFile("./tmp/output_graph.pb", 'rb') as fp: #학습데이터
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(fp.read())
            tf.import_graph_def(graph_def, name='')
        with tf.Session() as sess: #여기서 예측함
            logits = sess.graph.get_tensor_by_name('final_result:0')
            image = tf.gfile.FastGFile(image_dir, 'rb').read()
            prediction = sess.run(logits, {'DecodeJpeg/contents:0': image})
        name=[]
        score=[]
        for i in range(len(labels)):
            name.append(labels[i])
            score.append(prediction[0][i]*100)
    except:
        None

    return name, score

active=0
image_dir=None
window=tkinter.Tk()
window.title("과일분류 프로그램")
window.geometry("500x400")
label1 = tkinter.Label(image=None)
label1.pack()

button1 = tkinter.Button(window, width=15, command=image_change, text='확인')
button1.pack()
label2 = tkinter.Label(text='이미지 안넣어서 오류뜰거임')
label2.pack()
window.mainloop()