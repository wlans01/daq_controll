import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
import time

class DAQControl:
    def __init__(self, device_name):
        self.input_task = nidaqmx.Task()
        self.output_task = nidaqmx.Task()
        self.device_name = device_name
        self.input_channels = []
        self.output_channels = []
        self.sample_rate = None
        self.num_samples = None

    def devide_info(self):
        print('')
        print(f'연결 디바이스 이름  : {self.device_name}')
        print(f'연결된 input 채널  : {self.input_channels}')
        print(f'연결된 output 채널 : {self.output_channels}')
        print('')

    # 아날로그 input 채널 추가
    def add_input_channel(self, channel):
        self.input_channels.append(channel)
        self.input_task.ai_channels.add_ai_voltage_chan(f'{self.device_name}/{channel}')

    # 아날로그 output 채널 추가
    def add_output_channel(self, channel):
        self.output_channels.append(channel)
        self.output_task.ao_channels.add_ao_voltage_chan(f'{self.device_name}/{channel}')

    # 전압 범위 설정
    def set_voltage_range(self, channel, min_voltage, max_voltage):
        self.input_task.ai_channels[channel].ai_min = min_voltage
        self.input_task.ai_channels[channel].ai_max = max_voltage
        self.output_task.ao_channels[channel].ao_min = min_voltage
        self.output_task.ao_channels[channel].ao_max = max_voltage

    # 디지털 input 채널 추가
    def add_digital_input_channel(self, channel):
        self.input_task.di_channels.add_di_chan(channel)

    # 디지털 output 채널 추가
    def add_digital_output_channel(self, channel):
        self.output_task.do_channels.add_do_chan(channel)

    # def read_multiple_channels(self, channels):
    #     return self.input_task.read(number_of_samples_per_channel=self.num_samples, timeout=10.0, 
    #                           layout='group_by_channel',channels_to_read=channels)

    # def write_multiple_channels(self, data, channels):
    #     self.output_task.write(data, auto_start=True, layout='group_by_channel',channels_to_write=channels)

    def set_sample_rate(self, rate, samples):
        self.sample_rate = rate
        self.num_samples = samples
        self.input_task.timing.cfg_samp_clk_timing(rate, sample_mode='finite', samps_per_chan=samples)

    def set_trigger(self, source, edge):
        self.input_task.triggers.start_trigger.cfg_dig_edge_start_trig(source, edge)

    def self_diagnostics(self):
        '''
    '''
        # try:
        #     self.output_task.self_test()
        #     self.input_task.self_test()
        #     print("Device self-test passed.")
        # except nidaqmx.errors.DaqError as e:
        #     print("Device self-test failed: ", e)

    # read 할경우 자동으로 시작 필요 x
    def start(self):
        self.input_task.start()
        self.output_task.start()

    # 필요 x
    def stop(self):
        self.input_task.stop()

    def read(self):
        return self.input_task.read()

    def write(self, data):
        self.output_task.write(data)

    def save_data(self, filename):
        np.savetxt(filename, self.data)
        
    def plot_data(self):
        plt.plot(self.data)
        plt.show()

    # 유지 보수 해야함
    def start_output_streaming(self):
        self.input_task.start()
        self.output_data = np.linspace(0, 1, 100)
        for i in range(len(self.output_data)):
            self.line.set_ydata(self.output_data)
            self.fig.canvas.draw()
            self.write(self.output_data[i])
            time.sleep(0.1)
        self.input_task.stop()
        self.input_task.close()

    # 실행이 끝나면 필수로 닫아야 오류가 안생김
    def close(self):
        self.input_task.close()
        self.output_task.close()


# GVS002 테스트 함수 ㄹ 모양으로 스캔
def test(daq : DAQControl):
    # daq.self_diagnostics()
    daq.add_input_channel('ai0')
    daq.add_input_channel('ai1')
    daq.add_output_channel('ao0')
    daq.add_output_channel('ao1')
    daq.devide_info()
    # daq.write([0,0])
    # data = daq.read()
    # print(data)

    # 레이저 스캔경로 ㄹ 모양
    # 스캔범위와 스캔 간격 0.8v당 1도
    iteration = np.arange(-10,10,0.8)

    # 스캔위치가 왼쪽인지 오른쪽인지 확인
    _isLeft = True

    # 지연시간
    latency = 0.1

    # y 축
    for i in iteration[::-1]:
        i = round(i,3)
        if _isLeft:
            # x 축 왼쪽에서 오른쪽으로
            for j in iteration:
                j = round(j,3)
                daq.write([j,i])
                data = daq.read()
                print(np.round(data,3))
                time.sleep(latency)
                _isLeft = False
                
        else:
            # x 축 오른쪽에서 왼쪽으로
            for j in iteration[::-1]:
                j = round(j,3)
                daq.write([j,i])
                data = daq.read()
                print(np.round(data,3))
                time.sleep(latency)
                _isLeft = True

    daq.close()

if __name__ == '__main__':
    
    daq = DAQControl('Dev1')
    daq.self_diagnostics()
    daq.add_input_channel('ai0')
    daq.add_input_channel('ai1')
    daq.add_output_channel('ao0')
    daq.add_output_channel('ao1')
    
    daq.devide_info()
    daq.write([0,0])
    data = daq.read()
    print(data)
    daq.close()

    
    # test(daq)