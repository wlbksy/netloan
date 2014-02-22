import urllib.request, re, time, winsound, os
from operator import itemgetter

def getHTML(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    page.close()
    data = html.decode('UTF-8')

    reg_title = r'_Lab_title"><a href=\'/Lend/Detail.aspx\?id=(.*?)</span></b></li><li>'
    raw_title = re.findall(reg_title,data,re.S)

    reg_id = r"(\d+)' target"
    reg_present = r'([\d.]+)奖'
    reg_type = r"src='/images/(.*?)\."

    raw_id = []
    raw_present = []
    raw_type = []

    for each_title in raw_title:
        raw_id.append(re.findall(reg_id,each_title,re.S))
        raw_present.append(re.findall(reg_present,each_title,re.S))
        raw_type.append(re.findall(reg_type,each_title,re.S))

    reg_money = r'_Lab_jkje">([\d,]+)</span> 元</li><li>利率'
    raw_money = re.findall(reg_money,data,re.S)

    reg_interest = r'_Lab_null">([\d.]+)'
    raw_interest = re.findall(reg_interest,data,re.S)

    reg_percent = r"'Pointer' style='width:([\d.]+)%;height:100%;"
    raw_percent = re.findall(reg_percent,data,re.S)

    reg_time = r'_Lab_month">(\d+)'
    raw_time = re.findall(reg_time,data,re.S)

    reg_way = r'_Lab_hkfs">(.*?)</span></li><li></li><li></li></ul>'
    raw_way = re.findall(reg_way,data,re.S)

    return raw_id,raw_present,raw_type,raw_money,raw_interest,raw_percent,raw_time,raw_way

def getList(url):
    raw_id,raw_present,raw_type,raw_money,raw_interest,raw_percent,raw_time,raw_way = getHTML(url)

    loan_list=[]

    for i in range(0,len(raw_id)):
        each_url =  url[:25]+"CreateVote.aspx?id="+str(raw_id[i][0])

        if len(raw_present[i]):
            each_present =  eval(raw_present[i][0])
        else:
            each_present = 0

        each_interest = eval(raw_interest[i])
        each_time = eval(raw_time[i])
        
        day_or_month = 0

        if raw_type[i] ==[]:
            each_type = "信"
        else:
            raw_type_i = raw_type[i][0]
            if raw_type_i=="ji":
                each_type = "急"
            elif raw_type_i=="ya":
                each_type = "押"
            elif raw_type_i=="db":
                each_type = "担"
            elif raw_type_i=="miao":
                each_type = "秒"
            elif raw_type_i=="tian":
                each_type = "天"
                day_or_month = 1
            else:
                each_type = "信"

        each_money = int((100-eval(raw_percent[i]))*int(raw_money[i].replace(',', ''))/100)

        each_yearly = calc_yearly(each_interest,day_or_month,each_present,each_time)

        each_loan = (each_type, each_interest, each_present, each_url, each_money, each_time, raw_way[i],each_yearly)

        loan_list.append(each_loan)

    return loan_list

def calc_yearly(i,day_or_month,p,n):   
    compoundYearRate = ((p/100+1)**(12/n+1))*((1+i/1200)**12) *100 - 100
    
    if day_or_month:
        compoundYearRate = (((p/100+1)*(n*i/1000+1))**(365/n)) * 100 - 100
        
    return compoundYearRate
    
def single(least_profit):
    main_url = "http://url/"
	
    page_main = urllib.request.urlopen(main_url)
    html_main = page_main.read()
    page_main.close()
    data_main = html_main.decode('UTF-8')
	
    reg_host = r'href="/Lend/(.*?)">我要投资'
    raw_url = re.findall(reg_host,data_main,re.S)
	
    host = main_url+"Lend/"+str(raw_url[0])

    result = getList(host)
    
    filtered1_result = [each_loan for each_loan in result if each_loan[7]>least_profit]
    
    filtered_result = [each_loan for each_loan in filtered1_result if each_loan[1]!="天" and each_loan[5]<4]
    
    filtered_result.sort(key=itemgetter(7))#,reverse=True)
    
    print(time.strftime('%H:%M:%S'))

    for loan in filtered_result:
        print(loan)

    num = len(filtered_result)
    if num:
        winsound.Beep(500,500)
        os.startfile(filtered_result[-1][3])
        
    print("\tTotal:\t"+str(num)+"\n")


if __name__== "__main__":
    while True:
        try:
            single(24.3)
            time.sleep(30)
        except Exception as err:
            continue
