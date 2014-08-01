import urllib.request, re, time, winsound, os
from operator import itemgetter

def getHTML(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    page.close()
    data = html.decode('UTF-8')

    reg_title = r'Lab_title"><span class=\'span_width\'><a href=\'/Lend/Detail.aspx\?id=(.*?)</span></b></li><li>'
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
        
    reg_interest = r'_Lab_null">([\d.]+)'
    raw_interest = re.findall(reg_interest,data,re.S)

    reg_time = r'_Lab_month">(\d+)'
    raw_time = re.findall(reg_time,data,re.S)

    return raw_id,raw_present,raw_type,raw_interest,raw_time

def getList(url):
    raw_id,raw_present,raw_type,raw_interest,raw_time = getHTML(url)
    
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
            day_or_month = 0
        else:
            raw_type_i = raw_type[i][0]
            if raw_type_i=="tian":
                day_or_month = 1

        
        each_yearly = calc_yearly(each_interest,day_or_month,each_present,each_time)
        
        each_loan = (each_interest, each_present, day_or_month, each_url, each_time, each_yearly)

        loan_list.append(each_loan)

    return loan_list

def calc_yearly(i,day_or_month,p,n):   
    compoundYearRate = ((p/100+1)**(12/n+1))*((1+i/1200)**12) *100 - 100
    
    if day_or_month:
        compoundYearRate = (((p/100+1)*(n*i/1000+1))**(365/n)) * 100 - 100
        
    return compoundYearRate
    
def single(least_profit):
    main_url = "url"
	
    page_main = urllib.request.urlopen(main_url)
    html_main = page_main.read()
    page_main.close()
    data_main = html_main.decode('UTF-8')
	
    reg_host = r'end/(.*?)">我要投资'
    raw_url = re.findall(reg_host,data_main,re.S)

    host = main_url+"lend/"+str(raw_url[0])
    
    result = getList(host)
        
    high_profit_result = [each_loan for each_loan in result if each_loan[5]>least_profit]
    
    time_filtered_result = [each_loan for each_loan in high_profit_result if each_loan[2] or (not each_loan[2] and each_loan[4]<7)]
        
    time_filtered_result.sort(key=itemgetter(5))#,reverse=True)
    
    print(time.strftime('%H:%M:%S'))

    for loan in time_filtered_result:
        print(loan)

    num = len(time_filtered_result)
    if num:
        winsound.Beep(500,500)
        os.startfile(time_filtered_result[-1][3])
        
    print("\tTotal:\t"+str(num)+"\n")


if __name__== "__main__":
    while True:
        try:
            single(21)
            time.sleep(30)
        except Exception as err:
            continue
