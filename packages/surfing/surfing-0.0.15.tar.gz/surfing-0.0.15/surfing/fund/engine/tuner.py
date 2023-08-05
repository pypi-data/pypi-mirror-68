import time
import datetime
import pandas as pd
from pprint import pprint 
from .backtest import FundBacktestEngine
from .trader import AssetTrader
from ...data.manager.manager_fund import FundDataManager
from ...data.struct import AssetTrade, FundTrade, FundScoreParam, TAAParam, TaaTunerParam, AssetTradeParam, AssetWeight


class TaaTuner:

    BACKTEST_NUM = 3
    INDEX_WEIGHT = 0.1
    CASH_WEIGHT = 0.9
    TAA_LOW_TYPE = 'taa_low_only'
    TAA_UP_TYPE = 'taa_up_only'

    def __init__(self, start_time:str='20050101', end_time:str='20200501'):
        self.dm = FundDataManager(start_time=start_time, end_time=end_time)
        self.start_date = datetime.datetime.strptime(start_time, '%Y%m%d').date()
        self.end_date = datetime.datetime.strptime(end_time, '%Y%m%d').date()
        self.ap = AssetTradeParam()
        self.at = AssetTrader(self.ap)

    def init(self, taa_tuner:TaaTunerParam ):
        self.dm.init(score_pre_calc=False)
        self.taa_tuner = taa_tuner
        self.saa = AssetWeight(**{'cash':self.CASH_WEIGHT, self.taa_tuner.index_id:self.INDEX_WEIGHT})
        self.taa_type = self.TAA_LOW_TYPE if self.taa_tuner.IsTaaLowOnly else self.TAA_UP_TYPE
        self.bk_each_time = None

    def grid_search(self):
        self.run_saa()
        self.test_bk_time()
        self.search_bk()
        self.first_round_analysis()
        self.search_bk_2()
        self.second_round_analysis()

    def run_saa(self):
        saa_bk = FundBacktestEngine(data_manager=self.dm, trader=self.at, taa_params=None)
        saa_bk.init()
        saa_bk.run(saa=self.saa, start_date=self.start_date, end_date=self.end_date)
        self.saa_result = saa_bk._report_helper.get_asset_stat()
        
    def search_bk(self, is_test:bool=False, bk_list=None):
        if bk_list is None:
            if is_test:
                taa_param_list = self.taa_tuner.param_list[:self.BACKTEST_NUM]
            else:
                taa_param_list = self.taa_tuner.param_list
        else:
            taa_param_list = bk_list

        self.result = []
        c = 1
        bk_num = len(taa_param_list)
        if self.bk_each_time is not None:
            cost_min = len(taa_param_list) * self.bk_each_time / 60
            print(f'totally bk {bk_num} tasks index_id: {self.taa_tuner.index_id} may cost {cost_min} mins')
        else:
            print(f'totally bk {bk_num} tasks index_id: {self.taa_tuner.index_id}')
        for taa_i in taa_param_list:
            t_0 = time.time()
            taa_bk_i = FundBacktestEngine(data_manager=self.dm, trader=self.at, taa_params=taa_i)
            taa_bk_i.init()
            taa_bk_i.run(saa=self.saa, start_date=self.start_date, end_date=self.end_date)
            taa_result = taa_bk_i._report_helper.get_asset_stat()
            dic = taa_i.__dict__
            dic['taa_ret'] = taa_result['annual_ret']
            self.result.append(dic)
            t_1 = time.time()
            print(f'finish task {c}, cost {t_1 - t_0} sec')
            c += 1
        self.result = pd.DataFrame(self.result)
        self.result['saa_annual_ret'] = self.saa_result['annual_ret']
        self.result['taa_saa_annual_ret'] = self.result['taa_ret'] - self.saa_result['annual_ret']
        self.result['taa_type'] = self.taa_type
        self.result = self.result.sort_values('taa_saa_annual_ret', ascending=False)
        print()

    def test_bk_time(self):
        print()
        print('test backtest')
        t_0 = time.time()
        self.search_bk(is_test=True)
        t_1 = time.time()
        cost_time = t_1 - t_0
        self.bk_each_time = cost_time / self.BACKTEST_NUM
        print(f'bk {self.BACKTEST_NUM} times total cost {cost_time} sec, each bk {self.bk_each_time} sec')
        t_1 = time.time()
        task_num = len(self.taa_tuner.param_list)
        print(f'first round backtest may cost {task_num * self.bk_each_time / 60} mins')
        print()

    def first_round_analysis(self): 
        self.result.to_csv(f'{self.taa_tuner.index_id}_{self.taa_type}_round1.csv')
        self.first_round_result = self.result.iloc[0]
        print('first round filter result')
        pprint(self.first_round_result)
        print()

    def search_bk_2(self):
        d = self.first_round_result 
       
        self.bk_params = []
        if d.taa_type == self.TAA_UP_TYPE:
            LowThreshold = d.LowThreshold
            LowStop = d.LowStop
            LowPlus = d.LowPlus
            for HighMinus in [_ for _ in range( int(d.HighMinus * 100) - 1,int(d.HighMinus * 100) + 2, 1)]:
                for HighStop in [_ for _ in range( int(d.HighStop * 100) - 2,int(d.HighStop * 100) + 3, 1)]:
                    for HighThreshold  in [_ for _ in range( int(d.HighThreshold * 100) - 2,int(d.HighThreshold * 100) + 3, 1)]:
                        t = TAAParam()
                        t.HighThreshold = HighThreshold / 100
                        t.HighStop = HighStop / 100
                        t.HighMinus = HighMinus / 100
                        t.LowStop = LowStop 
                        t.LowThreshold = LowThreshold 
                        t.LowPlus = LowPlus 
                        t.TuneCash = True
                        self.bk_params.append(t)
        else:
            HighThreshold = d.HighThreshold
            HighStop = d.HighStop
            HighMinus = d.HighMinus
            for LowPlus in [_ for _ in range( int(d.LowPlus * 100) - 1,int(d.LowPlus * 100) + 2, 1)]:
                for LowStop in [_ for _ in range( int(d.LowStop * 100) - 2,int(d.LowStop * 100) + 3, 1)]:
                    for LowThreshold in [_ for _ in range( int(d.LowThreshold * 100) - 2,int(d.LowThreshold * 100) + 3, 1)]:
                        t = TAAParam()
                        t.HighThreshold = HighThreshold
                        t.HighStop = HighStop
                        t.HighMinus = HighMinus
                        t.LowStop = LowStop / 100
                        t.LowThreshold = LowThreshold / 100
                        t.LowPlus = LowPlus / 100
                        t.TuneCash = True
                        self.bk_params.append(t)
        self.search_bk(is_test=False, bk_list=self.bk_params)
        
    def second_round_analysis(self):
        self.result.to_csv(f'{self.taa_tuner.index_id}_{self.taa_type}_round2.csv')
        self.second_round_result = self.result.iloc[0]
        print('second round filter result')
        pprint(self.second_round_result)


if __name__ == "__main__":
    
    tt = TaaTunerParam()
    tt.IsTaaUpOnly = True
    tt.index_id = 'hs300'

    LowStop = -100
    LowThreshold = -100
    LowPlus = 0

    tt.param_list = []
    for HighThreshold in range(80, 97, 2):
        for HighStop in range(50, 71, 2):
            for HighMinus in [3 , 5, 7]:
                t = TAAParam()
                t.HighThreshold = HighThreshold / 100
                t.HighStop = HighStop / 100
                t.HighMinus = HighMinus / 100
                t.LowStop = LowStop / 100
                t.LowThreshold = LowThreshold / 100
                t.LowPlus = LowPlus / 100
                t.TuneCash = True
                tt.param_list.append(t)

    bk = TaaTuner()
    bk.init(tt)   
    bk.grid_search()