from flask import Flask, jsonify, request
from flask_cors import cross_origin
import threading
from seg_tif import get_seg_count
from change import seg_and_change, get_change_count
import os
app = Flask(__name__)

path = ''
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
        os.mkdir(f'{path}tif_file')
        os.mkdir(f'{path}tif_temp')
        os.mkdir(f'{path}/png_temp')
        return jsonify ({
            'code': 0,
            'msg': 'success to set path'
        })
    else:
        return jsonify ({
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

# 上传tif文件
@app.route('/img', methods=['POST'])
def img():
    # return os.getcwd()
    if not path:
        with open('a.txt', 'w') as f:
            f.write('aaa')
    tif_file = request.files.get('tif_file')
    file_path = f'{path}/tif_file/to_predict.tif'
    # print(file_path)
    tif_file.save(file_path)
    print(path)
    t = threading.Thread(target=seg_and_change, args=(path,))
    t.start()
    return jsonify({
        'code': 0,
        'msg': 'success to upload'
    })

# # 分割文件
# @app.route('/bgein_seg', methods=['GET'])
# def bgein_seg():
    
#     return jsonify({
#         'code': 0,
#         'msg': 'begin to seg'
#     })

# 分割进度
@app.route('/seg_process', methods=['GET'])
def seg_process():
    seg_total, seg_count= get_seg_count()
    change_count = get_change_count()
    return jsonify({
        'code': 0,
        'msg': 'success to get the count',
        'data': {
            'total_count': seg_total,
            'seg_count': seg_count,
            'change_count': change_count
        }
    })


# 退出
@app.route('/exit', methods=['GET'])
def exit():
    pass




if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, use_reloader=False, debug=True)
    # 注意，如果没有指定use_reloader=False，后续将其打包成exe后，运行exe会产生两个进程，在electron窗口关闭时kill掉进程时，会有一个守护进程无法kill掉
