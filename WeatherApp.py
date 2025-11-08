import sys
import requests
from PyQt5.QtWidgets import QApplication,QLineEdit,QWidget,QLabel,QVBoxLayout,QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class Weather_App(QWidget):
    def __init__(self):
        super().__init__()

        self.city_label = QLabel("Enter the city name",self)
        self.city_input = QLineEdit(self)
        self.get_weather_city = QPushButton("Get Weather",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.decription_label = QLabel(self)
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Weather APP")
        self.setWindowIcon(QIcon("OIP.jpg"))
        # Design User Interface
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_city)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.decription_label)
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.decription_label.setAlignment(Qt.AlignCenter)

        # Design font 

        # First: set object
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_city.setObjectName("get_weather_city")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.decription_label.setObjectName("decription_label")

        self.setStyleSheet("""
                            QLabel,QPushButton{
                                font-family: calibri;
                           }
                            QPushButton#get_weather_city{
                                font-size: 50px;
                                font-weight: bold;
                           }
                            QLineEdit#city_input{
                                font-size: 60px;
                           }
                            QLabel#city_label{
                                font-size: 60px;
                                font-style: italic;
                           }
                            QLabel#temperature_label{
                                font-size: 95px;
                           }
                            QLabel#emoji_label{
                                font-size: 170px;
                                font-family: Segoe UI emoji;
                           }
                            QLabel#decription_label{
                                font-size: 75px;
                                font-weight: bold;
                           }
                           """)
        self.get_weather_city.clicked.connect(self.get_weather_state)

    # Logic handling that clicked to get the weather
    def get_weather_state(self):
        
        api_key = "eb7316306822076af937877064cea128"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status() # Replace for if below
            
            data = response.json()
            self.Display_Weather(data)

        # Error with HTTP
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.Display_Error("Bad Request:\nPlease check your input")
                case 401:
                    self.Display_Error("Unauthorized:\nInvalid API Key")
                case 403:
                    self.Display_Error("Forbidden:\nAccess is denied")
                case 404:
                    self.Display_Error("Not Found:\nCity not found")
                case 500:
                    self.Display_Error("Internal Sever Error:\nPlease try again later")
                case 502:
                    self.Display_Error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.Display_Error("Service Unavailable:\nServer is down")
                case 504:
                    self.Display_Error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.Display_Error(f"HTTP error occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.Display_Error("Connection Error:\n Please check your internet connection")
        
        except requests.exceptions.Timeout:
            self.Display_Error("Timeout Error:\nThe request timed out")

        except requests.exceptions.TooManyRedirects:
            self.Display_Error("Too many Redirects:\nCheck the url")

        except requests.exceptions.RequestException as req_error: 
            self.Display_Error(f"Request Error:\n{req_error}")
            
    # if data doesn't exist (equal to 404 or ...)
    def Display_Error(self,message):
        self.temperature_label.setStyleSheet("font-size: 40px;")
        self.temperature_label.setText(message)
    
    # if data exists (equal to 200)
    def Display_Weather(self,data):
        # Temperature
        self.temperature_label.setStyleSheet("font-size: 95px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67

        # Weather Decription:
        weather_decription = data["weather"][0]["description"]

        # Weather Icon
        weather_id = data["weather"][0]["id"]


        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        self.decription_label.setText(weather_decription.capitalize())

        self.emoji_label.setText(self.get_weather_emoji(weather_id))

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232: # Thunderstorm
            return "⛈️"
        elif 300 <= weather_id <= 321: # Small Rain
            return "🌦️"
        elif 500 <= weather_id <= 531: # Rain
            return "🌧️"
        elif 600 <= weather_id <= 622: # Snow
            return "🌨️"
        elif 701 <= weather_id <= 741: # Fog
            return "🌫️"
        elif weather_id == 762: # Volcano
            return "🌋"
        elif weather_id == 771: # Super Wind
            return "💨"
        elif weather_id == 781: # Tonardo
            return "🌪️"
        elif weather_id == 800: # Sun
            return "🌤️"
        elif 801 <= weather_id <= 804: # Cloud
            return "☁️"
        else:
            return ""
def main():
    app = QApplication(sys.argv)
    weather_app = Weather_App()
    weather_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()