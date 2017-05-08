
class Calculate:

# dictionary 내의 dictionary
#ex )  {key:{key:value},key2:{key2:value2}}
    calculates = {}

    def __init__(self):
        pass

    #테스트시 마이크로초 단위로 중복발생 체크 (현실에서 발생할 가능성 적음. 테스트를 위함)
    def save_data(self, name, how_many, time):

        if name in self.calculates: #name 중복체크
            if time in self.calculates[name]: #time 중복체크 현실적으로 X
                self.calculates[name][time] += how_many
            else:
                self.calculates[name][time] = how_many
        else:
            self.calculates[name] = {time:how_many} # ex) {2017:04:07~~ :20EA}


    def all_calculates(self):
        print('=' * 33)
        for (key,value) in self.calculates.items():
            for (time,many) in value.items():
                print('%s: %s  - %d' %(time,key,many))
        print('=' * 33)
