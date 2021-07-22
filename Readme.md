# 前言
写这个程序的目的只是为了使用 Google 日历来记录别人的生日（邮件提醒功能挺好用的）。但 Google 日历并没有固定农历日期提醒的功能，不得已曲线救国，寻找其他软件或 App 生成 ics 文件导入到 Google 日历中。但寻遍许多日历软件，要么无农历功能，要么无导出功能，尤其国产日历 App，功能少，广告多。而上 Github 搜寻一番过后，找到一些能用的 Python 代码，却也发现有各种问题。最后索性自己花点时间写一个算了。

# 日期数据
农历并没有简单的转换公历方法，只能靠天文台观测。而香港天文台恰好提供了1901年到2100年间两百年的农历-公历对照表数据。这里十分感谢 [香港天文台](https://www.hko.gov.hk/tc/gts/time/conversion1_text.htm#)。爬虫爬下来后，打包成 json 文件供大家使用。

值得注意的是与公历相似，农历是闰月的说法，也就是有些月份在同一年内会有重复，如2020年的闰四月，2028年闰五月。本程序会将闰月日期也加入到ics文件中
# 环境
- Python 3.9.6

更低版本应该可以，并没有进行测试
# 使用方法
json 文件以1901年1月1日为例，每个值的含义如下：
```json
"19010101": {               // 日期
    "Year": 1901,           // 年份
    "Month": 1,             // 月份
    "Day": 1,               // 几号
    "Lunarmonth": 11,       // 日期对应农历月份
    "Lunarday": 11,         // 日期对应农历
    "Leapmonth": false      // 是否为闰月
}
```
Demo 如下：
```Python
if __name__ == "__main__":
    birthday = []
    birthday.append([2000, 1, 1 , "测试"])      #加入农历生日2020年1月1日
    birthday.append([2000, 4, 2 , "测试"])      #加入农历生日2020年4月2日
    birthday.append([1950, 3, 23, "测试"])      #加入农历生日1950年3月23日

    date = dict()                              #读入 json
    with open("date.json", 'r') as file:
        date = json.load(file)

    with ics('生日') as icsfile:
        for year, month, day, info in birthday:
            # 生成当前这个人每一年的生日列表
            tmp = [key for key, value in date.items() if judge(value, year, month, day)]
            # 写入列表
            icsfile.write_date_lis(tmp, convert(month, day)+ " " + info)
```
运行程序后，会在同目录下生成生日.ics文件，将此文件导入 Google 日历即可。
