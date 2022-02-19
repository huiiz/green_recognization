from time import sleep
from flask import Flask, jsonify, request, make_response
from flask_cors import cross_origin
import threading
from count_area import calculate_area
# from seg_tif import get_seg_count, get_seg_total
# from change import seg_and_change, get_change_count
from unet.predict import u_predict, get_u_predict_ls, get_u_total_count, stop_u_predict
from deeplab.predict import d_predict, get_d_predict_ls, get_d_total_count, stop_d_predict
from common import *
from get_gif import create_gif
app = Flask(__name__)

path = ''
img_path = ''
net = '0'


@app.route('/')
@cross_origin()
def homepage():
    return jsonify({
        'code': 0,
        'msg': 'ok'
    })

# 启动程序时，用来初始化程序路径


@app.route('/set_path', methods=['GET'])
def set_path():
    is_development = request.args.get('is_d')
    global path
    if not path:
        path = './pydist/app' if is_development == '1' else './resources/pydist/app'
        # make_folds(path, ('tif_file', 'tif_temp', 'png_temp', 'result_temp'))
        make_folds(path, ('result_temp',))

        return jsonify({
            'code': 0,
            'msg': 'success to set path'
        })
    else:
        return jsonify({
            'code': -1,
            'msg': 'path has been set before'
        })


# 设置网络
@app.route('/set_net', methods=['GET'])
def set_net():
    global net
    net = request.args.get('net')
    return jsonify({
        'code': 0,
        'msg': 'success to set net'
    })


@app.route('/set_img_path', methods=['GET'])
def set_img_path():
    # return os.getcwd()
    global img_path
    img_path = request.args.get('img_path')
    return jsonify({
        'code': 0,
        'msg': 'success to set img path'
    })


# 上传tif文件
# @app.route('/img', methods=['POST'])
# def img():
#     # return os.getcwd()
#     if not path:
#         with open('a.txt', 'w') as f:
#             f.write('aaa')
#     tif_file = request.files.get('tif_file')
#     file_path = f'{path}/tif_file/to_predict.tif'
#     # print(file_path)
#     tif_file.save(file_path)
#     print(path)
#     t = threading.Thread(target=seg_and_change, args=(path,))
#     t.start()
#     return jsonify({
#         'code': 0,
#         'msg': 'success to upload'
#     })


@app.route('/get_total', methods=['GET'])
def get_total():
    # x_count, y_count, seg_total = get_seg_total()
    if net == '0':
        total_count = get_u_total_count()
    elif net == '1':
        total_count = get_d_total_count()
    else:
        total_count = 0
    return jsonify({
        'code': 0,
        'msg': 'success to get the total',
        'data': {
            'total_count': total_count
        }
    })

# # 分割进度
# @app.route('/seg_process', methods=['GET'])
# def seg_process():
#     seg_count = get_seg_count()
#     change_count = get_change_count()
#     return jsonify({
#         'code': 0,
#         'msg': 'success to get the count',
#         'data': {
#             'seg_count': seg_count,
#             'change_count': change_count
#         }
#     })


@app.route('/predict', methods=['GET'])
def predict():
    # x_count, y_count, _ = get_seg_total()
    num = request.args.get('num')
    try:
        clear_fold(path, 'result_temp')
    except:
        pass
    if net == '0':
        # u_predict(path)
        t = threading.Thread(target=u_predict, args=(path, img_path, num))
        t.start()
    elif net == '1':
        # d_predict(path, x_count, y_count)
        t = threading.Thread(target=d_predict, args=(path, img_path, num))
        t.start()
    return jsonify({
        'code': 0,
        'msg': 'begin to predict'
        })

# 获得预测进度
@app.route('/pre_process', methods=['GET'])
def pre_process():
    if net == '0':
        predict_ls = get_u_predict_ls()
        total_count = get_u_total_count()
    elif net == '1':
        predict_ls = get_d_predict_ls()
        total_count = get_d_total_count()
    else:
        predict_ls = []
        total_count = 0
    return jsonify({
        'code': 0,
        'msg': 'success to get the count',
        'data': {
            'predict_ls': predict_ls,
            'pre_count': len(predict_ls),
            'total_count': total_count
        }
    })

@app.route('/create_gif', methods=['GET'])
def to_create_gif():
    # img_path = request.args.get('img_path')
    try:
        create_gif(path, gif_name='result.gif', duration=1)
        return jsonify({
            'code': 0,
            'msg': 'success to create gif'
        })
    except:
        return jsonify({
            'code': -1,
            'msg': 'fail'
        })

@app.route('/get_gif', methods=['GET'])
def get_gif():
    image_data = open(f'{path}/result.gif', "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/gif'
    return response


@app.route('/get_img', methods=['GET'])
def get_img():
    img_name = request.args.get('img_name')
    # return send_file(f'{path}/result_temp/{img_name}', mimetype='image/png')
    image_data = open(f'{path}/result_temp/{img_name}', "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response

# 获得面积
@app.route('/get_area', methods=['GET'])
def get_area():
    img_name = request.args.get('img_name')
    area = calculate_area(path, img_name)
    return jsonify({
        'code': 0,
        'msg': 'success to get area',
        'data': {
            'area': area
        }
    })

@app.route('/stop_predict', methods=['GET'])
def stop_predict():
    if net == '0':
        stop_u_predict()
    elif net == '1':
        stop_d_predict()
    sleep(3)
    clear_fold(path, 'result_temp')

    return 'ok'

# 退出
@app.route('/exit', methods=['GET'])
def exit():
    # del_folds(path, ('tif_file', 'tif_temp', 'png_temp', 'result_temp'))
    del_folds(path, ('result_temp',))

    return 'ok'


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, use_reloader=False, debug=True)
    # 注意，如果没有指定use_reloader=False，后续将其打包成exe后，运行exe会产生两个进程，在electron窗口关闭时kill掉进程时，会有一个守护进程无法kill掉
