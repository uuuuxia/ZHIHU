#coding='utf-8'
import requests
import json
import re
import time
import datetime
import os
import xlwt
def get_content(url):
# 提交请求，相应请求
    headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'Cookie': 'd_c0="AGACwW1jwQuPTlr5YanFx_G-HJZYL5Kr8dk=|1494736636"; _zap=5e5c25c5-1386-4d56-ad09-76f1c43fb010; q_c1=165c6c4be08541818ed4f6dc2eb8510a|1503317822000|1494736634000; q_c1=165c6c4be08541818ed4f6dc2eb8510a|1503317822000|1494736634000; aliyungf_tc=AQAAAO9ovFIJiAYAcODAZ+jWLzeAIuDe; __utma=51854390.1430115655.1503841718.1503841718.1503881231.2; __utmc=51854390; __utmz=51854390.1503881231.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20170109=1^3=entry_date=20170109=1; l_cap_id="NDY0YTg4NjQ5ZWNlNGZmOGIyZTJhZDBjMjRlODhkZWU=|1503890537|4bdf5f244dfd01d2ecf50c0d792660c531f09c0b"; r_cap_id="N2YxYTZlMTVlNmQxNGJmODlmMzllZDVhMzgzN2E2NGM=|1503890537|3b22f6f69fb77cf770c3528486bb3a0fc48bfab3"; cap_id="YjkzYWYxYTRjZjk4NGE5YmJkMDYxMjgyNTIzMzhmYzM=|1503890537|cd8daff9d641a4785be0c0450279e0dba08cab5f"; _xsrf=1e5ffd6e-c180-4837-98a9-ac59ea2bc326',
                'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
                'Accept-Encoding': 'gzip, deflate, sdch, br'
           }
    # url = 'http://www.zhihu.com/api/v4/questions/21031487/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=23'
    req_session = requests.session()
    try:
        response = req_session.get(url, headers=headers)
        print("提示:除最后一批，单次爬取20条数")
        content = json.loads(response.text)
        return content
    except:
        print("提示：数据爬取失败，请排查异常情况。。。。")
def run(req_url):
# 流程
    pass
    # 1、接收用户收入url，
    # 2、进行请求，获取content
    file_num = 0
    url = req_url
    wb = xlwt.Workbook()
    ws = wb.add_sheet('ZhihuSpider', cell_overwrite_ok=True)
    while True:
        content = get_content(url)
        # 3、处理content，返回数据和url，下一页的url进行返回，重新调用数据处理(打印回答量)
        paging_info = get_url(content)
        # print("提示：该问题共有%s条回答" %paging_info['totals'])
        data_text_list = get_data(content)
        # 4进行数据保存
        file_num = save_data(data_text_list, file_num, ws)
        print("提示：已爬取%s条" %file_num)
        # 5、判断是否有下一页，如果有，继续发出请求
        if paging_info['is_end'] == False :
            url = paging_info['next']
            print(url)
        else:
            wb.save(data_text_list[0]["question_title"]+'.xls')
            print(">>>>>>>")
            print("提示：标题“%s”" %data_text_list[0]["question_title"])
            print("提示：该问题 %s 条回答,爬取 %%s 条" %paging_info['totals'] %file_num)
            print("提示：------数据采集完毕!保存至同名文件!--------------------------------------------------------------")
            break
def get_url(content):
#获取下一页信息
    # print('$'*10)
    # print(content)
    paging_dic = content['paging']
    paging_item = {}
    # 是否最后一页
    paging_item['is_end'] = paging_dic['is_end']
    # 回答量
    paging_item['totals'] = paging_dic['totals']
    paging_item['previous'] = paging_dic['previous']
    # 下一页地址
    paging_item['next'] = paging_dic['next']
    return paging_item
