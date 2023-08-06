from lpr import plate_recognition as recognize
import cv2, os, shutil, glob, json

def scale_img(img,factor):
    w,h=img.shape[:-1][::-1]
    w=int(w*factor)
    h=int(h*factor)
    img=cv2.resize(img,(w,h))
    return img
def val_dir(dir, results_file):
    fs = glob.glob(dir + '/*.jpg')
    results = {}
    for i, f in enumerate(fs):
        img = cv2.imread(f)
        lable = os.path.basename(f).split('.')[0]
        best_plate=None
        scales = [0.5, 1, 1.5]
        for scale in scales:
            im=scale_img(img.copy(),scale)
            plates = recognize(im)
            if plates:
                if not best_plate or best_plate[1]<plates[0][1]:
                    best_plate=plates[0]
        plate=best_plate[0]

        res = {
            'label': lable, 'pred': plate, 'correct': lable == plate
        }
        results[os.path.basename(f)] = res
        print(i, f, res)
    total = len(results)
    corrects = 0
    for f, res in results.items():
        if res['correct']:
            corrects += 1
    accuracy = corrects / total
    acc_str = '%.1f' % (accuracy * 100)+'%'
    print(total, corrects, acc_str)
    with open(results_file, 'w') as f:
        json.dump(results,f,ensure_ascii=False,indent=4)


if __name__ == '__main__':
    val_dir(
        '/home/ars/disk/data/紫光云/licenseplate-testcase-basecase',
        'results.json'
    )

