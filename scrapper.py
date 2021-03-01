import requests

table = {
    '开始时间': '2021-03-08', '结束时间': '2021-07-16', '课表信息': [
        {'课程名称': '计算机网络', '教师姓名': '刘志颖', '学时分布': '1-10',
         '节次信息': [
             {'节次': '星期一3-4节', '教室': '二东201', '校区': '主校区', '时间类型': ''},
             {'节次': '星期三3-4节', '教室': '二东201', '校区': '主校区', '时间类型': ''}]},
        {'课程名称': '电力系统运行概论', '教师姓名': '周毅博', '学时分布': '1-12',
         '节次信息': [
             {'节次': '星期二7-8节', '教室': '二中221', '校区': '主校区', '时间类型': ''},
             {'节次': '星期五7-8节', '教室': '二中221', '校区': '主校区', '时间类型': ''}]},
        {'课程名称': '电力信息技术', '教师姓名': '田洪亮', '学时分布': '1-8',
         '节次信息': [
             {'节次': '星期二9-10节', '教室': '二中217', '校区': '主校区', '时间类型': ''},
             {'节次': '星期五9-10节', '教室': '二中217', '校区': '主校区', '时间类型': ''}]},
        {'课程名称': '计算机系统结构', '教师姓名': '张洪业', '学时分布': '1-9',
         '节次信息': [
             {'节次': '星期二5-6节', '教室': '二西101', '校区': '主校区', '时间类型': ''},
             {'节次': '星期四5-6节', '教室': '二西101', '校区': '主校区', '时间类型': ''}]},
        {'课程名称': '嵌入式系统', '教师姓名': '郭树强', '学时分布': '1-12',
         '节次信息': [
             {'节次': '星期二3-4节', '教室': '二西102', '校区': '主校区', '时间类型': ''},
             {'节次': '星期四3-4节', '教室': '二西102', '校区': '主校区', '时间类型': ''}]},
        {'课程名称': '信息安全', '教师姓名': '霍光', '学时分布': '1-8',
         '节次信息': [
             {'节次': '星期二1-2节', '教室': '机房9', '校区': '主校区', '时间类型': ''},
             {'节次': '星期四1-2节', '教室': '机房9', '校区': '主校区', '时间类型': ''}]},
        {'课程名称': '创新与创业', '教师姓名': '张秋实', '学时分布': '1-4',
         '节次信息': [
             {'节次': '星期三7-8节', '教室': '机房10', '校区': '主校区', '时间类型': ''},
             {'节次': '星期五5-6节', '教室': '机房10', '校区': '主校区', '时间类型': ''}]},
        {'课程名称': '创业就业教育', '教师姓名': '张学亮', '学时分布': '1-4',
         '节次信息': [
             {'节次': '星期三9-10节', '教室': '二东302', '校区': '主校区', '时间类型': ''}]}
    ]
}


def get_session(userid, password):
    # logging in
    login_url = "http://inedu.neepu.edu.cn/HandSchool/Handler/CheckLogin.ashx"
    login_response = requests.get(login_url, params={"userid": userid, "pwd": password, })
    token = login_response.json()["token"]

    # creating session
    create_session_url = "http://inedu.neepu.edu.cn/HandSchool/Handler/CreateSession.ashx"
    create_session_response = requests.get(create_session_url, params={"token": token, })
    return create_session_response.cookies["ASP.NET_SessionId"]


def get_table(session_id, term_no="20202"):
    url = "http://inedu.neepu.edu.cn/HandSchool/Handler/GetDataByCollegesEMSService.ashx"
    r = requests.get(url, params={
        "flag"  : "GetStuOccupyChoiceTerm",
        "TermNo": term_no,
    }, cookies={"ASP.NET_SessionId": session_id})
    # print(r.json())
    return r.json()
