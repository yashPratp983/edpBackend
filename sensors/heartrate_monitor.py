from .max30102 import MAX30102
from . import hrcalc
import threading
import time
import numpy as np

# Global variables to manage state
LOOP_TIME = 0.01
results = {"bpm": None, "spo2": None}
stopped = False
_thread = None

def run_sensor():
    global stopped, results
    sensor = MAX30102()
    ir_data = []
    red_data = []
    bpms = []
    spo2Data = 0
    bpmData = 0
    bpmCount = 0
    spo2Count = 0
    
    while not stopped:
        num_bytes = sensor.get_data_present()
        while num_bytes > 0:
            red, ir = sensor.read_fifo()
            num_bytes -= 1
            ir_data.append(ir)
            red_data.append(red)

        if len(ir_data) > 100:
            ir_data = ir_data[-100:]
            red_data = red_data[-100:]

        if len(ir_data) == 100:
            bpm, valid_bpm, spo2, valid_spo2 = hrcalc.calc_hr_and_spo2(ir_data, red_data)
            if valid_bpm and (60 < bpm < 120):
                bpmData += bpm
                bpmCount += 1
            if valid_spo2 and (80 <= spo2 <= 100):
                spo2Data += spo2
                spo2Count += 1

        time.sleep(LOOP_TIME)

    sensor.shutdown()
    if bpmCount > 0 and spo2Count > 0:
        results["bpm"] = round(bpmData / bpmCount,2)
        results["spo2"] = round(spo2Data / spo2Count,2)
    else:
        results["message"] = "Data inaccurate"
    print(results)
    return results

def start_sensor():
    global stopped, _thread
    stopped = False
    _thread = threading.Thread(target=run_sensor)
    _thread.start()

def stop_sensor():
    global stopped
    stopped = True
    if _thread and _thread.is_alive():
        _thread.join()