def get_data(content):
#处理数据，得到项目信息
    data_list = content['data']
    # print(data_list)
    data_text_list = []
    for data in data_list:
        # print(data)
        item = {}
        # 问题创建时间
        item['question_created_time'] = time_tran_stamp(data['question']['created'])
        # 问题更新时间
        # item['question_updated_time'] = data['question']['updated_time']
        item['question_updated_time'] = time_tran_stamp(data['question']['updated_time'])
        # 点赞数
        item['voteup_count'] = data['voteup_count']
        # 用户名
        item['author_name'] = data['author']['name']
        # 性别,男-1，女0，未知1
        item['author_gender'] = data['author']['gender']
        if item['author_gender'] == -1:
            item['author_gender'] = '男'
        elif item['author_gender'] == 0:
            item['author_gender'] = '女'
        else:
            item['author_gender'] = '未知'
        # 是否广告者
        item['author_is_advertiser'] = data['author']['is_advertiser']
        if item['author_is_advertiser'] == False:
            item['author_is_advertiser'] = '否'
        else:
            item['author_is_advertiser'] = '是'
        # 简单介绍
        item['author_headline']  = data['author']['headline']
        #用户主页
        url_user = data['author']['url']
        if url_user =='http://www.zhihu.com/api/v4/people/0':
            item['author_url'] ='空'
        else :
            item['author_url'] = re.sub(r'/api/v4', "", url_user)
        # 问题
        item['question_title'] = data['question']['title']
        # 回复时间
        item['question_created_time'] = time_tran_stamp(data['created_time'])
        # 回答内容
        # item['answer_content'] = re.sub(r'<.*>', '', data['content'])
        item['answer_content'] = data['content']
        # 评论数
        item['comment_count'] = data['comment_count']
        # 问题链接
        url_question = data['question']['url']
        item['question_url'] = re.sub(r'/api/v4', "", url_question)
        data_text_list.append(item)
    return data_text_list
def save_data(data_text_list, file_num, ws):
#文件保存
    for data in data_text_list:
        print(data)
        if file_num == 0 and os.path.exists(data['question_title']+".xls") == True:
            print("请删除保存目录下的同名文件,并重新执行本程序")
            exit()
        else:
            if file_num == 0:
                # 打印标题
                ws.write(0, 0, "标题：")
                ws.write(0, 1, data['question_title'])
                ws.write(1, 0, "创建时间：")
                ws.write(1, 1, data['question_created_time'])
                ws.write(2, 0, "更新时间:")
                ws.write(2, 1, data['question_updated_time'])
                ws.write(3, 0, "问题链接")
                ws.write(3, 1, data['question_url'])
                ws.write(4, 0, "序号")
                ws.write(4, 1, "内容")
                ws.write(4, 2, "点赞")
                ws.write(4, 3, "评论")
                ws.write(4 ,4, "回复时间")
                ws.write(4, 5, "用户名")
                ws.write(4, 6, "性别")
                ws.write(4, 7, "广告者?")
                ws.write(4, 8, "介绍")
                ws.write(4, 9, "用户主页")
                ws.write(5, 0, file_num + 1)
                ws.write(5, 1, data['answer_content'])
                ws.write(5, 2, data['voteup_count'])
                ws.write(5, 3, data['comment_count'])
                ws.write(5, 4, data['question_created_time'])
                ws.write(5, 5, data['author_name'])
                ws.write(5, 6, data['author_gender'])
                ws.write(5, 7, data['author_is_advertiser'])
                ws.write(5, 8, data['author_headline'])
                ws.write(5, 9, data['author_url'])
                file_num = file_num + 1
            else:
                # ws.write(file_num+1, 0,)
                # with open (data['question_title']+".csv", 'a') as f:
                    # f.write(json.dumps(data),)
                    # f.write("\n")
                answer_num = file_num+5
                ws.write(answer_num, 0, file_num+1)
                ws.write(answer_num, 1, data['answer_content'])
                ws.write(answer_num, 2, data['voteup_count'])
                ws.write(answer_num, 3, data['comment_count'])
                ws.write(answer_num, 4, data['question_created_time'])
                ws.write(answer_num, 5, data['author_name'])
                ws.write(answer_num, 6, data['author_gender'])
                ws.write(answer_num, 7, data['author_is_advertiser'])
                ws.write(answer_num, 8, data['author_headline'])
                ws.write(answer_num, 9, data['author_url'])
                file_num = file_num + 1
    return file_num
def time_tran_stamp(time_date):
#时间戳处理
    time_tran_ing = time.localtime(time_date)
    return time.strftime('%Y-%m-%d %H:%M:%S', time_tran_ing)
if __name__ == '__main__':
    #给"url_input"输入知乎问答地址(注意格式)
    url_input = 'https://www.zhihu.com/question/21935157'
    url_id = re.findall(r'\d*$', url_input)[0]
    req_url = 'http://www.zhihu.com/api/v4/questions/'+url_id+'/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0'
    print(req_url)
    run(req_url)
