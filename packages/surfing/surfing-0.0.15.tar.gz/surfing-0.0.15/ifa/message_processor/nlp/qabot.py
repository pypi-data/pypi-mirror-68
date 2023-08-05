import pandas as pd
import numpy as np
from ...util.config import Configurator
from aip import AipNlp
from .rules import key_words_parser
import pkuseg
import json
import os
import pprint

class QaBot():
    def __init__(self):
        app_id = Configurator().config['bot']['baidu_aip']['app_id']
        api_key = Configurator().config['bot']['baidu_aip']['api_key']
        secret_key = Configurator().config['bot']['baidu_aip']['secret_key']
        self.baidu_client = AipNlp(app_id, api_key, secret_key)

        data_path = Configurator().config['bot']['data_path']
        
        self.sent_dict = {}
        sents = pd.read_csv(os.path.join(data_path, 'sentence.csv'))
        for sentence, cur_type in sents.values:
            self.sent_dict[sentence] = {}
            # self.sent_dict[sentence]['field'] = cur_field
            self.sent_dict[sentence]['type'] = cur_type

        self.greet_dict = {}
        greet = pd.read_csv(os.path.join(data_path, 'greeting.csv'))
        for keyw, cur_type in greet.values:
            self.greet_dict[keyw] = cur_type

        self.stock_factor_dict = {}
        stock_factor = pd.read_csv(os.path.join(data_path, 'stock_factors.csv'))
        for name, cur_type in stock_factor.values:
            self.stock_factor_dict[name] = cur_type

        self.seg = pkuseg.pkuseg(model_name = 'default', user_dict = os.path.join(data_path, 'pkuseg_symbols.txt'),
            postag = True)

        with open(os.path.join(data_path, 'fund_symbol.json'), 'r', encoding='utf-8') as f:
            self.fund_info = json.load(f)
        
        with open(os.path.join(data_path, 'fund_ridx.json'), 'r', encoding='utf-8') as f2:
            self.reverse_index = json.load(f2)
    
    def text_parser(self, text):
        emotion = self.baidu_client.sentimentClassify(text)
        rule = {
            'type': '',
            'emotion': emotion['items']
        }

        # check text
        if text in self.sent_dict.keys():
            rule['type'] = self.sent_dict[text]['type']
            # rule['field'] = self.sent_dict[text]['field']
            return rule

        w_tuples = self.seg.cut(text)
        # print(w_tuples)
        words = [x[0] for x in w_tuples]
        
        for tp in w_tuples:
            if tp[1] == 'n' and tp[0] in self.fund_info.keys():
                rule['type'] = 'fund'
                rule['fund'] = self.fund_info[tp[0]]
                rule['query'] = 'acc'
                return rule
        
        fm = self.fuzzy_matching(w_tuples)
        if fm is not None:
            rule['type'] = 'fund'
            rule['fund'] = fm
            rule['query'] = 'sim'
            return rule
        
        # key words parser
        key_words_parser(self, rule, words, w_tuples, text)
        if 'field' in rule.keys():
            return rule

        for tp in w_tuples:
            if tp[0] in self.greet_dict.keys():
                rule['field'] = 'hx'
                return rule
        
        return rule
    
    def fuzzy_matching(self, w_tuples, threshold=3):
        phase = []
        index = 0
        length = len(w_tuples)
        while index < length:
            cur_idx = index
            tmp = []
            while 'n' in w_tuples[cur_idx][1] or 'v' in w_tuples[cur_idx][1] or 'j' in w_tuples[cur_idx][1] or 'a' in w_tuples[cur_idx][1]:
                tmp.append(w_tuples[cur_idx][0])
                cur_idx += 1
                if cur_idx >= length:
                    break

            if len(tmp) > 0:
                phase.append(tmp)
            index = cur_idx
            index += 1

        new_phase = []
        for key_ws in phase:
            length = len(key_ws)
            if length > 1:
                for i in range(1, length):
                    new_phase.append(key_ws[i:])
                for i in range(length, 0, -1):
                    new_phase.append(key_ws[:i])

        phase = phase + new_phase
        final_phase = [x for x in phase if len(x) > 1]

        records = []
        for key_ws in final_phase:
            key_len = len(key_ws)
            
            try:
                cur_dict = self.reverse_index[key_ws[0]].copy()
            except:
                continue
            
            for i in range(1, key_len):
                try:
                    tmp_dict = self.reverse_index[key_ws[i]].copy()
                except:
                    break
                
                removed_key = []
                for k in cur_dict.keys():
                    if k not in tmp_dict.keys():
                        removed_key.append(k)
                for k in removed_key:      
                    del cur_dict[k]
                        
                if len(cur_dict.keys()) <= 0:
                    break
            
            if len(cur_dict.keys()) <= 0 or i <= 1:
                continue
            
            records.append((cur_dict, len(cur_dict.keys())))
        
        if len(records) > 0:
            sr_records = sorted(records, key=lambda x: x[1])
            opt = sr_records[0][0]
            opt_num = sr_records[0][1]
            if opt_num > threshold:
                return None
            else:
                return opt
        else:
            return None


if __name__ == '__main__':
    qr = QaBot()
    while True:
        data = input('Q: ')
        rule = qr.text_parser(data)
        pprint.pprint(rule)
    