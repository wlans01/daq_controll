import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
import time

class DAQControl:
    def __init__(self, device_name):
        self.task = nidaqmx.Task()
        self.device_name = device_name
        self.input_channels = []
        self.output_channels = []
        self.sample_rate = None
        self.num_samples = None

    def add_input_channel(self, channel):
        self.input_channels.append(channel)
        self.task.ai_channels.add_ai_voltage_chan(channel)

    def add_output_channel(self, channel):
        self.output_channels.append(channel)
        self.task.ao_channels.add_ao_voltage_chan(channel)

    def set_voltage_range(self, channel, min_voltage, max_voltage):
        self.task.ai_channels[channel].ai_min = min_voltage
        self.task.ai_channels[channel].ai_max = max_voltage
        self.task.ao_channels[channel].ao_min = min_voltage
        self.task.ao_channels[channel].ao_max = max_voltage

    def add_digital_input_channel(self, channel):
        self.task.di_channels.add_di_chan(channel)

    def add_digital_output_channel(self, channel):
        self.task.do_channels.add_do_chan(channel)

    def read_multiple_channels(self, channels):
        return self.task.read(number_of_samples_per_channel=self.num_samples, timeout=10.0, 
                              layout='group_by_channel',channels_to_read=channels)

    def write_multiple_channels(self, data, channels):
        self.task.write(data, auto_start=True, layout='group_by_channel',channels_to_write=channels)

    def set_sample_rate(self, rate, samples):
        self.sample_rate = rate
        self.num_samples = samples
        self.task.timing.cfg_samp_clk_timing(rate, sample_mode='finite', samps_per_chan=samples)

    def set_trigger(self, source, edge):
        self.task.triggers.start_trigger.cfg_dig_edge_start_trig(source, edge)

    def self_diagnostics(self):
        try:
            self.task_output.self_test()
            self.task_input.self_test()
            print("Device self-test passed.")
        except nidaqmx.errors.DaqError as e:
            print("Device self-test failed: ", e)

    def start(self):
        self.task.start()

    def stop(self):
        self.task.stop()

    def read(self):
        return self.task.read()

    def write(self, data):
        self.task.write(data)

    def save_data(self, filename):
        np.savetxt(filename, self.data)
        
    def plot_data(self):
        plt.plot(self.data)
        plt.show()

    def start_output_streaming(self):
        self.task.start()
        self.output_data = np.linspace(0, 1, 100)
        for i in range(len(self.output_data)):
            self.line.set_ydata(self.output_data)
            self.fig.canvas.draw()
            self.write(self.output_data[i])
            time.sleep(0.1)
        self.task.stop()
        self.task.close()


if __name__ == '__main__':
    daq = DAQControl('Dev1')
    daq.add_input_channel('Dev1/ai0')
    daq.add_output_channel('Dev1/ao0')