import tkinter,os, random
import tensorflow as tf
from PIL import Image, ImageTk

def random_file():
    randomfile_path = "C:/Users/user/PycharmProjects/projectABC/abc/tmp/flower_photos/sunflowers"
    random_filename = random.choice([x for x in os.listdir(randomfile_path) if os.path.isfile(os.path.join(randomfile_path, x))])
    # ("C:/Users/user/PycharmProjects/projectABC/abc/tmp/flower_photos/sunflowers/" + str(random_filename))
    image_dir = "C:/Users/user/PycharmProjects/projectABC/abc/tmp/flower_photos/sunflowers/" + str(random_filename)
    return image_dir

def fileload(image_dir):
    befo_resize=Image.open(image_dir)
    if befo_resize.width/befo_resize.height>1.5:
        befo_resize = befo_resize.resize((int(befo_resize.height / befo_resize.width * 400), 400))
    else:
        befo_resize = befo_resize.resize((int(befo_resize.width / befo_resize.height * 300),int(befo_resize.height / befo_resize.width*300)))

    image = ImageTk.PhotoImage(befo_resize)
    return image

def asdf(): #인공지능돌아가고 결과값을 라벨2에 출력
    global active,image,image_dir

    if active==0:
        button1.config(text='다음 사진')
        a,b=main(image_dir)
        b_max_index=b.index(max(b))
        label2.config(text='%s  %.2f%%'%(a[b_max_index],b[b_max_index]))
        active=+1

    else: #라벨1의 이미지가 교체
        image_dir=image_dir=random_file()
        image = fileload(image_dir)
        button1.config(text='확 인')
        label1.config(image=image)
        active = 0

def main(image_dir):
    labels = [line.rstrip() for line in tf.gfile.GFile("./tmp/output_labels.txt")]#학습한 종류를 저장해놓음
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
    return name, score

active=0
image_dir='샘플데이터.jpg'
window=tkinter.Tk()
window.title("과일분류 프로그램")
window.geometry("500x400")
#window.resizable(False, False) 기본값트루 크기조절가능불가
label1 = tkinter.Label(image=None)
image = fileload(image_dir)
label1.config(image=image)
label1.pack()

button1 = tkinter.Button(window, width=15, command=asdf, text='확인')
button1.pack()
label2 = tkinter.Label(text='입력값이없습니다')
label2.pack()
window.mainloop()