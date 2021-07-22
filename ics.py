import json

class ics:
    def __init__(self, filename):
        self.file = open(filename + '.ics', 'w', encoding="utf-8")
    
    def __enter__(self):
        self.file.write('BEGIN:VCALENDAR' + '\n')
        self.file.write('PRODID:-//Google Inc//Google Calendar 70.9054//EN' + '\n')
        self.file.write('VERSION:2.0' + '\n')
        return self

    def __exit__(self, exceptionType, exceptionVal, trace):
        self.file.write('END:VCALENDAR' + '\n')
        self.file.close()
        
    def write_date(self, date, info):
        self.file.write('BEGIN:VEVENT' + '\n')
        self.file.write('DTSTART;VALUE=DATE:' + date + '\n')
        self.file.write('DTEND;VALUE=DATE:' + date + '\n')
        self.file.write('CLASS:PRIVATE' + '\n')
        self.file.write('DESCRIPTION:' + '\n')
        self.file.write('LOCATION:' + '\n')
        self.file.write('SEQUENCE:0' + '\n')
        self.file.write('STATUS:CONFIRMED' + '\n')
        self.file.write('SUMMARY:' + info + '\n')
        self.file.write('TRANSP:TRANSPARENT' + '\n')
        self.file.write('END:VEVENT' + '\n')

    def write_date_lis(self, date_lis, info):
        for date in date_lis:
            self.write_date(date, info)

def judge(date, year, month, day):
    ans = True
    ans &= int(date['Year']) >= year
    ans &= int(date['Lunarmonth']) == month
    ans &= int(date['Lunarday']) == day
    return ans

def convert(month, day):
    convert_day = ["", "初一","初二","初三","初四","初五","初六","初七","初八","初九","初十","十一","十二","十三","十四","十五","十六","十七","十八","十九","二十","廿一","廿二","廿三","廿四","廿五","廿六","廿七","廿八","廿九","三十", "三十一"]
    convert_month = ["零","正","二","三","四","五","六","七","八","九","十", "冬", "腊"]  
    return convert_month[int(month)] + '月' + convert_day[int(day)]

if __name__ == "__main__":
    birthday = []
    birthday.append([2000, 1, 1 , "测试"])      #加入农历生日2020年1月1日
    birthday.append([2000, 4, 2 , "测试"])      #加入农历生日2020年4月2日
    birthday.append([1950, 3, 23, "测试"])      #加入农历生日1950年4月23日

    date = dict()                              #读入 json
    with open("date.json", 'r') as file:
        date = json.load(file)

    with ics('生日') as icsfile:
        for year, month, day, info in birthday:
            # 生成当前这个人每一年的生日列表
            tmp = [key for key, value in date.items() if judge(value, year, month, day)]
            # 写入列表
            icsfile.write_date_lis(tmp, convert(month, day)+ " " + info)
    