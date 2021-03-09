#-*- codeing = utf-8 -*-
#@Author: m.kaku
#@Date: 2020-12-29 22:55:07
#@LastEditTime: 2021-01-06 00:44:36

from flask import Flask,request
import mercari
import rakuma
import json
 
app=Flask(__name__)
 
# 只接受get方法访问
@app.route("/",methods=["GET"])
def check():
    # 默认返回内容
    return_dict= {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.args is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的params参数
    get_data=request.args.to_dict()
    keyword=get_data.get('keyword')
    # 对参数进行操作
    return_dict['mercari']=m_search(keyword)
    return_dict['rakuma']=r_search(keyword)
    return json.dumps(return_dict, ensure_ascii=False)
 
# 功能函数
def m_search(keyword):
    result_str=mercari.search(keyword)
    return result_str
def r_search(keyword):
    result_str=rakuma.search(keyword)
    return result_str
if __name__ == "__main__":
    app.run(debug=True)