from pyvi.pyvi import ViTokenizer, ViPosTagger

token = ViTokenizer.tokenize(u"Sửa đổi, bổ sung một số điều của Thông tư số 45/2013/TT-BTC ngày 25 \
tháng 4 năm 2013 và Thông tư số 147/2016/TT-BTC ngày 13 tháng 10 \
năm 2016 của \
Bộ Tài chính hướng dẫn chế độ quản lý, sử dụng \
và trích khấu hao tài sản cổ định")

pos = ViPosTagger.postagging(token)

print(pos)

dic = {}

for key, value in zip(pos[0], pos[1]):
    dic[key] = value

for key, value in dic.items():
    print(key, value)