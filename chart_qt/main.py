import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib import gridspec
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from get_price_data import *
from get_per_data import *
from get_krx_code import *


class Charter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.height = 30

        self.initRadioBtn()
        self.initLineEditBtn()
        self.initBtn()

        self.timeline = QLabel("", self)
        self.timeline.setFixedHeight(self.height)

        top_layout = QVBoxLayout()
        top_layout.addLayout(self.country_layout)
        top_layout.addLayout(self.ticker_layout)
        top_layout.addLayout(self.year_layout)
        top_layout.addLayout(self.chart_type_layout)
        top_layout.addLayout(self.btn_layout)
        top_layout.addWidget(self.timeline)

        # 그래프 레이아웃 배치
        self.figg = plt.Figure()
        self.canvas = FigureCanvas(self.figg)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.canvas)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addLayout(bottom_layout)

        self.setWindowTitle("Charter")
        path = os.path.dirname(os.path.abspath(__file__))
        self.setWindowIcon(QIcon(path + "/chart.png"))
        self.setGeometry(100, 100, 900, 900)
        self.setLayout(layout)
        self.show()

    def initBtn(self):
        # 종료 버튼
        exit_btn = QPushButton("Quit", self)
        exit_btn.setFixedHeight(self.height)
        exit_btn.clicked.connect(QCoreApplication.instance().quit)

        # 차트 저장 버튼
        save_btn = QPushButton("Save", self)
        save_btn.setFixedHeight(self.height)
        save_btn.clicked.connect(self.save_btn_clicked)

        # 차트 생성 버튼
        generate_btn = QPushButton("Generate", self)
        generate_btn.setFixedHeight(self.height)
        generate_btn.clicked.connect(self.generate_btn_clicked)

        # btn_layout: 차트 생성, 저장, 종료 버튼 layout
        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(generate_btn)
        self.btn_layout.addWidget(save_btn)
        self.btn_layout.addWidget(exit_btn)

    def initRadioBtn(self):
        # 국가 선택 라벨 및 라디오 버튼
        country_label = QLabel("국가 구분:", self)
        country_label.setFixedSize(150, self.height)
        self.rb_america = QRadioButton("미국 주식", self)
        self.rb_america.setChecked(True)
        self.rb_korea = QRadioButton("한국 주식", self)

        rb_country_group = QButtonGroup(self)
        rb_country_group.addButton(self.rb_america)
        rb_country_group.addButton(self.rb_korea)

        self.country_layout = QHBoxLayout()
        self.country_layout.addWidget(country_label)
        self.country_layout.addWidget(self.rb_america)
        self.country_layout.addWidget(self.rb_korea)

        # 차트 종류 선택 라벨 및 라디오 버튼
        chart_type = QLabel("차트 구분:")
        chart_type.setFixedSize(150, self.height)
        self.rb_normal = QRadioButton("기본 차트", self)
        self.rb_normal.setChecked(True)
        self.rb_per_band = QRadioButton("PER BAND 차트", self)

        rb_chart = QButtonGroup(self)
        rb_chart.addButton(self.rb_normal)
        rb_chart.addButton(self.rb_per_band)

        self.chart_type_layout = QHBoxLayout()
        self.chart_type_layout.addWidget(chart_type)
        self.chart_type_layout.addWidget(self.rb_normal)
        self.chart_type_layout.addWidget(self.rb_per_band)

    def initLineEditBtn(self):
        # 티커 입력 라벨 및 버튼
        ticker_label = QLabel("Ticker:", self)
        ticker_label.setFixedSize(75, self.height)

        self.ticker_label2 = QLabel("", self)
        self.ticker_label2.setFixedSize(69, self.height)
        self.ticker_label2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.ticker_input = QLineEdit(self)
        self.ticker_text = ""
        self.ticker_input.textChanged[str].connect(self.ticker_changed)
        self.ticker_input.returnPressed.connect(self.generate_btn_clicked)
        self.ticker_input.setFocus()

        self.ticker_layout = QHBoxLayout()
        self.ticker_layout.addWidget(ticker_label)
        self.ticker_layout.addWidget(self.ticker_label2)
        self.ticker_layout.addWidget(self.ticker_input)

        # 목표 기간 입력 라벨 및 버튼
        year_label = QLabel("Target Year:", self)
        year_label.setFixedSize(150, self.height)

        self.year_input = QLineEdit("5", self)
        self.year_text = 5
        self.year_input.textChanged[str].connect(self.year_changed)
        self.year_input.returnPressed.connect(self.generate_btn_clicked)

        self.year_layout = QHBoxLayout()
        self.year_layout.addWidget(year_label)
        self.year_layout.addWidget(self.year_input)

    def ticker_changed(self, text):
        self.ticker_text = text

    def year_changed(self, text):
        try:
            self.year_text = int(text)
        except:
            self.year_text = 5

    def generate_btn_clicked(self):
        try:
            self.chart_process()
            self.error = 0
        except KeyError:
            print(KeyError)
            self.error = 1
        if self.error == 0:
            self.timeline.setText("조회 성공")
            self.ticker_label2.setText(f"{self.ticker_text}    ")
            self.ticker_input.setText("")
        else:
            self.timeline.setText("조회 실패. 입력 정보를 확인하세요.")
            self.ticker_input.setText("")

    def chart_process(self):
        if self.rb_america.isChecked():
            country = 1
        else:
            country = 2
        if self.rb_normal.isChecked():
            self.type = 1
        else:
            self.type = 2
        if country == 1:
            self.ticker_text = self.ticker_text.upper()
            ticker = self.ticker_text
            self.ticker_name = ticker
        elif country == 2:
            stock_name = self.ticker_text
            ticker = get_code(stock_name)
            self.ticker_name = ticker
            self.type = 1
        target = self.year_text
        df = get_base_data(ticker, target)
        if self.type == 2:
            eps_df = get_per_band(ticker)
        else:
            eps_df = None
        self.chart(ticker, df, eps_df, self.type)

    def chart(self, ticker, df, eps_df, type):
        self.figg.clear()

        spec = gridspec.GridSpec(ncols=1, nrows=2, height_ratios=[3, 1])
        ax1 = self.figg.add_subplot(spec[0])
        ax2 = self.figg.add_subplot(spec[1])
        self.time_now = datetime.datetime.now().strftime("%Y-%m-%d")
        self.figg.suptitle(f"{self.time_now}")
        df.plot(kind="line", x="Date", y=["Close", "52High"], ax=ax1)
        df.plot(kind="line", x="Date", y="MDD", ax=ax2)
        if type == 2:
            columns = list(eps_df.columns)[3:]
            colors = [
                "#FF0000",
                "#BDFF95",
                "#95FFE2",
                "#95CFFF",
                "#959BFF",
                "#CD95FF",
                "#FF95E7",
                "#95FFBD",
            ]
            eps_df.plot(kind="line", x="name", y=columns, ax=ax1, color=colors, linewidth=1)
            eps_df.plot(kind="line", x="name", y=["zero"], ax=ax2, linewidth=0)
        ax1.grid(True, axis="y")
        ax1.set_xlabel("")
        ax1.set_ylabel("Price ($)")
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.spines["left"].set_visible(False)
        ax2.grid(True, axis="y")
        ax2.set_ylabel("MDD (%)")
        ax2.spines["top"].set_visible(False)
        ax2.spines["bottom"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.spines["left"].set_visible(False)
        ax2.get_xaxis().set_visible(False)
        ax2.get_legend().remove()
        self.canvas.draw()

    def save_btn_clicked(self):
        if self.error:
            self.timeline.setText("저장 실패")
        else:
            ticker = self.ticker_name
            if self.type == 1:
                self.figg.savefig(f"{self.time_now}-{ticker}.png", bbox_inches="tight")
            else:
                self.figg.savefig(f"{self.time_now}-{ticker}-PERband.png", bbox_inches="tight")
            self.timeline.setText("저장 성공")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chater = Charter()
    sys.exit(app.exec_())
