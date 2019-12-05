import xlwt

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('SN')
SN = 'E20120191019'
for i in range(10000):
    if len(str(i)) == 1:
        SN_new = SN + '000'+ str(i)
    elif len(str(i)) == 2:
        SN_new = SN + '00' + str(i)
    elif len(str(i)) == 3:
        SN_new = SN + '0' + str(i)
    else:
        SN_new = SN + str(i)
    worksheet.write(i,0,SN_new)
workbook.save(r'C:\Users\tester\Desktop\SN_new.xlsx')