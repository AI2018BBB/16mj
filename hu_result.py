from p16mj import next_two_not_block
from p16mj import next_two_not_blsame

def insert_mj(mjv, mj):
    return_mj = mj[:]
    for i, v in enumerate(return_mj):
        if mjv <= v:
            return_mj = return_mj[:i] + [mjv] + return_mj[i:]
            return return_mj, len(return_mj)
    
    return_mj.append(mjv)
    return return_mj, len(return_mj)

# rturn 1: hu, 0: NOT hu, mj must sort   
def hu(pmj, value):

    mj, mj_num = insert_mj(value, pmj)
    block = [0] * mj_num
    
    c = 0
    while c < mj_num:
        if mj_num - 1 == c:
            break
        #check pair
        if mj[c] == mj[c+1]:
            block[c] = 1
            block[c+1] = 1
            i = 0
            
            # mj_hu 1:hu, 0:NOT hu
            mj_hu = 1
            while i < mj_num:
                if 1 == block[i]:
                    i += 1
                    continue
                
                n1, n2 = next_two_not_block(block, mj_num, i+1)
                
                if n1 != -1 and n2 != -1:
                    if mj[i] == mj[n1] == mj[n2]:
                        block[i] = block[n1] = block[n2] = 1
                        i += 1
                        continue
                    else:
                        m1, m2 = next_two_not_blsame(block, mj_num, i+1, mj, mj[i])
                        
                        if m1 != -1 and m2 != -1 and mj[i] < 27 and mj[i]//9 == mj[m1]//9 == mj[m2]//9 and mj[i]+1 == mj[m1] and mj[m1]+1 == mj[m2]:
                            block[i] = block[m1] = block[m2] = 1
                            i += 1
                            continue
                        else:
                            mj_hu = 0
                            break
                else:
                    mj_hu = 0
                    break
                    
            if 1 == mj_hu:
                return 1
                
            block = [0] * mj_num
            c += 2
            
        c += 1
    
    return 0

