from lpr import plate_recognition as recognize
import cv2, os, shutil, glob, json
from PIL import Image,ImageDraw

def draw_box(img,box,copy=True,width=5,outline='red',fill=None):
    box=tuple(box)
    if copy:
        img=img.copy()
    draw=ImageDraw.Draw(img)
    draw.rectangle((box[:2],box[2:]),width=width,outline=outline,fill=fill)
    return img
def val_dir(dir, results_file, error_img_dir=None):
    fs = glob.glob(dir + '/*.jpg')
    results = {}
    if error_img_dir:
        if os.path.exists(error_img_dir):
            shutil.rmtree(error_img_dir)
        if not os.path.exists(error_img_dir):
            os.makedirs(error_img_dir)
    for i, f in enumerate(fs):
        img = cv2.imread(f)
        # print(img.shape[:-1][::-1])
        # img=cv2.resize()
        lable = os.path.basename(f).split('.')[0]
        plates = recognize(img)
        print(plates)
        if plates:
            plate = plates[0][0]
        else:
            plate = None
        res = {
            'label': lable, 'pred': plate, 'correct': lable == plate
        }
        results[os.path.basename(f)] = res
        print(i, f, res)

        if not res['correct'] and error_img_dir:
        # if error_img_dir:
            path = error_img_dir + '/' + os.path.basename(f).replace('.jpg', '_%s.jpg' % (plate))
            img=Image.open(f)
            if plates:
                img=draw_box(img,plates[0][-1])
            img.save(path)

    total = len(results)
    corrects = 0
    for f, res in results.items():
        if res['correct']:
            corrects += 1
    accuracy = corrects / total
    acc_str = '%.1f' % (accuracy * 100) + '%'
    print(total, corrects, acc_str)
    with open(results_file, 'w') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    val_dir(
        '/home/ars/disk/data/紫光云/licenseplate-testcase-basecase',
        'results.json',
        error_img_dir='/home/ars/disk/data/紫光云/lpr-errors'
    )

