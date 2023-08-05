import re

def key_words_parser(this_, rule, words, w_tuples, text):
    
    if '投资' in text and '策略' in text:
        rule['field'] = 'tyzx'
        rule['type'] = '投资策略'
    elif '投资' in text and '组合' in text:
        rule['field'] = 'tyzx'
        rule['type'] = '投资策略'
    elif '收益' in text and '风险' in text and '预估' in text:
        rule['field'] = 'tyzx'
        rule['type'] = '投资策略'
    elif '持有' in text and ('多久' in text or '时间' in text):
        rule['field'] = 'tyzx'
        rule['type'] = '持有时间'
    elif '赎回' in text:
        rule['field'] = 'tyzx'
        rule['type'] = '持有时间'
    elif '费用' in text or '收费' in text or '交易费' in text:
        rule['field'] = 'tyzx'
        rule['type'] = '收费方式'
    elif '交易' in text:
        if '记录' in text:
            rule['field'] = 'cczx'
            rule['type'] = 'trading_history'
        elif '如何' in text:
            rule['field'] = 'tyzx'
            rule['type'] = '收费方式'
    elif '年化' in text and '收益' in text:
        arr = re.findall(r"\d+\.?\d*", text)
        if len(arr) > 0:
            ret = float(arr[0])
            if ret > 1:
                ret = ret / 100
            rule['field'] = 'zhtj'
            rule['type'] = 'ret'
            rule['ret'] = ret
    elif '高' in text and '收益' in text:
        rule['field'] = 'zhtj'
        rule['type'] = 'ret'
        rule['ret'] = 'high'
    elif '回撤' in text:
        arr = re.findall(r"\d+\.?\d*", text)
        if len(arr) > 0:
            mdd = float(arr[0])
            if mdd > 1:
                mdd = mdd / 100
            rule['field'] = 'zhtj'
            rule['type'] = 'mdd'
            rule['mdd'] = mdd
    elif '低' in text and '风险' in text:
        rule['field'] = 'zhtj'
        rule['type'] = 'mdd'
        rule['mdd'] = 'low'
    elif '股票' in text:
        if '为何' in text or '为什么' in text:
            if '收益' in text and ('不明显' in text or '下降' in text):
                rule['field'] = 'yjfx'
                rule['baseline'] = 'stock'
            else:
                rule['field'] = 'chfx'
                rule['type'] = 'asset'
                rule['asset'] = 'stock'
        else:
            rule['field'] = 'hqzx'
            rule['type'] = 'asset'
            rule['asset'] = 'stock'
    elif '信用债' in text:
        if '为何' in text or '为什么' in text:
            rule['field'] = 'chfx'
            rule['type'] = 'asset'
            rule['asset'] = 'credit_debt'
        else:
            rule['field'] = 'hqzx'
            rule['type'] = 'asset'
            rule['asset'] = 'credit_debt'
    elif 'type' in rule.keys() and rule['type'] == 'fund':
        if '为何' in text or '为什么' in text:
            rule['field'] = 'chfx'
        else:
            rule['field'] = 'hqzx'
    elif '组合' and '收益' in text:
        rule['field'] = 'cczx'
        rule['type'] = 'nav'
    elif '组合' in text and '板' in text:
        rule['field'] = 'cczx'
        rule['type'] = 'industry'
        for tp in w_tuples:
            if tp[1] == 'n' and tp[0] in this_.stock_factor_dict.keys():
                rule['industry'] = this_.stock_factor_dict[tp[0]]
    elif '大类' in text and ('配比' in text or '表现' in text):
        if '为何' in text or '为什么' in text:
            rule['field'] = 'chfx'
            rule['type'] = 'asset'
            rule['asset'] = 'all'
        else:
            rule['field'] = 'cczx'
            rule['type'] = 'asset'
    elif '持仓' in text:
        rule['field'] = 'cczx'
        rule['type'] = 'fund'
    elif '基金' in text:
        if '怎么' in text or '为什么' in text or '为何' in text:
            rule['field'] = 'chfx'
            rule['type'] = 'fund'
            rule['fund'] = 'all'
        else:
            rule['field'] = 'cczx'
            rule['type'] = 'fund'
    elif '业绩' in text:
        rule['field'] = 'cczx'
        rule['type'] = 'backtest'
    elif '国债' in text:
        rule['field'] = 'chfx'
        rule['type'] = 'asset'
        rule['asset'] = 'national_debt'
    elif '净值' in text and '下降' in text:
        rule['field'] = 'yjfx'
    elif '组合' in text and '亏损' in text:
        rule['field'] = 'yjfx'
    
    
    
        