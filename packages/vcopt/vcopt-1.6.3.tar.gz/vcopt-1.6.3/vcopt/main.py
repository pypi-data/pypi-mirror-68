import math ,time ,os #line:2
import numpy as np #line:3
import numpy .random as nr #line:4
from copy import deepcopy #line:5
import matplotlib .pyplot as plt #line:6
from joblib import Parallel ,delayed #line:7
import hashlib #line:8
md5_s =['6c11f117a84c860c4044f8a1a45a0e67','cb51d4bbfdf4cc67e8bec57bc57e21c8','28f9afcaa52714aa964e215b7247a691','57f92316a9e611dd97c1528694ff6f9f','fd3dbb083970d4ba54ff6d067ab0c320','57c3d88ebf6777016c1429d25f283052','5f12a9899da112ee22a9a3ca7286b75b','9c84d4d198be8a5ef0dd96a8df934a80','df9c3ded3fe362c4c513a2bb3b28383f','12536e9b1dad1aabd97139327a115cc4','2a282b5b4649959c8a37c38e333789ad','0946a6c2e833058ced3d4798ba7ed903','432b8b1a39018c5b423f618c825a170c','46332f4160a17a9cb13fe5a559a66004','53630aba1c1685f49a216d70eb6bb7e0','acd9e269de3dcf51a4090cc907ae6ca9','affe60d5c024c79e77e7723bbca9608d','985b95f3aa925b05f3ac50561bab5dc2','2b7b9589e306a4419a7b259a1a7f1127','f9ac39e0da75c423a92003125f573429','0a988276a12594b79f9d79457371a1ad','ff4808135d6784b9a849f650cf579a46','91f88b573ccf4e2cc31da287baaff287','660440c7e709d6d3cd86293bd8ef1368','d552702c3e333e8c8e0d766c9b2c2b1c','31cd4b4c4b6964a1d4b1f78e8d2b213e','03a6a04c30c6d5b2041671c39eeec57e','503b8c8889c87da762be47d452d9fe12','146aec80f4ccdd435a2aaf7339e598e8','a02c5ad1046ed530f5e96c317300f312']#line:44
class vcopt :#line:63
    def __init__ (O000O000OO0OOOOO0 ):#line:64
        pass #line:65
    def __del__ (OOOOOO000O0O0000O ):#line:66
        pass #line:67
    def setting_1 (OOO000OO00000O000 ,O0O00OOO00O00OOO0 ,O0OOO0000OOOOOOO0 ,O000000OO0000OO00 ,OOO000O0OOOO0000O ,OO0OOO00O00OO00OO ,OOOOO0O0O00OOOOOO ,OO00OO0000O0OO0OO ,OO00OO0OOOOOOOOO0 ):#line:71
        OOO000OO00000O000 .para_range =O0O00OOO00O00OOO0 #line:72
        OOO000OO00000O000 .para_num =len (O0O00OOO00O00OOO0 )#line:73
        OOO000OO00000O000 .score_func =O0OOO0000OOOOOOO0 #line:74
        if type (O000000OO0000OO00 )==str and O000000OO0000OO00 [0 :2 ]=='==':#line:76
                OOO000OO00000O000 .aim =float (O000000OO0000OO00 [2 :])#line:77
                OOO000OO00000O000 .aim_operator ='=='#line:78
        elif type (O000000OO0000OO00 )==str and (O000000OO0000OO00 [0 :2 ]=='>='or O000000OO0000OO00 [0 :2 ]=='=>'):#line:79
                OOO000OO00000O000 .aim =float (O000000OO0000OO00 [2 :])#line:80
                OOO000OO00000O000 .aim_operator ='>='#line:81
        elif type (O000000OO0000OO00 )==str and (O000000OO0000OO00 [0 :2 ]=='<='or O000000OO0000OO00 [0 :2 ]=='=<'):#line:82
                OOO000OO00000O000 .aim =float (O000000OO0000OO00 [2 :])#line:83
                OOO000OO00000O000 .aim_operator ='<='#line:84
        elif type (O000000OO0000OO00 )==str and O000000OO0000OO00 [0 :1 ]=='>':#line:85
                OOO000OO00000O000 .aim =float (O000000OO0000OO00 [1 :])#line:86
                OOO000OO00000O000 .aim_operator ='>'#line:87
        elif type (O000000OO0000OO00 )==str and O000000OO0000OO00 [0 :1 ]=='<':#line:88
                OOO000OO00000O000 .aim =float (O000000OO0000OO00 [1 :])#line:89
                OOO000OO00000O000 .aim_operator ='<'#line:90
        elif type (O000000OO0000OO00 )==str and O000000OO0000OO00 [0 :1 ]=='=':#line:91
                OOO000OO00000O000 .aim =float (O000000OO0000OO00 [1 :])#line:92
                OOO000OO00000O000 .aim_operator ='=='#line:93
        else :#line:94
            OOO000OO00000O000 .aim =float (O000000OO0000OO00 )#line:95
            OOO000OO00000O000 .aim_operator ='=='#line:96
        OOO000OO00000O000 .show_pool_func =OOO000O0OOOO0000O #line:98
        if OOO000OO00000O000 .show_pool_func ==None :pass #line:100
        elif OOO000OO00000O000 .show_pool_func in ['bar','print','plot']:pass #line:101
        elif callable (OOO000OO00000O000 .show_pool_func ):pass #line:102
        elif type (OOO000O0OOOO0000O )==str :#line:103
            if len (OOO000O0OOOO0000O )==0 or OOO000O0OOOO0000O [-1 ]!='/':#line:104
                OOO000OO00000O000 .show_pool_func ='bar'#line:105
        if type (OO0OOO00O00OO00OO )in [int ,float ]:#line:107
            OOO000OO00000O000 .seed =int (OO0OOO00O00OO00OO )#line:108
        else :#line:109
            OOO000OO00000O000 .seed =None #line:110
        nr .seed (OOO000OO00000O000 .seed )#line:111
        OO00O0000OOOO0OOO =1609426800.0 #line:112
        if type (OOOOO0O0O00OOOOOO )in [int ,float ]:#line:114
            OOO000OO00000O000 .pool_num =int (OOOOO0O0O00OOOOOO )#line:115
            if OOO000OO00000O000 .pool_num %2 !=0 :#line:117
                OOO000OO00000O000 .pool_num +=1 #line:118
        else :#line:119
            OOO000OO00000O000 .pool_num =None #line:120
        if type (OO00OO0000O0OO0OO )in [int ,float ]:#line:122
            OOO000OO00000O000 .max_gen =int (OO00OO0000O0OO0OO )#line:123
        else :#line:124
            OOO000OO00000O000 .max_gen =None #line:125
        OOO000OO00000O000 .core_num =1 #line:128
        if type (OO00OO0OOOOOOOOO0 )in [int ,float ]:#line:129
            OOOOO000O00OOOOO0 =hashlib .md5 (str (OO0OOO00O00OO00OO ).encode ()).hexdigest ()#line:131
            if OOOOO000O00OOOOO0 in md5_s and time .time ()<OO00O0000OOOO0OOO :#line:132
                OOO000OO00000O000 .core_num =int (OO00OO0OOOOOOOOO0 )#line:133
        OOO000OO00000O000 .start =time .time ()#line:134
    def setting_2 (O000000OO0OO0O0OO ,O0OOO00O00O00O0OO ,OO000OO000OOO0000 ,OO000OOO0OO0O0OOO ):#line:138
        if O000000OO0OO0O0OO .pool_num is None :#line:140
            O000000OO0OO0O0OO .pool_num =O0OOO00O00O00O0OO #line:141
        O000000OO0OO0O0OO .parent_num =OO000OO000OOO0000 #line:142
        O000000OO0OO0O0OO .child_num =OO000OOO0OO0O0OOO #line:143
        O000000OO0OO0O0OO .family_num =OO000OO000OOO0000 +OO000OOO0OO0O0OOO #line:144
        if O000000OO0OO0O0OO .max_gen is None :#line:146
            O000000OO0OO0O0OO .max_n =1000000 #line:147
        else :#line:148
            O000000OO0OO0O0OO .max_n =O000000OO0OO0O0OO .max_gen //O000000OO0OO0O0OO .pool_num +1 #line:149
    def setting_3 (OO0000O0O00O0O0O0 ,O0O00000OOO0O0OO0 ):#line:153
        OO0000O0O00O0O0O0 .pool ,OO0000O0O00O0O0O0 .pool_score =np .zeros ((OO0000O0O00O0O0O0 .pool_num ,OO0000O0O00O0O0O0 .para_num ),dtype =O0O00000OOO0O0OO0 ),np .zeros (OO0000O0O00O0O0O0 .pool_num )#line:154
        OO0000O0O00O0O0O0 .parent ,OO0000O0O00O0O0O0 .parent_score =np .zeros ((OO0000O0O00O0O0O0 .parent_num ,OO0000O0O00O0O0O0 .para_num ),dtype =O0O00000OOO0O0OO0 ),np .zeros (OO0000O0O00O0O0O0 .parent_num )#line:155
        OO0000O0O00O0O0O0 .child ,OO0000O0O00O0O0O0 .child_score =np .zeros ((OO0000O0O00O0O0O0 .child_num ,OO0000O0O00O0O0O0 .para_num ),dtype =O0O00000OOO0O0OO0 ),np .zeros (OO0000O0O00O0O0O0 .child_num )#line:156
        OO0000O0O00O0O0O0 .family ,OO0000O0O00O0O0O0 .family_score =np .zeros ((OO0000O0O00O0O0O0 .family_num ,OO0000O0O00O0O0O0 .para_num ),dtype =O0O00000OOO0O0OO0 ),np .zeros (OO0000O0O00O0O0O0 .family_num )#line:157
    def print_info (OO00O0O00O0OOO0O0 ):#line:161
        if OO00O0O00O0OOO0O0 .show_pool_func is not None :#line:162
            print ('{:_^86}'.format (' info '))#line:163
            print ('para_range     : n={}'.format (OO00O0O00O0OOO0O0 .para_num ))#line:164
            print ('score_func     : {}'.format (type (OO00O0O00O0OOO0O0 .score_func )))#line:165
            print ('aim            : {}{}'.format (OO00O0O00O0OOO0O0 .aim_operator ,OO00O0O00O0OOO0O0 .aim ))#line:166
            print ('show_pool_func : \'{}\''.format (OO00O0O00O0OOO0O0 .show_pool_func ))#line:168
            print ('seed           : {}'.format (OO00O0O00O0OOO0O0 .seed ))#line:169
            print ('pool_num       : {}'.format (OO00O0O00O0OOO0O0 .pool_num ))#line:170
            print ('max_gen        : {}'.format (OO00O0O00O0OOO0O0 .max_gen ))#line:171
            if OO00O0O00O0OOO0O0 .core_num ==1 :#line:172
                print ('core_num       : {} (*vcopt, vc-grendel)'.format (OO00O0O00O0OOO0O0 .core_num ))#line:173
            else :#line:174
                print ('core_num       : {} (vcopt, *vc-grendel)'.format (OO00O0O00O0OOO0O0 .core_num ))#line:175
            print ('{:_^86}'.format (' start '))#line:176
    def print_result (OO000O000OO0O0OO0 ,O0OOOOO0O000O000O ):#line:180
        if OO000O000OO0O0OO0 .show_pool_func !=None :#line:182
            print ('{:_^86}'.format (' result '))#line:183
            O00O0000OOOO00O00 ='para = np.array([{}'.format (O0OOOOO0O000O000O [0 ])#line:186
            for OOOO0O0OOO0OO00OO in O0OOOOO0O000O000O [1 :]:#line:187
                O00O0000OOOO00O00 +=', {}'.format (OOOO0O0OOO0OO00OO )#line:188
            O00O0000OOOO00O00 +='])'#line:189
            print (O00O0000OOOO00O00 )#line:190
            print ('score = {}'.format (OO000O000OO0O0OO0 .score_best ))#line:191
            print ('{:_^86}'.format (' end '))#line:192
    def score_pool_multi (OOOOO00000OOO0000 ,O00OOO0O0OOO000O0 ):#line:196
        O0000O000O0O00O00 =OOOOO00000OOO0000 .para_range [OOOOO00000OOO0000 .pool [O00OOO0O0OOO000O0 ]]#line:197
        OOOOO00000OOO0000 .pool_score [O00OOO0O0OOO000O0 ]=OOOOO00000OOO0000 .score_func (O0000O000O0O00O00 )#line:198
        OOOOO00000OOO0000 .aaa +=1 #line:199
        if OOOOO00000OOO0000 .show_pool_func !=None :#line:200
            O00O000000OOO000O ='\rScoring first gen {}/{}        '.format (O00OOO0O0OOO000O0 +1 ,OOOOO00000OOO0000 .pool_num )#line:201
            print (O00O000000OOO000O ,end ='')#line:202
    def score_pool (OO0OOO00O000O00OO ):#line:203
        OO0OOO00O000O00OO .aaa =0 #line:204
        Parallel (n_jobs =OO0OOO00O000O00OO .core_num ,require ='sharedmem')([delayed (OO0OOO00O000O00OO .score_pool_multi )(OOO0O0OO0O000OO0O )for OOO0O0OO0O000OO0O in range (OO0OOO00O000O00OO .pool_num )])#line:205
        if OO0OOO00O000O00OO .show_pool_func !=None :#line:206
            O000O0O0OO0O00OO0 ='\rScoring first gen {}/{}        '.format (OO0OOO00O000O00OO .pool_num ,OO0OOO00O000O00OO .pool_num )#line:207
            print (O000O0O0OO0O00OO0 )#line:208
    def score_pool_dc_multi (OOOOO0O0OOO0O0O00 ,O0000O00OO000000O ):#line:219
        O0O0OO0O0O0O0OOOO =[]#line:220
        for O00000000O0O00O00 in range (OOOOO0O0OOO0O0O00 .para_num ):#line:221
            O0O0OO0O0O0O0OOOO .append (OOOOO0O0OOO0O0O00 .para_range [O00000000O0O00O00 ][OOOOO0O0OOO0O0O00 .pool [O0000O00OO000000O ,O00000000O0O00O00 ]])#line:222
        O0O0OO0O0O0O0OOOO =np .array (O0O0OO0O0O0O0OOOO )#line:223
        OOOOO0O0OOO0O0O00 .pool_score [O0000O00OO000000O ]=OOOOO0O0OOO0O0O00 .score_func (O0O0OO0O0O0O0OOOO )#line:224
        OOOOO0O0OOO0O0O00 .aaa +=1 #line:225
        if OOOOO0O0OOO0O0O00 .show_pool_func !=None :#line:226
            OO0O00O0O0000O00O ='\rScoring first gen {}/{}        '.format (O0000O00OO000000O +1 ,OOOOO0O0OOO0O0O00 .pool_num )#line:227
            print (OO0O00O0O0000O00O ,end ='')#line:228
    def score_pool_dc (O0OOO0OO00O0OO00O ):#line:229
        O0OOO0OO00O0OO00O .aaa =0 #line:230
        Parallel (n_jobs =O0OOO0OO00O0OO00O .core_num ,require ='sharedmem')([delayed (O0OOO0OO00O0OO00O .score_pool_dc_multi )(OOO00000000O00OO0 )for OOO00000000O00OO0 in range (O0OOO0OO00O0OO00O .pool_num )])#line:231
        if O0OOO0OO00O0OO00O .show_pool_func !=None :#line:232
            O0000O000OOO0OO0O ='\rScoring first gen {}/{}        '.format (O0OOO0OO00O0OO00O .pool_num ,O0OOO0OO00O0OO00O .pool_num )#line:233
            print (O0000O000OOO0OO0O )#line:234
    def score_pool_rc_multi (OOOO000O000O0O0O0 ,O0OOOO00OO00000O0 ):#line:248
        O0OOO0O0O0O0OO000 =OOOO000O000O0O0O0 .pool [O0OOOO00OO00000O0 ]*(OOOO000O000O0O0O0 .para_range [:,1 ]-OOOO000O000O0O0O0 .para_range [:,0 ])+OOOO000O000O0O0O0 .para_range [:,0 ]#line:249
        OOOO000O000O0O0O0 .pool_score [O0OOOO00OO00000O0 ]=OOOO000O000O0O0O0 .score_func (O0OOO0O0O0O0OO000 )#line:250
        OOOO000O000O0O0O0 .aaa +=1 #line:251
        if OOOO000O000O0O0O0 .show_pool_func !=None :#line:252
            OOO0O0OO0OO00O000 ='\rScoring first gen {}/{}        '.format (O0OOOO00OO00000O0 +1 ,OOOO000O000O0O0O0 .pool_num )#line:253
            print (OOO0O0OO0OO00O000 ,end ='')#line:254
    def score_pool_rc (O0O0OOO00O0O00000 ):#line:255
        O0O0OOO00O0O00000 .aaa =0 #line:256
        Parallel (n_jobs =O0O0OOO00O0O00000 .core_num ,require ='sharedmem')([delayed (O0O0OOO00O0O00000 .score_pool_rc_multi )(O000O000OOO0000O0 )for O000O000OOO0000O0 in range (O0O0OOO00O0O00000 .pool_num )])#line:257
        if O0O0OOO00O0O00000 .show_pool_func !=None :#line:258
            O00OOOOOOOOO000O0 ='\rScoring first gen {}/{}        '.format (O0O0OOO00O0O00000 .pool_num ,O0O0OOO00O0O00000 .pool_num )#line:259
            print (O00OOOOOOOOO000O0 )#line:260
    def save_best_mean (OOOO00OO0O0O00O0O ):#line:294
        OOOO00OO0O0O00O0O .best_index =np .argmin (np .abs (OOOO00OO0O0O00O0O .aim -OOOO00OO0O0O00O0O .pool_score ))#line:296
        OOOO00OO0O0O00O0O .pool_best =deepcopy (OOOO00OO0O0O00O0O .pool [OOOO00OO0O0O00O0O .best_index ])#line:298
        OOOO00OO0O0O00O0O .score_best =deepcopy (OOOO00OO0O0O00O0O .pool_score [OOOO00OO0O0O00O0O .best_index ])#line:299
        OOOO00OO0O0O00O0O .score_mean =np .mean (OOOO00OO0O0O00O0O .pool_score )#line:302
        OOOO00OO0O0O00O0O .gap_mean =np .mean (np .abs (OOOO00OO0O0O00O0O .aim -OOOO00OO0O0O00O0O .pool_score ))#line:303
        OOOO00OO0O0O00O0O .score_mean_save =deepcopy (OOOO00OO0O0O00O0O .score_mean )#line:305
        OOOO00OO0O0O00O0O .gap_mean_save =deepcopy (OOOO00OO0O0O00O0O .gap_mean )#line:306
    def make_parent (O00000O0O00OO00OO ,OO0O0O0OOOOOOOOO0 ):#line:310
        O00000O0O00OO00OO .pool_select =OO0O0O0OOOOOOOOO0 #line:311
        O00000O0O00OO00OO .parent =O00000O0O00OO00OO .pool [O00000O0O00OO00OO .pool_select ]#line:312
        O00000O0O00OO00OO .parent_score =O00000O0O00OO00OO .pool_score [O00000O0O00OO00OO .pool_select ]#line:313
    def make_family (O0OO000O000OOOO00 ):#line:317
        O0OO000O000OOOO00 .family =np .vstack ((O0OO000O000OOOO00 .child ,O0OO000O000OOOO00 .parent ))#line:318
        O0OO000O000OOOO00 .family_score =np .hstack ((O0OO000O000OOOO00 .child_score ,O0OO000O000OOOO00 .parent_score ))#line:319
    def JGG (O00O000O00OOOO0OO ):#line:323
        O00O000O00OOOO0OO .family_select =np .argpartition (np .abs (O00O000O00OOOO0OO .aim -O00O000O00OOOO0OO .family_score ),O00O000O00OOOO0OO .parent_num )[:O00O000O00OOOO0OO .parent_num ]#line:326
        O00O000O00OOOO0OO .pool [O00O000O00OOOO0OO .pool_select ]=O00O000O00OOOO0OO .family [O00O000O00OOOO0OO .family_select ]#line:328
        O00O000O00OOOO0OO .pool_score [O00O000O00OOOO0OO .pool_select ]=O00O000O00OOOO0OO .family_score [O00O000O00OOOO0OO .family_select ]#line:329
    def end_check (OO0O0000O0O00000O ):#line:333
        OO0O0000O0O00000O .best_index =np .argmin (np .abs (OO0O0000O0O00000O .aim -OO0O0000O0O00000O .pool_score ))#line:335
        OO0O0000O0O00000O .score_best =deepcopy (OO0O0000O0O00000O .pool_score [OO0O0000O0O00000O .best_index ])#line:336
        OO0O0000O0O00000O .gap_mean =np .mean (np .abs (OO0O0000O0O00000O .aim -OO0O0000O0O00000O .pool_score ))#line:338
        if eval (str (OO0O0000O0O00000O .score_best )+OO0O0000O0O00000O .aim_operator +str (OO0O0000O0O00000O .aim )):#line:342
            return 10 #line:343
        if OO0O0000O0O00000O .gap_mean >=OO0O0000O0O00000O .gap_mean_save :#line:345
            return 1 #line:346
        return 0 #line:347
    def make_info (O0O0OOO0O0O00OO00 ,OO000OOOOOOOOO0OO ):#line:365
        OOOOO0OOO000O00O0 ={'gen':OO000OOOOOOOOO0OO ,'best_index':O0O0OOO0O0O00OO00 .best_index ,'best_score':O0O0OOO0O0O00OO00 .score_best ,'mean_score':O0O0OOO0O0O00OO00 .score_mean ,'mean_gap':O0O0OOO0O0O00OO00 .gap_mean ,'time':time .time ()-O0O0OOO0O0O00OO00 .start }#line:370
        return OOOOO0OOO000O00O0 #line:371
    def show_pool (O0OO0000OOO0O00O0 ,O0OOO0OOOO0OO0OO0 ):#line:375
        O00OOO0O000OO00OO =O0OO0000OOO0O00O0 .make_info (O0OOO0OOOO0OO0OO0 )#line:376
        O0OO0000OOO0O00O0 .show_pool_func (O0OO0000OOO0O00O0 .para_range [O0OO0000OOO0O00O0 .pool ],**O00OOO0O000OO00OO )#line:377
    def show_pool_dc (OO000OOOOOO00OO00 ,OO00O00O0O0O0OOOO ):#line:378
        OO0000OO000O0O0O0 =OO000OOOOOO00OO00 .make_info (OO00O00O0O0O0OOOO )#line:379
        O000000O0OOO0O0OO =[]#line:380
        for O000OOO0O0O0O0OOO in range (OO000OOOOOO00OO00 .pool_num ):#line:381
            O0OOOO0O0OOOO0OOO =[]#line:382
            for OO00O00O00000OO00 in range (OO000OOOOOO00OO00 .para_num ):#line:383
                O0OOOO0O0OOOO0OOO .append (OO000OOOOOO00OO00 .para_range [OO00O00O00000OO00 ][OO000OOOOOO00OO00 .pool [O000OOO0O0O0O0OOO ,OO00O00O00000OO00 ]])#line:384
            O000000O0OOO0O0OO .append (O0OOOO0O0OOOO0OOO )#line:385
        O000000O0OOO0O0OO =np .array (O000000O0OOO0O0OO )#line:386
        OO000OOOOOO00OO00 .show_pool_func (O000000O0OOO0O0OO ,**OO0000OO000O0O0O0 )#line:387
    def show_pool_rc (OO0O00000OO000OO0 ,O00OOOOO0O00OO0O0 ):#line:388
        OO00000O0OOOO0OOO =OO0O00000OO000OO0 .make_info (O00OOOOO0O00OO0O0 )#line:389
        O00OO00OOOO0OO000 =np .array (list (map (lambda O0000000O0O0O0OO0 :OO0O00000OO000OO0 .pool [O0000000O0O0O0OO0 ]*(OO0O00000OO000OO0 .para_range [:,1 ]-OO0O00000OO000OO0 .para_range [:,0 ])+OO0O00000OO000OO0 .para_range [:,0 ],range (OO0O00000OO000OO0 .pool_num ))))#line:392
        OO0O00000OO000OO0 .show_pool_func (O00OO00OOOO0OO000 ,**OO00000O0OOOO0OOO )#line:393
    def make_fill (O00OOO0OO000O0000 ,OO00OOO0O0OO00O00 ):#line:397
        OO00OOO0O0OO00O00 ='{:>8}'.format (OO00OOO0O0OO00O00 )#line:398
        O00OO00O00OO0O00O ='{:8.3f}'.format (O00OOO0OO000O0000 .score_best )#line:399
        OO00O0O0O0O00OOO0 ='{:8.3f}'.format (O00OOO0OO000O0000 .score_mean )#line:400
        O0OO0O0000O000OO0 ='{:8.3f}'.format (O00OOO0OO000O0000 .gap_mean )#line:401
        O0OOO0OO000OOO000 ='{:6.1f}'.format (time .time ()-O00OOO0OO000O0000 .start )#line:402
        return OO00OOO0O0OO00O00 ,O00OO00O00OO0O00O ,OO00O0O0O0O00OOO0 ,O0OO0O0000O000OO0 ,O0OOO0OO000OOO000 #line:403
    def show_pool_bar (O0OO0000OOO00000O ,OOO0O0OO0O000OOOO ):#line:408
        OOO00OO0O0OOO000O =round (O0OO0000OOO00000O .score_best ,4 )#line:410
        OOO00000OOOOO0OOO =min (abs (O0OO0000OOO00000O .aim -O0OO0000OOO00000O .init_score_range [0 ]),abs (O0OO0000OOO00000O .aim -O0OO0000OOO00000O .init_score_range [1 ]))#line:412
        O000OO0OO000O0000 =abs (O0OO0000OOO00000O .aim -O0OO0000OOO00000O .score_best )#line:413
        O00OO0O0O00000O0O =min (abs (O0OO0000OOO00000O .aim -O0OO0000OOO00000O .gap_mean ),OOO00000OOOOO0OOO )#line:414
        if OOO00000OOOOO0OOO ==0 :#line:416
            OOO00000OOOOO0OOO =0.001 #line:417
        O00O0OO0O0OO00O00 =int (O000OO0OO000O0000 /OOO00000OOOOO0OOO *40 )#line:418
        O0000OOO0O000O000 =int ((O00OO0O0O00000O0O -O000OO0OO000O0000 )/OOO00000OOOOO0OOO *40 )#line:419
        O00O00000OO0O00O0 =40 -O00O0OO0O0OO00O00 -O0000OOO0O000O000 #line:420
        O0O0OOO00O00000O0 ='\r|{}+{}<{}| gen={}, best_score={}'.format (' '*O00O0OO0O0OO00O00 ,' '*O0000OOO0O000O000 ,' '*O00O00000OO0O00O0 ,OOO0O0OO0O000OOOO ,OOO00OO0O0OOO000O )#line:422
        print (O0O0OOO00O00000O0 ,end ='')#line:423
        if OOO0O0OO0O000OOOO ==0 :#line:425
            time .sleep (0.2 )#line:426
    def show_pool_print (OOOOO0OO00OO0O0O0 ,O00O0OOOOO000OOOO ):#line:428
        O00O0OOOOO000OOOO ,O0O0OO0O0OOO00000 ,OO0OO0O000O0OO000 ,O0O0O000O00O0000O ,OO00OO0O000OO00OO =OOOOO0OO00OO0O0O0 .make_fill (O00O0OOOOO000OOOO )#line:429
        print ('gen={}, best_score={}, mean_score={}, mean_gap={}, time={}'.format (O00O0OOOOO000OOOO ,O0O0OO0O0OOO00000 ,OO0OO0O000O0OO000 ,O0O0O000O00O0000O ,OO00OO0O000OO00OO ))#line:430
    def show_pool_plot (O00OO00000O00O0OO ,O00O0OOOO0OO0O000 ):#line:433
        O00O0OOOO0OO0O000 ,O0OO00OOOO00O0000 ,OO0O00000O0O000OO ,OO0O0OO0O0000OO0O ,OO0000OO0000OOOO0 =O00OO00000O00O0OO .make_fill (O00O0OOOO0OO0O000 )#line:434
        plt .bar (range (len (O00OO00000O00O0OO .pool_score [:100 ])),O00OO00000O00O0OO .pool_score [:100 ])#line:436
        plt .ylim ([min (O00OO00000O00O0OO .aim ,O00OO00000O00O0OO .init_score_range [0 ]),max (O00OO00000O00O0OO .aim ,O00OO00000O00O0OO .init_score_range [1 ])])#line:437
        plt .title ('gen        = {}{}best_score = {}{}mean_score = {}{}mean_gap   = {}{}time       =   {}'.format (O00O0OOOO0OO0O000 ,'\n',O0OO00OOOO00O0000 ,'\n',OO0O00000O0O000OO ,'\n',OO0O0OO0O0000OO0O ,'\n',OO0000OO0000OOOO0 ),loc ='left',fontname ='monospace')#line:438
        plt .show ();plt .close ();print ()#line:439
    def show_pool_save (OO0OOO0OOOOO0O000 ,OO0O0O000O000OO00 ):#line:442
        OO0OOO0OOOOO0O000 .show_pool_bar (OO0O0O000O000OO00 )#line:444
        O0O00O0O000O0O000 ,OO0O0OOO00O0O0O0O ,O0OOO000O0OOO0OOO ,O0000O000OO0O0OO0 ,O00OOOOO00OOO0OO0 =OO0OOO0OOOOO0O000 .make_fill (OO0O0O000O000OO00 )#line:446
        plt .bar (range (len (OO0OOO0OOOOO0O000 .pool_score [:100 ])),OO0OOO0OOOOO0O000 .pool_score [:100 ])#line:448
        plt .ylim ([min (OO0OOO0OOOOO0O000 .aim ,OO0OOO0OOOOO0O000 .init_score_range [0 ]),max (OO0OOO0OOOOO0O000 .aim ,OO0OOO0OOOOO0O000 .init_score_range [1 ])])#line:449
        plt .title ('gen        = {}{}best_score = {}{}mean_score = {}{}mean_gap   = {}{}time       =   {}'.format (O0O00O0O000O0O000 ,'\n',OO0O0OOO00O0O0O0O ,'\n',O0OOO000O0OOO0OOO ,'\n',O0000O000OO0O0OO0 ,'\n',O00OOOOO00OOO0OO0 ),loc ='left',fontname ='monospace')#line:450
        plt .subplots_adjust (left =0.1 ,right =0.95 ,bottom =0.1 ,top =0.70 )#line:451
        plt .savefig (OO0OOO0OOOOO0O000 .show_pool_func +'gen_{}.png'.format (str (OO0O0O000O000OO00 ).zfill (8 )));plt .close ()#line:452
    def opt2 (O0OOOOOOO0O0OOOO0 ,OO0OO0OOO00000000 ,O0000O00OOO0000O0 ,O0O00OO00OO0OOOO0 ,show_para_func =None ,seed =None ,step_max =float ('inf')):#line:458
        OO0OO0OOO00000000 ,O000000O00O0000O0 =np .array (OO0OO0OOO00000000 ),O0000O00OOO0000O0 (OO0OO0OOO00000000 )#line:460
        OO00O0OOO00OOOOO0 ={}#line:461
        if seed !='pass':nr .seed (seed )#line:462
        OOO0O0O0O00OO000O =0 #line:463
        if show_para_func !=None :#line:465
            OO00O0OOO00OOOOO0 .update ({'step_num':OOO0O0O0O00OO000O ,'score':round (O000000O00O0000O0 ,3 )})#line:466
            show_para_func (OO0OO0OOO00000000 ,**OO00O0OOO00OOOOO0 )#line:467
        while 1 :#line:469
            OO000O0O0O000O00O =False #line:470
            if OOO0O0O0O00OO000O >=step_max :#line:471
                break #line:473
            O000OOO00O000OO00 =np .arange (0 ,len (OO0OO0OOO00000000 )-1 )#line:475
            nr .shuffle (O000OOO00O000OO00 )#line:476
            for OO0OOOOOO000OOOOO in O000OOO00O000OO00 :#line:477
                if OO000O0O0O000O00O ==True :break #line:479
                OO0OO0OO0OOO0OO00 =np .arange (OO0OOOOOO000OOOOO +1 ,len (OO0OO0OOO00000000 ))#line:481
                nr .shuffle (OO0OO0OO0OOO0OO00 )#line:482
                for OOO000O00000O0OOO in OO0OO0OO0OOO0OO00 :#line:483
                    if OO000O0O0O000O00O ==True :break #line:485
                    OO00OO0OO0O00OO0O =np .hstack ((OO0OO0OOO00000000 [:OO0OOOOOO000OOOOO ],OO0OO0OOO00000000 [OO0OOOOOO000OOOOO :OOO000O00000O0OOO +1 ][::-1 ],OO0OO0OOO00000000 [OOO000O00000O0OOO +1 :]))#line:488
                    OOO00OOOO0O00OO0O =O0000O00OOO0000O0 (OO00OO0OO0O00OO0O )#line:489
                    if np .abs (O0O00OO00OO0OOOO0 -OOO00OOOO0O00OO0O )<np .abs (O0O00OO00OO0OOOO0 -O000000O00O0000O0 ):#line:492
                        OO0OO0OOO00000000 ,O000000O00O0000O0 =OO00OO0OO0O00OO0O ,OOO00OOOO0O00OO0O #line:493
                        OOO0O0O0O00OO000O +=1 #line:494
                        if show_para_func !=None :#line:495
                            OO00O0OOO00OOOOO0 .update ({'step_num':OOO0O0O0O00OO000O ,'score':round (O000000O00O0000O0 ,3 )})#line:496
                            show_para_func (OO0OO0OOO00000000 ,**OO00O0OOO00OOOOO0 )#line:497
                        OO000O0O0O000O00O =True #line:498
            if OO000O0O0O000O00O ==False :#line:499
                break #line:501
        return OO0OO0OOO00000000 ,O000000O00O0000O0 #line:502
    def opt2_tspGA (O0O00O00OOO0O0OOO ,OO00000OO00O0O000 ,OO000OOOO000OOO0O ,step_max =float ('inf')):#line:506
        OO00000OO00O0O000 ,OO000OOOO000OOO0O =OO00000OO00O0O000 ,OO000OOOO000OOO0O #line:508
        O0OOO0O0O00O00OOO =0 #line:509
        while 1 :#line:511
            OO00O000OOO0OO000 =False #line:512
            if O0OOO0O0O00O00OOO >=step_max :#line:513
                break #line:514
            O0OOOO0000O0O0OOO =np .arange (0 ,O0O00O00OOO0O0OOO .para_num -1 )#line:516
            nr .shuffle (O0OOOO0000O0O0OOO )#line:518
            for O00O0OO00OO0OOO00 in O0OOOO0000O0O0OOO :#line:519
                if OO00O000OOO0OO000 ==True :break #line:521
                O00O0O0OOOOOOOOOO =np .arange (O00O0OO00OO0OOO00 +1 ,O0O00O00OOO0O0OOO .para_num )#line:523
                nr .shuffle (O00O0O0OOOOOOOOOO )#line:524
                for O0000OO00OO0OOO0O in O00O0O0OOOOOOOOOO :#line:525
                    if OO00O000OOO0OO000 ==True :break #line:527
                    OOO0O0OOOO00O0OO0 =np .hstack ((OO00000OO00O0O000 [:O00O0OO00OO0OOO00 ],OO00000OO00O0O000 [O00O0OO00OO0OOO00 :O0000OO00OO0OOO0O +1 ][::-1 ],OO00000OO00O0O000 [O0000OO00OO0OOO0O +1 :]))#line:530
                    O0O00O0O0OO00O00O =O0O00O00OOO0O0OOO .score_func (O0O00O00OOO0O0OOO .para_range [OOO0O0OOOO00O0OO0 ])#line:531
                    if np .abs (O0O00O00OOO0O0OOO .aim -O0O00O0O0OO00O00O )<np .abs (O0O00O00OOO0O0OOO .aim -OO000OOOO000OOO0O ):#line:534
                        OO00000OO00O0O000 ,OO000OOOO000OOO0O =OOO0O0OOOO00O0OO0 ,O0O00O0O0OO00O00O #line:535
                        O0OOO0O0O00O00OOO +=1 #line:536
                        OO00O000OOO0OO000 =True #line:537
            if OO00O000OOO0OO000 ==False :#line:538
                break #line:540
        return OO00000OO00O0O000 ,OO000OOOO000OOO0O #line:541
    def tspGA_multi (OO0O0000O000OOO0O ,OOOO0O0O0OOOOOOO0 ):#line:570
        OOOOO0000OOO000O0 =OO0O0000O000OOO0O .pool [OOOO0O0O0OOOOOOO0 ]#line:572
        O0O0O00000O00O0OO =OO0O0000O000OOO0O .pool_score [OOOO0O0O0OOOOOOO0 ]#line:573
        OOOOOOOOOO0O000OO =np .ones ((OO0O0000O000OOO0O .child_num ,OO0O0000O000OOO0O .para_num ),dtype =int )#line:574
        O0OOOO0O00OOOO00O =np .zeros (OO0O0000O000OOO0O .child_num )#line:575
        OO0OO0O0OOO0O00OO =np .hstack ((OOOOO0000OOO000O0 [:,-2 :].reshape (OO0O0000O000OOO0O .parent_num ,2 ),OOOOO0000OOO000O0 ,OOOOO0000OOO000O0 [:,:2 ].reshape (OO0O0000O000OOO0O .parent_num ,2 )))#line:580
        for OOOOO00O0O0O0O00O in range (OO0O0000O000OOO0O .child_num ):#line:583
            O00O0O00000OOO000 =OOOOO0000OOO000O0 [nr .randint (OO0O0000O000OOO0O .parent_num ),0 ]#line:585
            if nr .rand ()<(1.0 /OO0O0000O000OOO0O .para_num ):#line:586
                O00O0O00000OOO000 =nr .choice (OO0O0000O000OOO0O .para_index )#line:587
            OOOOOOOOOO0O000OO [OOOOO00O0O0O0O00O ,0 ]=O00O0O00000OOO000 #line:588
            for O0O0O0O0000OO00OO in range (1 ,OO0O0000O000OOO0O .para_num ):#line:590
                OO0OO00OO00O0OOO0 =np .zeros ((OO0O0000O000OOO0O .parent_num ,OO0O0000O000OOO0O .para_num +4 ),dtype =bool )#line:592
                OOO0OOO0OOO0000O0 =np .zeros ((OO0O0000O000OOO0O .parent_num ,OO0O0000O000OOO0O .para_num +4 ),dtype =bool )#line:593
                OO0OO00OO00O0OOO0 [:,1 :-3 ]+=(OO0O0000O000OOO0O .parent ==O00O0O00000OOO000 )#line:595
                OO0OO00OO00O0OOO0 [:,3 :-1 ]+=(OO0O0000O000OOO0O .parent ==O00O0O00000OOO000 )#line:596
                OOO0OOO0OOO0000O0 [:,0 :-4 ]+=(OO0O0000O000OOO0O .parent ==O00O0O00000OOO000 )#line:597
                OOO0OOO0OOO0000O0 [:,4 :]+=(OO0O0000O000OOO0O .parent ==O00O0O00000OOO000 )#line:598
                OO0O0OOO00OO00O0O =np .ones (OO0O0000O000OOO0O .para_num )*(1.0 /OO0O0000O000OOO0O .para_num )#line:601
                for O00O0O0OO0O00OO00 in OO0OO0O0OOO0O00OO [OO0OO00OO00O0OOO0 ]:#line:602
                    OO0O0OOO00OO00O0O [np .where (OO0O0000O000OOO0O .para_index ==O00O0O0OO0O00OO00 )[0 ]]+=1.0 /OO0O0000O000OOO0O .parent_num #line:603
                for O00O0O0OO0O00OO00 in OO0OO0O0OOO0O00OO [OOO0OOO0OOO0000O0 ]:#line:604
                    OO0O0OOO00OO00O0O [np .where (OO0O0000O000OOO0O .para_index ==O00O0O0OO0O00OO00 )[0 ]]+=0.1 /OO0O0000O000OOO0O .parent_num #line:605
                for O00O0O0OO0O00OO00 in OOOOOOOOOO0O000OO [OOOOO00O0O0O0O00O ,0 :O0O0O0O0000OO00OO ]:#line:608
                    OO0O0OOO00OO00O0O [np .where (OO0O0000O000OOO0O .para_index ==O00O0O0OO0O00OO00 )[0 ]]=0.0 #line:609
                OO0O0OOO00OO00O0O *=1.0 /np .sum (OO0O0OOO00OO00O0O )#line:612
                O00O0O00000OOO000 =nr .choice (OO0O0000O000OOO0O .para_index ,p =OO0O0OOO00OO00O0O )#line:613
                OOOOOOOOOO0O000OO [OOOOO00O0O0O0O00O ,O0O0O0O0000OO00OO ]=O00O0O00000OOO000 #line:615
        for OOOOO00O0O0O0O00O in range (OO0O0000O000OOO0O .child_num ):#line:619
            OO0OO00O0000O00OO =OO0O0000O000OOO0O .para_range [OOOOOOOOOO0O000OO [OOOOO00O0O0O0O00O ]]#line:620
            O0OOOO0O00OOOO00O [OOOOO00O0O0O0O00O ]=OO0O0000O000OOO0O .score_func (OO0OO00O0000O00OO )#line:621
        OO0000O0OO0OO0OO0 =np .vstack ((OOOOOOOOOO0O000OO ,OOOOO0000OOO000O0 ))#line:623
        O0000OOO0OO0O0OO0 =np .hstack ((O0OOOO0O00OOOO00O ,O0O0O00000O00O0OO ))#line:624
        for OOOOO00O0O0O0O00O in range (OO0O0000O000OOO0O .family_num ):#line:626
            OO0000O0OO0OO0OO0 [OOOOO00O0O0O0O00O ],O0000OOO0OO0O0OO0 [OOOOO00O0O0O0O00O ]=OO0O0000O000OOO0O .opt2_tspGA (OO0000O0OO0OO0OO0 [OOOOO00O0O0O0O00O ],O0000OOO0OO0O0OO0 [OOOOO00O0O0O0O00O ],step_max =OO0O0000O000OOO0O .opt2_num )#line:627
        OOOO00OOOOO0000OO =np .argpartition (np .abs (OO0O0000O000OOO0O .aim -O0000OOO0OO0O0OO0 ),OO0O0000O000OOO0O .parent_num )[:OO0O0000O000OOO0O .parent_num ]#line:629
        OO0O0000O000OOO0O .pool [OOOO0O0O0OOOOOOO0 ]=OO0000O0OO0OO0OO0 [OOOO00OOOOO0000OO ]#line:630
        OO0O0000O000OOO0O .pool_score [OOOO0O0O0OOOOOOO0 ]=O0000OOO0OO0O0OO0 [OOOO00OOOOO0000OO ]#line:631
    def tspGA (OO00O0OO0O0OOOO0O ,OOO000OO000OOO0O0 ,O0O000000O0O0O000 ,OO00000OO0OO00OO0 ,show_pool_func ='bar',seed =None ,pool_num =None ,max_gen =None ,core_num =1 ):#line:633
        OOO000OO000OOO0O0 =np .array (OOO000OO000OOO0O0 )#line:638
        OO00O0OO0O0OOOO0O .setting_1 (OOO000OO000OOO0O0 ,O0O000000O0O0O000 ,OO00000OO0OO00OO0 ,show_pool_func ,seed ,pool_num ,max_gen ,core_num )#line:641
        OO00O0OO0O0OOOO0O .setting_2 (OO00O0OO0O0OOOO0O .para_num *10 ,2 ,4 )#line:642
        OO00O0OO0O0OOOO0O .setting_3 (int )#line:643
        OO00O0OO0O0OOOO0O .print_info ()#line:644
        OO00O0OO0O0OOOO0O .para_index =np .arange (OO00O0OO0O0OOOO0O .para_num )#line:647
        OO00O0OO0O0OOOO0O .opt2_num =1 #line:648
        for O0O00000000O00000 in range (OO00O0OO0O0OOOO0O .pool_num ):#line:651
            OO00O0OO0O0OOOO0O .pool [O0O00000000O00000 ]=deepcopy (OO00O0OO0O0OOOO0O .para_index )#line:652
            nr .shuffle (OO00O0OO0O0OOOO0O .pool [O0O00000000O00000 ])#line:653
        OO00O0OO0O0OOOO0O .score_pool ()#line:656
        for O0O00000000O00000 in range (OO00O0OO0O0OOOO0O .pool_num ):#line:659
            OO00O0OO0O0OOOO0O .pool [O0O00000000O00000 ],OO00O0OO0O0OOOO0O .pool_score [O0O00000000O00000 ]=OO00O0OO0O0OOOO0O .opt2_tspGA (OO00O0OO0O0OOOO0O .pool [O0O00000000O00000 ],OO00O0OO0O0OOOO0O .pool_score [O0O00000000O00000 ],step_max =OO00O0OO0O0OOOO0O .opt2_num )#line:660
            if OO00O0OO0O0OOOO0O .show_pool_func !=None :#line:661
                OOO00OO00O0000O00 ='\rMini 2-opting first gen {}/{}        '.format (O0O00000000O00000 +1 ,OO00O0OO0O0OOOO0O .pool_num )#line:662
                print (OOO00OO00O0000O00 ,end ='')#line:663
        if OO00O0OO0O0OOOO0O .show_pool_func !=None :print ()#line:664
        OO00O0OO0O0OOOO0O .save_best_mean ()#line:667
        OO00O0OO0O0OOOO0O .init_score_range =(np .min (OO00O0OO0O0OOOO0O .pool_score ),np .max (OO00O0OO0O0OOOO0O .pool_score ))#line:669
        OO00O0OO0O0OOOO0O .init_gap_mean =deepcopy (OO00O0OO0O0OOOO0O .gap_mean )#line:670
        if OO00O0OO0O0OOOO0O .show_pool_func ==None :pass #line:673
        elif OO00O0OO0O0OOOO0O .show_pool_func =='bar':OO00O0OO0O0OOOO0O .show_pool_bar (0 )#line:674
        elif OO00O0OO0O0OOOO0O .show_pool_func =='print':OO00O0OO0O0OOOO0O .show_pool_print (0 )#line:675
        elif OO00O0OO0O0OOOO0O .show_pool_func =='plot':OO00O0OO0O0OOOO0O .show_pool_plot (0 )#line:676
        elif callable (OO00O0OO0O0OOOO0O .show_pool_func ):OO00O0OO0O0OOOO0O .show_pool (0 )#line:677
        elif type (show_pool_func )==str :#line:678
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:679
                if not os .path .exists (show_pool_func ):os .mkdir (show_pool_func )#line:680
                OO00O0OO0O0OOOO0O .show_pool_save (0 )#line:681
        OO0O0O000OOO0OO0O =0 #line:684
        for OOO00OOOOO00OO0OO in range (1 ,OO00O0OO0O0OOOO0O .max_n +1 ):#line:685
            O000O00OO0OOO00O0 =np .arange (OO00O0OO0O0OOOO0O .pool_num )#line:690
            nr .shuffle (O000O00OO0OOO00O0 )#line:691
            O000O00OO0OOO00O0 =O000O00OO0OOO00O0 .reshape ((OO00O0OO0O0OOOO0O .pool_num //OO00O0OO0O0OOOO0O .parent_num ),OO00O0OO0O0OOOO0O .parent_num )#line:692
            Parallel (n_jobs =OO00O0OO0O0OOOO0O .core_num ,require ='sharedmem')([delayed (OO00O0OO0O0OOOO0O .tspGA_multi )(OO0O00O0O000O0000 )for OO0O00O0O000O0000 in O000O00OO0OOO00O0 ])#line:695
            OO0O0O000OOO0OO0O +=OO00O0OO0O0OOOO0O .end_check ()#line:752
            OO00O0OO0O0OOOO0O .save_best_mean ()#line:755
            if OO00O0OO0O0OOOO0O .show_pool_func ==None :pass #line:758
            elif OO00O0OO0O0OOOO0O .show_pool_func =='bar':OO00O0OO0O0OOOO0O .show_pool_bar (OOO00OOOOO00OO0OO *OO00O0OO0O0OOOO0O .pool_num )#line:759
            elif OO00O0OO0O0OOOO0O .show_pool_func =='print':OO00O0OO0O0OOOO0O .show_pool_print (OOO00OOOOO00OO0OO *OO00O0OO0O0OOOO0O .pool_num )#line:760
            elif OO00O0OO0O0OOOO0O .show_pool_func =='plot':OO00O0OO0O0OOOO0O .show_pool_plot (OOO00OOOOO00OO0OO *OO00O0OO0O0OOOO0O .pool_num )#line:761
            elif callable (OO00O0OO0O0OOOO0O .show_pool_func ):OO00O0OO0O0OOOO0O .show_pool (OOO00OOOOO00OO0OO *OO00O0OO0O0OOOO0O .pool_num )#line:762
            elif type (show_pool_func )==str :#line:763
                if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:764
                    OO00O0OO0O0OOOO0O .show_pool_save (OOO00OOOOO00OO0OO )#line:765
            if OO0O0O000OOO0OO0O >=1 :#line:768
                break #line:769
        OOO0OO0OO0O00OOOO =OO00O0OO0O0OOOO0O .para_range [OO00O0OO0O0OOOO0O .pool_best ]#line:772
        if OO00O0OO0O0OOOO0O .show_pool_func =='bar':print ()#line:775
        elif type (show_pool_func )==str :#line:776
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:777
                print ()#line:778
        OO00O0OO0O0OOOO0O .print_result (OOO0OO0OO0O00OOOO )#line:781
        return OOO0OO0OO0O00OOOO ,OO00O0OO0O0OOOO0O .score_best #line:783
    def dcGA_multi (OO00000OO000OOO00 ,OO0O0OOO0OOOO00OO ):#line:811
        O0O0OO0O0O00O00O0 =OO00000OO000OOO00 .pool [OO0O0OOO0OOOO00OO ]#line:813
        O0000000OO0O000OO =OO00000OO000OOO00 .pool_score [OO0O0OOO0OOOO00OO ]#line:814
        OOO0OOO0OOOO0OO0O =np .zeros ((OO00000OO000OOO00 .child_num ,OO00000OO000OOO00 .para_num ),dtype =int )#line:815
        OOOO000O0OOOO0OOO =np .zeros (OO00000OO000OOO00 .child_num )#line:816
        if OO00000OO000OOO00 .para_num >=3 :#line:819
            OO00OOO000000OOO0 =nr .choice (range (1 ,OO00000OO000OOO00 .para_num ),2 ,replace =False )#line:823
            if OO00OOO000000OOO0 [0 ]>OO00OOO000000OOO0 [1 ]:#line:824
                OO00OOO000000OOO0 [0 ],OO00OOO000000OOO0 [1 ]=OO00OOO000000OOO0 [1 ],OO00OOO000000OOO0 [0 ]#line:825
            for O00O0O0OO0OO00O0O in range (len (OO00000OO000OOO00 .choice )):#line:827
                OOO0OOO0OOOO0OO0O [O00O0O0OO0OO00O0O ]=np .hstack ((O0O0OO0O0O00O00O0 [OO00000OO000OOO00 .choice [O00O0O0OO0OO00O0O ,0 ],:OO00OOO000000OOO0 [0 ]],O0O0OO0O0O00O00O0 [OO00000OO000OOO00 .choice [O00O0O0OO0OO00O0O ,1 ],OO00OOO000000OOO0 [0 ]:OO00OOO000000OOO0 [1 ]],O0O0OO0O0O00O00O0 [OO00000OO000OOO00 .choice [O00O0O0OO0OO00O0O ,2 ],OO00OOO000000OOO0 [1 ]:]))#line:830
            for O00O0O0OO0OO00O0O in [2 ,3 ]:#line:835
                O0O00OO0000O00OOO =nr .randint (0 ,2 ,OO00000OO000OOO00 .para_num )#line:836
                OOO0OOO0OOOO0OO0O [O00O0O0OO0OO00O0O ][O0O00OO0000O00OOO ==0 ]=O0O0OO0O0O00O00O0 [0 ][O0O00OO0000O00OOO ==0 ]#line:837
                OOO0OOO0OOOO0OO0O [O00O0O0OO0OO00O0O ][O0O00OO0000O00OOO ==1 ]=O0O0OO0O0O00O00O0 [1 ][O0O00OO0000O00OOO ==1 ]#line:838
            for OO0O0O0OOO00OOO00 in OOO0OOO0OOOO0OO0O :#line:842
                for OOO0O00000OO0000O in range (OO00000OO000OOO00 .para_num ):#line:843
                    if nr .rand ()<(1.0 /OO00000OO000OOO00 .para_num ):#line:844
                        OO0O0O0OOO00OOO00 [OOO0O00000OO0000O ]=nr .choice (OO00000OO000OOO00 .para_index [OOO0O00000OO0000O ])#line:845
        elif OO00000OO000OOO00 .para_num ==2 :#line:849
            OOO0OOO0OOOO0OO0O [:2 ]=np .array ([[O0O0OO0O0O00O00O0 [0 ,0 ],O0O0OO0O0O00O00O0 [1 ,1 ]],[O0O0OO0O0O00O00O0 [0 ,1 ],O0O0OO0O0O00O00O0 [1 ,0 ]]])#line:851
            for O00O0O0OO0OO00O0O in range (2 ,OO00000OO000OOO00 .child_num ):#line:853
                for OOO0O00000OO0000O in range (2 ):#line:854
                    OOO0OOO0OOOO0OO0O [O00O0O0OO0OO00O0O ,OOO0O00000OO0000O ]=nr .choice (OO00000OO000OOO00 .para_index [OOO0O00000OO0000O ])#line:855
        elif OO00000OO000OOO00 .para_num ==1 :#line:857
            for O00O0O0OO0OO00O0O in range (OO00000OO000OOO00 .child_num ):#line:859
                OOO0OOO0OOOO0OO0O [O00O0O0OO0OO00O0O ]=nr .choice (OO00000OO000OOO00 .para_index [0 ])#line:860
        for O00O0O0OO0OO00O0O in range (OO00000OO000OOO00 .child_num ):#line:864
            O00000OOO00000O00 =[]#line:865
            for OOO0O00000OO0000O in range (OO00000OO000OOO00 .para_num ):#line:866
                O00000OOO00000O00 .append (OO00000OO000OOO00 .para_range [OOO0O00000OO0000O ][OOO0OOO0OOOO0OO0O [O00O0O0OO0OO00O0O ,OOO0O00000OO0000O ]])#line:867
            O00000OOO00000O00 =np .array (O00000OOO00000O00 )#line:868
            OOOO000O0OOOO0OOO [O00O0O0OO0OO00O0O ]=OO00000OO000OOO00 .score_func (O00000OOO00000O00 )#line:869
        OOOOO0OOOO0000O00 =np .vstack ((OOO0OOO0OOOO0OO0O ,O0O0OO0O0O00O00O0 ))#line:871
        O0000O0OO00O0000O =np .hstack ((OOOO000O0OOOO0OOO ,O0000000OO0O000OO ))#line:872
        OO0O00O0OO0O0O000 =np .argpartition (np .abs (OO00000OO000OOO00 .aim -O0000O0OO00O0000O ),OO00000OO000OOO00 .parent_num )[:OO00000OO000OOO00 .parent_num ]#line:874
        OO00000OO000OOO00 .pool [OO0O0OOO0OOOO00OO ]=OOOOO0OOOO0000O00 [OO0O00O0OO0O0O000 ]#line:875
        OO00000OO000OOO00 .pool_score [OO0O0OOO0OOOO00OO ]=O0000O0OO00O0000O [OO0O00O0OO0O0O000 ]#line:876
    def dcGA (O00000O0O0O0OOO0O ,O00000OO00OO00O0O ,OOO00OOOOOOOOOOO0 ,OOO0O00O0OOO000OO ,show_pool_func ='bar',seed =None ,pool_num =None ,max_gen =None ,core_num =1 ):#line:879
        if type (O00000OO00OO00O0O )==list :#line:884
            if isinstance (O00000OO00OO00O0O [0 ],list )==False :#line:885
                O00000OO00OO00O0O =[O00000OO00OO00O0O ]#line:886
        if type (O00000OO00OO00O0O )==np .ndarray :#line:887
            if O00000OO00OO00O0O .ndim ==1 :#line:888
                O00000OO00OO00O0O =O00000OO00OO00O0O .reshape (1 ,len (O00000OO00OO00O0O ))#line:889
        O00000O0O0O0OOO0O .setting_1 (O00000OO00OO00O0O ,OOO00OOOOOOOOOOO0 ,OOO0O00O0OOO000OO ,show_pool_func ,seed ,pool_num ,max_gen ,core_num )#line:892
        O00000O0O0O0OOO0O .setting_2 (O00000O0O0O0OOO0O .para_num *10 ,2 ,4 )#line:893
        O00000O0O0O0OOO0O .setting_3 (int )#line:894
        O00000O0O0O0OOO0O .print_info ()#line:895
        O00000O0O0O0OOO0O .para_index =[]#line:898
        for O0000O0OOO0O00O0O in range (O00000O0O0O0OOO0O .para_num ):#line:899
            O00000O0O0O0OOO0O .para_index .append (np .arange (len (O00000O0O0O0OOO0O .para_range [O0000O0OOO0O00O0O ])))#line:900
        O00000O0O0O0OOO0O .choice =np .array ([[0 ,1 ,0 ],[1 ,0 ,1 ]],dtype =int )#line:901
        for O0000O0OOO0O00O0O in range (O00000O0O0O0OOO0O .pool_num ):#line:904
            for O0O0O0OOOO000O00O in range (O00000O0O0O0OOO0O .para_num ):#line:905
                O00000O0O0O0OOO0O .pool [O0000O0OOO0O00O0O ,O0O0O0OOOO000O00O ]=nr .choice (O00000O0O0O0OOO0O .para_index [O0O0O0OOOO000O00O ])#line:906
        O00000O0O0O0OOO0O .score_pool_dc ()#line:909
        O00000O0O0O0OOO0O .save_best_mean ()#line:910
        O00000O0O0O0OOO0O .init_score_range =(np .min (O00000O0O0O0OOO0O .pool_score ),np .max (O00000O0O0O0OOO0O .pool_score ))#line:912
        O00000O0O0O0OOO0O .init_gap_mean =deepcopy (O00000O0O0O0OOO0O .gap_mean )#line:913
        if O00000O0O0O0OOO0O .show_pool_func ==None :pass #line:916
        elif O00000O0O0O0OOO0O .show_pool_func =='bar':O00000O0O0O0OOO0O .show_pool_bar (0 )#line:917
        elif O00000O0O0O0OOO0O .show_pool_func =='print':O00000O0O0O0OOO0O .show_pool_print (0 )#line:918
        elif O00000O0O0O0OOO0O .show_pool_func =='plot':O00000O0O0O0OOO0O .show_pool_plot (0 )#line:919
        elif callable (O00000O0O0O0OOO0O .show_pool_func ):O00000O0O0O0OOO0O .show_pool_dc (0 )#line:920
        elif type (show_pool_func )==str :#line:921
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:922
                if not os .path .exists (show_pool_func ):os .mkdir (show_pool_func )#line:923
                O00000O0O0O0OOO0O .show_pool_save (0 )#line:924
        O0O000000OOO0OO00 =0 #line:927
        for OOO0OO00O00O0O000 in range (1 ,O00000O0O0O0OOO0O .max_n +1 ):#line:928
            OO00O0OO0000OO0OO =np .arange (O00000O0O0O0OOO0O .pool_num )#line:931
            nr .shuffle (OO00O0OO0000OO0OO )#line:932
            OO00O0OO0000OO0OO =OO00O0OO0000OO0OO .reshape ((O00000O0O0O0OOO0O .pool_num //O00000O0O0O0OOO0O .parent_num ),O00000O0O0O0OOO0O .parent_num )#line:933
            Parallel (n_jobs =O00000O0O0O0OOO0O .core_num ,require ='sharedmem')([delayed (O00000O0O0O0OOO0O .dcGA_multi )(O00000OOOO00000OO )for O00000OOOO00000OO in OO00O0OO0000OO0OO ])#line:936
            O0O000000OOO0OO00 +=O00000O0O0O0OOO0O .end_check ()#line:992
            O00000O0O0O0OOO0O .save_best_mean ()#line:995
            if O00000O0O0O0OOO0O .show_pool_func ==None :pass #line:998
            elif O00000O0O0O0OOO0O .show_pool_func =='bar':O00000O0O0O0OOO0O .show_pool_bar (OOO0OO00O00O0O000 *O00000O0O0O0OOO0O .pool_num )#line:999
            elif O00000O0O0O0OOO0O .show_pool_func =='print':O00000O0O0O0OOO0O .show_pool_print (OOO0OO00O00O0O000 *O00000O0O0O0OOO0O .pool_num )#line:1000
            elif O00000O0O0O0OOO0O .show_pool_func =='plot':O00000O0O0O0OOO0O .show_pool_plot (OOO0OO00O00O0O000 *O00000O0O0O0OOO0O .pool_num )#line:1001
            elif callable (O00000O0O0O0OOO0O .show_pool_func ):O00000O0O0O0OOO0O .show_pool_dc (OOO0OO00O00O0O000 *O00000O0O0O0OOO0O .pool_num )#line:1002
            elif type (show_pool_func )==str :#line:1003
                if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1004
                    O00000O0O0O0OOO0O .show_pool_save (OOO0OO00O00O0O000 )#line:1005
            if O0O000000OOO0OO00 >=1 :#line:1008
                break #line:1009
        OO000O000O000OOOO =[]#line:1012
        for O0O0O0OOOO000O00O in range (O00000O0O0O0OOO0O .para_num ):#line:1013
            OO000O000O000OOOO .append (O00000O0O0O0OOO0O .para_range [O0O0O0OOOO000O00O ][O00000O0O0O0OOO0O .pool [O00000O0O0O0OOO0O .best_index ,O0O0O0OOOO000O00O ]])#line:1014
        OO000O000O000OOOO =np .array (OO000O000O000OOOO )#line:1015
        if O00000O0O0O0OOO0O .show_pool_func =='bar':print ()#line:1018
        elif type (show_pool_func )==str :#line:1019
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1020
                print ()#line:1021
        O00000O0O0O0OOO0O .print_result (OO000O000O000OOOO )#line:1024
        return OO000O000O000OOOO ,O00000O0O0O0OOO0O .score_best #line:1026
    def setGA_multi (O00OO00OO0O0OO0OO ,OO00000O0O0O000OO ):#line:1056
        OOOOO00O0O0000OO0 =O00OO00OO0O0OO0OO .pool [OO00000O0O0O000OO ]#line:1058
        OOO0OO00O00O00O0O =O00OO00OO0O0OO0OO .pool_score [OO00000O0O0O000OO ]#line:1059
        O0OO0000O00O00O00 =np .zeros ((O00OO00OO0O0OO0OO .child_num ,O00OO00OO0O0OO0OO .para_num ),dtype =int )#line:1060
        OOO0O0000OOO00OOO =np .zeros (O00OO00OO0O0OO0OO .child_num )#line:1061
        OO00O000OOOO000OO =set (OOOOO00O0O0000OO0 [0 ])&set (OOOOO00O0O0000OO0 [1 ])#line:1066
        O0OO0OO0O0OOOOOO0 =set (O00OO00OO0O0OO0OO .para_index )-OO00O000OOOO000OO #line:1068
        for OO0000O00OOO0OO00 in range (len (O0OO0000O00O00O00 )):#line:1070
            O0OO0O0O00OOO00OO =nr .choice (np .array (list (O0OO0OO0O0OOOOOO0 )),O00OO00OO0O0OO0OO .set_num -len (OO00O000OOOO000OO ),replace =False )#line:1071
            O0OO0000O00O00O00 [OO0000O00OOO0OO00 ]=np .hstack ((np .array (list (OO00O000OOOO000OO )),O0OO0O0O00OOO00OO ))#line:1073
        for O0000OO0000O00000 in O0OO0000O00O00O00 [2 :]:#line:1080
            for OOOOO0OOO00OO0O0O in range (O00OO00OO0O0OO0OO .set_num ):#line:1081
                if nr .rand ()<(1.0 /O00OO00OO0O0OO0OO .set_num ):#line:1082
                    O000OOO00O00OOOO0 =nr .choice (O00OO00OO0O0OO0OO .para_index )#line:1083
                    if O000OOO00O00OOOO0 not in O0000OO0000O00000 :#line:1084
                        O0000OO0000O00000 [OOOOO0OOO00OO0O0O ]=O000OOO00O00OOOO0 #line:1085
        for OO0000O00OOO0OO00 in range (O00OO00OO0O0OO0OO .child_num ):#line:1090
            O000OO000O000OOO0 =O00OO00OO0O0OO0OO .para_range [O0OO0000O00O00O00 [OO0000O00OOO0OO00 ]]#line:1091
            OOO0O0000OOO00OOO [OO0000O00OOO0OO00 ]=O00OO00OO0O0OO0OO .score_func (O000OO000O000OOO0 )#line:1092
        OOOO0OOO0OO00O00O =np .vstack ((O0OO0000O00O00O00 ,OOOOO00O0O0000OO0 ))#line:1094
        O000OO000OOO0OOOO =np .hstack ((OOO0O0000OOO00OOO ,OOO0OO00O00O00O0O ))#line:1095
        O00OOO000OOOOO00O =np .argpartition (np .abs (O00OO00OO0O0OO0OO .aim -O000OO000OOO0OOOO ),O00OO00OO0O0OO0OO .parent_num )[:O00OO00OO0O0OO0OO .parent_num ]#line:1097
        O00OO00OO0O0OO0OO .pool [OO00000O0O0O000OO ]=OOOO0OOO0OO00O00O [O00OOO000OOOOO00O ]#line:1098
        O00OO00OO0O0OO0OO .pool_score [OO00000O0O0O000OO ]=O000OO000OOO0OOOO [O00OOO000OOOOO00O ]#line:1099
    def setGA (OO0OO0O0OOOOO0000 ,O00OO000O0OO000O0 ,OO000000OOO0O0OOO ,O0O0000OO00O0000O ,OO00OO0OO0OOOOO00 ,show_pool_func ='bar',seed =None ,pool_num =None ,max_gen =None ,core_num =1 ):#line:1101
        O00OO000O0OO000O0 =np .array (O00OO000O0OO000O0 )#line:1106
        OO0OO0O0OOOOO0000 .setting_1 (O00OO000O0OO000O0 ,O0O0000OO00O0000O ,OO00OO0OO0OOOOO00 ,show_pool_func ,seed ,pool_num ,max_gen ,core_num )#line:1109
        OO0OO0O0OOOOO0000 .set_num =OO000000OOO0O0OOO #line:1110
        OO0OO0O0OOOOO0000 .para_num =OO0OO0O0OOOOO0000 .set_num #line:1111
        OO0OO0O0OOOOO0000 .setting_2 (OO0OO0O0OOOOO0000 .para_num *10 ,2 ,4 )#line:1112
        OO0OO0O0OOOOO0000 .setting_3 (int )#line:1113
        OO0OO0O0OOOOO0000 .print_info ()#line:1114
        OO0OO0O0OOOOO0000 .para_index =np .arange (len (OO0OO0O0OOOOO0000 .para_range ))#line:1117
        for O0OOOO0000OO0OO00 in range (OO0OO0O0OOOOO0000 .pool_num ):#line:1120
            OO0OO0O0OOOOO0000 .pool [O0OOOO0000OO0OO00 ]=nr .choice (OO0OO0O0OOOOO0000 .para_index ,OO0OO0O0OOOOO0000 .set_num ,replace =False )#line:1121
        OO0OO0O0OOOOO0000 .score_pool ()#line:1125
        OO0OO0O0OOOOO0000 .save_best_mean ()#line:1126
        OO0OO0O0OOOOO0000 .init_score_range =(np .min (OO0OO0O0OOOOO0000 .pool_score ),np .max (OO0OO0O0OOOOO0000 .pool_score ))#line:1128
        OO0OO0O0OOOOO0000 .init_gap_mean =deepcopy (OO0OO0O0OOOOO0000 .gap_mean )#line:1129
        if OO0OO0O0OOOOO0000 .show_pool_func ==None :pass #line:1132
        elif OO0OO0O0OOOOO0000 .show_pool_func =='bar':OO0OO0O0OOOOO0000 .show_pool_bar (0 )#line:1133
        elif OO0OO0O0OOOOO0000 .show_pool_func =='print':OO0OO0O0OOOOO0000 .show_pool_print (0 )#line:1134
        elif OO0OO0O0OOOOO0000 .show_pool_func =='plot':OO0OO0O0OOOOO0000 .show_pool_plot (0 )#line:1135
        elif callable (OO0OO0O0OOOOO0000 .show_pool_func ):OO0OO0O0OOOOO0000 .show_pool (0 )#line:1136
        elif type (show_pool_func )==str :#line:1137
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1138
                if not os .path .exists (show_pool_func ):os .mkdir (show_pool_func )#line:1139
                OO0OO0O0OOOOO0000 .show_pool_save (0 )#line:1140
        O000O00000O0OOO00 =0 #line:1143
        for O00O00OOO00OOOO0O in range (1 ,OO0OO0O0OOOOO0000 .max_n +1 ):#line:1144
            OO0OOO00O00OOOOO0 =np .arange (OO0OO0O0OOOOO0000 .pool_num )#line:1147
            nr .shuffle (OO0OOO00O00OOOOO0 )#line:1148
            OO0OOO00O00OOOOO0 =OO0OOO00O00OOOOO0 .reshape ((OO0OO0O0OOOOO0000 .pool_num //OO0OO0O0OOOOO0000 .parent_num ),OO0OO0O0OOOOO0000 .parent_num )#line:1149
            Parallel (n_jobs =OO0OO0O0OOOOO0000 .core_num ,require ='sharedmem')([delayed (OO0OO0O0OOOOO0000 .setGA_multi )(O0O00OO0OOO00OOO0 )for O0O00OO0OOO00OOO0 in OO0OOO00O00OOOOO0 ])#line:1152
            O000O00000O0OOO00 +=OO0OO0O0OOOOO0000 .end_check ()#line:1188
            OO0OO0O0OOOOO0000 .save_best_mean ()#line:1191
            if OO0OO0O0OOOOO0000 .show_pool_func ==None :pass #line:1194
            elif OO0OO0O0OOOOO0000 .show_pool_func =='bar':OO0OO0O0OOOOO0000 .show_pool_bar (O00O00OOO00OOOO0O *OO0OO0O0OOOOO0000 .pool_num )#line:1195
            elif OO0OO0O0OOOOO0000 .show_pool_func =='print':OO0OO0O0OOOOO0000 .show_pool_print (O00O00OOO00OOOO0O *OO0OO0O0OOOOO0000 .pool_num )#line:1196
            elif OO0OO0O0OOOOO0000 .show_pool_func =='plot':OO0OO0O0OOOOO0000 .show_pool_plot (O00O00OOO00OOOO0O *OO0OO0O0OOOOO0000 .pool_num )#line:1197
            elif callable (OO0OO0O0OOOOO0000 .show_pool_func ):OO0OO0O0OOOOO0000 .show_pool (O00O00OOO00OOOO0O *OO0OO0O0OOOOO0000 .pool_num )#line:1198
            elif type (show_pool_func )==str :#line:1199
                if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1200
                    OO0OO0O0OOOOO0000 .show_pool_save (O00O00OOO00OOOO0O )#line:1201
            if O000O00000O0OOO00 >=1 :#line:1204
                break #line:1205
        O0O0O0000000OO0O0 =OO0OO0O0OOOOO0000 .para_range [OO0OO0O0OOOOO0000 .pool_best ]#line:1208
        if OO0OO0O0OOOOO0000 .show_pool_func =='bar':print ()#line:1211
        elif type (show_pool_func )==str :#line:1212
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1213
                print ()#line:1214
        OO0OO0O0OOOOO0000 .print_result (O0O0O0000000OO0O0 )#line:1217
        return O0O0O0000000OO0O0 ,OO0OO0O0OOOOO0000 .score_best #line:1219
    def rcGA_multi (O0O0OO0OOO000O0OO ,OOO00OO00OOO0000O ):#line:1247
        OO000OOO0O0OOO000 =O0O0OO0OOO000O0OO .pool [OOO00OO00OOO0000O ]#line:1249
        O0O00OOOOO000O000 =O0O0OO0OOO000O0OO .pool_score [OOO00OO00OOO0000O ]#line:1250
        OO000O00O000OOO0O =np .ones ((O0O0OO0OOO000O0OO .child_num ,O0O0OO0OOO000O0OO .para_num ),dtype =float )*2.0 #line:1251
        OO00O00OO0OO00OO0 =np .zeros (O0O0OO0OOO000O0OO .child_num )#line:1252
        OO0O0O000OO00OO00 =np .mean (OO000OOO0O0OOO000 ,axis =0 )#line:1257
        for OO0O0O0O000O0000O in range (O0O0OO0OOO000O0OO .child_num ):#line:1260
            for OO00O0O00O00O00O0 in range (O0O0OO0OOO000O0OO .para_num ):#line:1261
                OO000O00O000OOO0O [OO0O0O0O000O0000O ,OO00O0O00O00O00O0 ]=OO0O0O000OO00OO00 [OO00O0O00O00O00O0 ]#line:1263
                for O0000O00O0O0OO000 in range (O0O0OO0OOO000O0OO .parent_num ):#line:1265
                    OO000O00O000OOO0O [OO0O0O0O000O0000O ,OO00O0O00O00O00O0 ]+=nr .normal (0 ,O0O0OO0OOO000O0OO .sd )*(OO000OOO0O0OOO000 [O0000O00O0O0OO000 ][OO00O0O00O00O00O0 ]-OO0O0O000OO00OO00 [OO00O0O00O00O00O0 ])#line:1266
        OO000O00O000OOO0O =np .clip (OO000O00O000OOO0O ,0.0 ,1.0 )#line:1268
        for OO0O0O0O000O0000O in range (O0O0OO0OOO000O0OO .child_num ):#line:1272
            OOO0000OOO000O0O0 =OO000O00O000OOO0O [OO0O0O0O000O0000O ]*(O0O0OO0OOO000O0OO .para_range [:,1 ]-O0O0OO0OOO000O0OO .para_range [:,0 ])+O0O0OO0OOO000O0OO .para_range [:,0 ]#line:1273
            OO00O00OO0OO00OO0 [OO0O0O0O000O0000O ]=O0O0OO0OOO000O0OO .score_func (OOO0000OOO000O0O0 )#line:1274
        OOOO00O000OO00O0O =np .vstack ((OO000O00O000OOO0O ,OO000OOO0O0OOO000 ))#line:1276
        OOO00O0OOOOOOOOO0 =np .hstack ((OO00O00OO0OO00OO0 ,O0O00OOOOO000O000 ))#line:1277
        OOOOOO0O00OOOOO0O =np .argpartition (np .abs (O0O0OO0OOO000O0OO .aim -OOO00O0OOOOOOOOO0 ),O0O0OO0OOO000O0OO .parent_num )[:O0O0OO0OOO000O0OO .parent_num ]#line:1279
        O0O0OO0OOO000O0OO .pool [OOO00OO00OOO0000O ]=OOOO00O000OO00O0O [OOOOOO0O00OOOOO0O ]#line:1280
        O0O0OO0OOO000O0OO .pool_score [OOO00OO00OOO0000O ]=OOO00O0OOOOOOOOO0 [OOOOOO0O00OOOOO0O ]#line:1281
    def rcGA (O00OO00O0O0O0O00O ,O00O000OO0O00O0OO ,OO0O0OO000O00O000 ,OOOO0OO00O000OO00 ,show_pool_func ='bar',seed =None ,pool_num =None ,max_gen =None ,core_num =1 ):#line:1284
        O00O000OO0O00O0OO =np .array (O00O000OO0O00O0OO )#line:1289
        if O00O000OO0O00O0OO .ndim ==1 :#line:1290
            O00O000OO0O00O0OO =O00O000OO0O00O0OO .reshape (1 ,2 )#line:1291
        O00OO00O0O0O0O00O .setting_1 (O00O000OO0O00O0OO ,OO0O0OO000O00O000 ,OOOO0OO00O000OO00 ,show_pool_func ,seed ,pool_num ,max_gen ,core_num )#line:1294
        O00OO00O0O0O0O00O .setting_2 (O00OO00O0O0O0O00O .para_num *10 ,2 ,4 )#line:1295
        O00OO00O0O0O0O00O .setting_3 (float )#line:1296
        O00OO00O0O0O0O00O .print_info ()#line:1297
        O00OO00O0O0O0O00O .sd =1.2 /math .sqrt (O00OO00O0O0O0O00O .parent_num )#line:1300
        if O00OO00O0O0O0O00O .para_num ==1 :#line:1305
            O00O0OO0OO00OOO0O =np .tile (np .array ([0.5 ]),(O00OO00O0O0O0O00O .pool_num //O00OO00O0O0O0O00O .para_num )+1 )#line:1306
        else :#line:1307
            O00O0OO0OO00OOO0O =np .tile (np .arange (0.0 ,1.000001 ,1.0 /(O00OO00O0O0O0O00O .para_num -1 )),(O00OO00O0O0O0O00O .pool_num //O00OO00O0O0O0O00O .para_num )+1 )#line:1308
        for O0O00OOO0OOOOOOO0 in range (O00OO00O0O0O0O00O .para_num ):#line:1311
            O00OO00O0O0O0O00O .pool [:,O0O00OOO0OOOOOOO0 ]=nr .permutation (O00O0OO0OO00OOO0O [:O00OO00O0O0O0O00O .pool_num ])#line:1312
        if O00OO00O0O0O0O00O .para_num ==1 :#line:1315
            O00OO00O0O0O0O00O .pool +=nr .rand (O00OO00O0O0O0O00O .pool_num ,O00OO00O0O0O0O00O .para_num )*1.0 -0.5 #line:1316
        else :#line:1317
            O00OO00O0O0O0O00O .pool +=nr .rand (O00OO00O0O0O0O00O .pool_num ,O00OO00O0O0O0O00O .para_num )*(2.0 /(3 *O00OO00O0O0O0O00O .para_num -3 ))-(1.0 /(3 *O00OO00O0O0O0O00O .para_num -3 ))#line:1318
        O00OO00O0O0O0O00O .pool =np .clip (O00OO00O0O0O0O00O .pool ,0.0 ,1.0 )#line:1321
        def OOOO0000OO000O00O (O0OO0OO0OOO0OOO00 ):#line:1324
            O00OO0OO000OO0OO0 =np .expand_dims (O00OO00O0O0O0O00O .pool ,axis =1 )-np .expand_dims (O00OO00O0O0O0O00O .pool ,axis =0 )#line:1325
            O00OO0OO000OO0OO0 =np .sqrt (np .sum (O00OO0OO000OO0OO0 **2 ,axis =-1 ))#line:1326
            O00OO0OO000OO0OO0 =np .sum (O00OO0OO000OO0OO0 ,axis =-1 )/O00OO00O0O0O0O00O .pool_num #line:1327
            return O00OO0OO000OO0OO0 #line:1328
        if O00OO00O0O0O0O00O .pool_num <=5 *10 :#line:1331
            OOOOOO0000O0O00O0 =200 #line:1332
        elif O00OO00O0O0O0O00O .pool_num <=10 *10 :#line:1333
            OOOOOO0000O0O00O0 =150 #line:1334
        elif O00OO00O0O0O0O00O .pool_num <=15 *10 :#line:1335
            OOOOOO0000O0O00O0 =70 #line:1336
        elif O00OO00O0O0O0O00O .pool_num <=20 *10 :#line:1337
            OOOOOO0000O0O00O0 =30 #line:1338
        elif O00OO00O0O0O0O00O .pool_num <=30 *10 :#line:1339
            OOOOOO0000O0O00O0 =12 #line:1340
        else :#line:1341
            OOOOOO0000O0O00O0 =0 #line:1342
        OOO00OO0O000O0OO0 =False #line:1343
        for OOO0O000O000OO000 in range (OOOOOO0000O0O00O0 ):#line:1344
            OO0000O00O0OO00O0 =OOOO0000OO000O00O (O00OO00O0O0O0O00O .pool )#line:1345
            OO0OOO000O0000OO0 =np .argmin (OO0000O00O0OO00O0 )#line:1346
            O00OO00O0O0O0O00O .pool [OO0OOO000O0000OO0 ]=nr .rand (O00OO00O0O0O0O00O .para_num )#line:1348
            OO000OO0O00OO00O0 =OOOO0000OO000O00O (O00OO00O0O0O0O00O .pool )#line:1349
            O000OO000O0OOO0O0 =0 #line:1351
            while np .sum (OO000OO0O00OO00O0 )<np .sum (OO0000O00O0OO00O0 ):#line:1352
                O00OO00O0O0O0O00O .pool [OO0OOO000O0000OO0 ]=nr .rand (O00OO00O0O0O0O00O .para_num )#line:1354
                OO000OO0O00OO00O0 =OOOO0000OO000O00O (O00OO00O0O0O0O00O .pool )#line:1355
                O000OO000O0OOO0O0 +=1 #line:1356
                if O000OO000O0OOO0O0 ==OOOOOO0000O0O00O0 :#line:1357
                    OOO00OO0O000O0OO0 =True #line:1359
                    break #line:1360
            if OOO00OO0O000O0OO0 ==True :#line:1361
                break #line:1362
        O00OO00O0O0O0O00O .score_pool_rc ()#line:1367
        O00OO00O0O0O0O00O .save_best_mean ()#line:1368
        O00OO00O0O0O0O00O .init_score_range =(np .min (O00OO00O0O0O0O00O .pool_score ),np .max (O00OO00O0O0O0O00O .pool_score ))#line:1370
        O00OO00O0O0O0O00O .init_gap_mean =deepcopy (O00OO00O0O0O0O00O .gap_mean )#line:1371
        if O00OO00O0O0O0O00O .show_pool_func ==None :pass #line:1374
        elif O00OO00O0O0O0O00O .show_pool_func =='bar':O00OO00O0O0O0O00O .show_pool_bar (0 )#line:1375
        elif O00OO00O0O0O0O00O .show_pool_func =='print':O00OO00O0O0O0O00O .show_pool_print (0 )#line:1376
        elif O00OO00O0O0O0O00O .show_pool_func =='plot':O00OO00O0O0O0O00O .show_pool_plot (0 )#line:1377
        elif callable (O00OO00O0O0O0O00O .show_pool_func ):O00OO00O0O0O0O00O .show_pool_rc (0 )#line:1378
        elif type (show_pool_func )==str :#line:1379
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1380
                if not os .path .exists (show_pool_func ):os .mkdir (show_pool_func )#line:1381
                O00OO00O0O0O0O00O .show_pool_save (0 )#line:1382
        O000OO000O0OOO0O0 =0 #line:1385
        for O00OOO0O0O0000000 in range (1 ,O00OO00O0O0O0O00O .max_n +1 ):#line:1386
            O00OO000O0OOOOOO0 =np .arange (O00OO00O0O0O0O00O .pool_num )#line:1389
            nr .shuffle (O00OO000O0OOOOOO0 )#line:1390
            O00OO000O0OOOOOO0 =O00OO000O0OOOOOO0 .reshape ((O00OO00O0O0O0O00O .pool_num //O00OO00O0O0O0O00O .parent_num ),O00OO00O0O0O0O00O .parent_num )#line:1391
            Parallel (n_jobs =O00OO00O0O0O0O00O .core_num ,require ='sharedmem')([delayed (O00OO00O0O0O0O00O .rcGA_multi )(O0OO00O00O0O0OOOO )for O0OO00O00O0O0OOOO in O00OO000O0OOOOOO0 ])#line:1394
            O00OO00O0O0O0O00O .sd =max (O00OO00O0O0O0O00O .sd *0.995 ,0.9 /math .sqrt (O00OO00O0O0O0O00O .parent_num ))#line:1424
            O000OO000O0OOO0O0 +=O00OO00O0O0O0O00O .end_check ()#line:1427
            if np .max (np .std (O00OO00O0O0O0O00O .pool ,axis =0 ))<0.03 :#line:1430
                O000OO000O0OOO0O0 +=1 #line:1431
            O00OO00O0O0O0O00O .save_best_mean ()#line:1434
            if O00OO00O0O0O0O00O .show_pool_func ==None :pass #line:1437
            elif O00OO00O0O0O0O00O .show_pool_func =='bar':O00OO00O0O0O0O00O .show_pool_bar (O00OOO0O0O0000000 *O00OO00O0O0O0O00O .pool_num )#line:1438
            elif O00OO00O0O0O0O00O .show_pool_func =='print':O00OO00O0O0O0O00O .show_pool_print (O00OOO0O0O0000000 *O00OO00O0O0O0O00O .pool_num )#line:1439
            elif O00OO00O0O0O0O00O .show_pool_func =='plot':O00OO00O0O0O0O00O .show_pool_plot (O00OOO0O0O0000000 *O00OO00O0O0O0O00O .pool_num )#line:1440
            elif callable (O00OO00O0O0O0O00O .show_pool_func ):O00OO00O0O0O0O00O .show_pool_rc (O00OOO0O0O0000000 *O00OO00O0O0O0O00O .pool_num )#line:1441
            elif type (show_pool_func )==str :#line:1442
                if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1443
                    O00OO00O0O0O0O00O .show_pool_save (O00OOO0O0O0000000 )#line:1444
            if O000OO000O0OOO0O0 >=1 :#line:1447
                break #line:1448
        OO0OO0OOOO0000O0O =O00OO00O0O0O0O00O .pool_best *(O00OO00O0O0O0O00O .para_range [:,1 ]-O00OO00O0O0O0O00O .para_range [:,0 ])+O00OO00O0O0O0O00O .para_range [:,0 ]#line:1451
        if O00OO00O0O0O0O00O .show_pool_func =='bar':print ()#line:1454
        elif type (show_pool_func )==str :#line:1455
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1456
                print ()#line:1457
        O00OO00O0O0O0O00O .print_result (OO0OO0OOOO0000O0O )#line:1460
        return OO0OO0OOOO0000O0O ,O00OO00O0O0O0O00O .score_best #line:1462
if __name__ =='__main__':#line:1472
    pass #line:1473
