from rest_framework.views import APIView
from rest_framework.response import Response
from smbus2 import SMBus
from .mlx90614 import MLX90614  # Make sure the import path is correct
from .heartrate_monitor import start_sensor, stop_sensor, results  # Adjust import path
import threading
import time


class TemperatureAPIView(APIView):
    """
    API view to fetch sensor data.
    """

    def get(self, request, format=None):
        bus = SMBus(1)
        sensor = MLX90614(bus, address=0x5A)
        
        try:
            object_temperature = sensor.get_object_1()
            ambient_temperature = sensor.get_ambient()
            bus.close()
            
            data = {
                'object_temperature': round(object_temperature, 2),
                'ambient_temperature': round(ambient_temperature, 2)
            }
            return Response(data)
        
        except Exception as e:
            bus.close()
            return Response({'error': str(e)}, status=500)
        
        
class HeartRateAPIView(APIView):
    def get(self, request):
        duration = int(request.GET.get('duration', 10))  # Use duration from request

        start_sensor()  # Start the heart rate sensor

        # Let the sensor collect data for the specified duration
        time.sleep(duration)

        stop_sensor()  # Stop the sensor and wait for the thread to finish
        print(results)  # Access results after the sensor operation

        return Response(results)