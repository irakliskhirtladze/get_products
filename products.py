import requests
import json
import sys
import time
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    
    def __init__(self) -> None:
        """Initialize UI, a list to store products and connect a button with method"""
        super().__init__()
        self.ui = loadUi("ui/products.ui", self)
        
        self.ui.pushButton.clicked.connect(self.get_products)
        self.products = []

    def get_product(self, url) -> None:
        """Obtains single product from given URL"""
        response = requests.get(url)
        dictionary = response.json()
        self.products.append(dictionary) 

    def get_products(self) -> None:
        """Obtains products from given number of URLs in parallel and writes them to JSON"""
        self.num_of_products = int(self.ui.spinBox.text())
        self.urls = [f'https://dummyjson.com/products/{str(i)}' for i in range(1, self.num_of_products)]
        threads = [] # Stores threads before they are joined

        try:
            start_time = time.perf_counter()
            for url in self.urls:
                thread = threading.Thread(target=self.get_product, args=(url,))
                thread.start()
                threads.append(thread)
            
            for thread in threads:
                thread.join()
            end_time = time.perf_counter()
            
            # Write to JSON
            with open('products.json', 'w') as f:
                json.dump(self.products, f, indent=4)

            # Set labels
            self.ui.label.setStyleSheet("color:rgb(0, 255, 127)")
            self.ui.label.setText("Success")
            self.ui.label_2.setText(f"Obtained {self.num_of_products} products in {round(end_time - start_time, 3)} seconds")

        except:
            self.ui.label.setStyleSheet("color:rgb(255, 0, 0)")
            self.ui.label.setText("Failure")
            self.ui.label_2.setText(f"Could not obtain products")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("TBC Academy")
    window.setWindowIcon(QIcon("resources/tbcicon.png"))
    window.show()
    sys.exit(app.exec_())