class hu_result():
    def __init__(self, mj, dmj, hnum, first_turn, hmj, circle, door, bool_last, getmj = None, first_hear = 0, drophu = None, hhu = False, bool_akong = False, bool_pkong = False):
        self.mj = mj
        self.dj = dmj
        self.hnum = hnum
        self.ft = first_turn
        
        self.hj = hmj[:]
        self.hj.sort()
        
        self.circle = circle
        self.door = door
        self.last = bool_last
        self.gethu = getmj
        self.first_hear = first_hear
        self.drophu = drophu
        self.hhu = hhu
        self.bkong = bool_akong
        self.bpkong = bool_pkong
        
        self.fmj = self.mj[:]
        if None == self.gethu:
            insert_mj(self.drophu, self.fmj)
        else:
            insert_mj(self.gethu, self.fmj)
            
        self.table = {
            "莊家": self.hosthu(),
            ("連%d拉%d" % (hnum, hnum)): 2 * hnum,
            "自摸": self.selfhu(),
            "門清": self.dmjclear(),
            "三元台": self.dragons(2),
            "圈風台": self.wind_tai(0),
            "門風台": self.wind_tai(1),
            "花牌": self.flower_tai(),
            "獨聽": self.single_hear(),
            "搶槓": self.capture_kong(),
            "槓上開花": self.kong_hu(),
            "半求人": self.need_others(0),
            "海底撈月": self.last_hu(0),
            "河底撈魚": self.last_hu(1),
            "花槓": self.flower_kong(),
            "全求人": self.need_others(1),
            "平胡": self.pean_hu(),
            "三暗刻": self.same_color_bundle(3),
            "門清自摸": 0,
            "對對胡": 0,
            "混一色": 0,
            "小三元": self.dragons(1),
            "四暗刻": self.same_color_bundle(4),
            "五暗刻": self.same_color_bundle(5),
            "清一色": 0,
            "小四喜": 0,
            "大三元": self.dragons(0),
            "七搶一": self.seven_hhu(),
            "八仙過海": self.eight_hhu(),
            "天聽": 0,
            "地聽": 0,
            "字一色": 0,
            "大四喜": 0,
            "地胡": 0,
            "天胡": 0,
            "人胡": 0,
            "見花見台": 0,
            "見風見台": 0,
            "槓牌": 0,
            "暗槓": 0
        }
        
    def hosthu(self):
        if self.hnum > 0:
            return 1
        else:
            return 0
            
    def selfhu(self):
        if True == self.hhu:
            return 0
    
        if None == self.drophu:
            return 1
        else:
            return 0
            
    def dmjclear(self):
        if True == self.hhu:
            return 0
    
        if 0 == len(self.dj):
            return 1
        else:
            for tv in self.dj:
                type = tv[0]
                if type != 2: # dmj type is not dark kong
                    return 0
                    
            return 1
    
    def cal_same_color(self):
        bundle_number = 0
        
        # Calculate dark kong
        for tv in self.dj:
            type = tv[0]
            if 2 == type: #dmj type is dark kong
                bundle_number += 1
        
        i = 0
        while(i+2 < len(self.fmj)):
            if self.fmj[i] == self.fmj[i+1] == self.fmj[i+2]:
                i += 3
                bundle_number += 1
                continue
            i += 1
                
        return bundle_number
        
    def same_color_bundle(self, n):
        if True == self.hhu:
            return 0
        
        if n == self.cal_same_color():
            if 3 == n:
                return 2
            elif 4 == n:
                return 5
            elif 5 == n:
                return 8
            else:
                return 0
        else:
            return 0
            
    def cal_dragons(self):
        dpair = 0
        dseq = 0
        
        for tv in self.dj:
            t = tv[0]
            v = tv[1][0]
            if 1 == t or 2 == t or 3 == t:
                if 31 == v or 32 == v or 33 == v:
                    dseq += 1
                    
        i = 0
        while i+1 < len(self.fmj):
            if i+2 < len(self.fmj):
                if self.fmj[i] == self.fmj[i+1] == self.fmj[i+2] and (31 == self.fmj[i] or 32 == self.fmj[i] or 33 == self.fmj[i]):
                    dseq += 1
                    i += 3
                    continue
                elif self.fmj[i] == self.fmj[i+1] and (31 == self.fmj[i] or 32 == self.fmj[i] or 33 == self.fmj[i]):
                    dpair += 1
                    i += 2
                    continue
            else:
                if self.fmj[i] == self.fmj[i+1] and (31 == self.fmj[i] or 32 == self.fmj[i] or 33 == self.fmj[i]):
                    dpair += 1
                    i += 2
                    continue
            i += 1
        
        return dseq, dpair
        
    # t = 0, big dragons. t = 1, little dragons. t = 2, dragons.
    def dragons(self, t):
        if True == self.hhu:
            return 0
        
        dseq, dpair = self.cal_dragons()
        if 0 == t:
            if 3 == dseq:
                return 1
            else:
                return 0
        elif 1 == t:
            if 2 == dseq and 1 == dpair:
                return 1
            else:
                return 0
        elif 2 == t:
            if 1 == dseq:
                return 1
            elif 2 == dseq and 0 == dpair:
                return 2
            else:
                return 0
                
    def wind_index_to_value(self, c):
        if 0 == c:
            return 27
        elif 1 == c:
            return 28
        elif 2 == c:
            return 29
        elif 3 == c:
            return 30
    
    # mode = 0, for circle tai. mode = 1, for door tai
    def wind_tai(self, mode):
        if True == self.hhu:
            return 0
        
        if 0 == mode:
            wv = self.wind_index_to_value(self.circle)
        elif 1 == mode:
            wv = self.wind_index_to_value(self.door)
    
        for tv in self.dj:
            t = tv[0]
            v = tv[1][0]
            if 1 == t or 2 == t or 3 == t:
                if wv == v:
                    return 1
        
        i = 0
        while i+2 < len(self.fmj):
            if self.fmj[i] == self.fmj[i+1] == self.fmj[i+2] and wv == self.fmj[i]:
                return 1
            i += 1
        
        return 0
        
    def flower_tai(self):
        htai = 0
        
        if True == self.hhu:
            return 0
        elif self.flower_kong() > 0:
            return 0
        
        # east to north
        if 0 == self.door:
            for hv in self.hj:
                if 34 == hv:
                    htai += 1
                elif 38 == hv:
                    htai += 1
            return htai
        elif 1 == self.door:
            for hv in self.hj:
                if 35 == hv:
                    htai += 1
                elif 39 == hv:
                    htai += 1
            return htai
        elif 2 == self.door:
            for hv in self.hj:
                if 36 == hv:
                    htai += 1
                elif 40 == hv:
                    htai += 1
            return htai
        elif 3 == self.door:
            for hv in self.hj:
                if 37 == hv:
                    htai += 1
                elif 41 == hv:
                    htai += 1
            return htai
        else:
            return 0
            
    def single_hear(self):
        if True == self.hhu:
            return 0
        
        # for NOT duplicate need_others
        if 1 == len(self.mj):
            return 0
    
        if None == self.gethu:
            last_mj = self.drophu
        else:
            last_mj = self.gethu
        
        for i in range(31):
            if last_mj == i:
                continue
            elif 1 == hu(self.mj, i):
                return 0
                
        return 1
        
    def capture_kong(self):
        if True == self.hhu:
            return 0
        
        if True == self.bkong:
            return 1
        else:
            return 0
            
    def kong_hu(self):
        if True == self.hhu:
            return 0
        
        if True == self.bpkong:
            return 1
        else:
            return 0
    
    # m = 0 for half need others, m = 1 for complete need others
    def need_others(self, m):
        if True == self.hhu:
            return 0
        
        if 1 == len(self.mj):
            if 0 == m:
                if None == self.gethu:
                    return 0
                else:
                    return 2
            elif 1 == m:
                if None == self.gethu:
                    return 2
                else:
                    return 0
        return 0
        
    # m = 0, for sea hu. m = 1 for river hu.
    def last_hu(self, m):        
        if True == self.last:
            if True == self.hhu:
                if 0 == m and 8 == len(self.hj):
                    return 1
                elif 1 == m and 7 == len(self.hj):
                    return 1
            
            if 0 == m:
                if self.gethu != None:
                    return 1
            elif 1 == m:
                if None == self.gethu and self.drophu != None:
                    return 1
        
        return 0
    
    def flower_kong(self):
        if True == self.hhu:
            return 0
    
        length = len(self.hj)
        for i in range(length):
            if 34 == self.hj[i] and i+3 < length:
                if 35 == self.hj[i+1] and 36 == self.hj[i+2] and 37 == self.hj[i+3]:
                    return 2
            if 38 == self.hj[i] and i+3 < length:
                if 39 == self.hj[i+1] and 40 == self.hj[i+2] and 41 == self.hj[i+3]:
                    return 2
            
        return 0
        
    def eight_hhu(self):
        if 8 == len(self.hj):
            return 16
    
    def seven_hhu(self):
        if 7 == len(self.hj) and True == self.hhu:
            return 8
        else:
            return 0
    
    # check word in mj, 0 for NO word, 1 for word. 
    def check_word(self, mjlist):
        for c in mjlist:
            if 26 < c < 34:
                return 1
        return 0
    
    # 0 for NO word, 1 has word
    def is_word(self):
        nword = self.check_word(self.fmj)
        if 1 == nword:
            return 1
        for tv in self.dj:
            v = tv[1][0]
            nword = self.check_word([v])
            if 1 == nword:
                break
        
        return nword
    
    # return 0 if have pair and NO same color bundle, 1 for other wise
    # precondition: mj must hear
    def is_same_color():
        for tv in self.dj:
            t = tv[0]
            if 1 == t or 2 == t or 3 == t:
                return 1
    
        pair = False
        i = 0
        while i+1 < len(self.mj):
            if False == pair and self.mj[i] == self.mj[i+1]:
                pair = True
                i += 2
            #elif two pair
            elif self.mj[i] == self.mj[i+1]:
                return 1
            else:
                i += 1
    
        # must have pair
        if True == pair:
            return 0
        else:
            return 1
    
    def pean_hu(self):
        if True == self.hhu:
            return 0
        
        if 1 == self.is_word():
            return 0
        elif len(self.hj) > 0:
            return 0
        elif 1 == self.is_same_color():
            return 0
        elif self.single_hear() > 0:
            return 0
        elif self.selfhu() > 0:
            return 0
        else:
            return 2