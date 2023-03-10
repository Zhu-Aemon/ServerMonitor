from PySide6.QtCore import QTimer, QDateTime
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
import socket


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('GUI.ui')  # 替换为你的UI文件名
        self.setCentralWidget(self.ui)
        self.timer = None

        # 设置控件的默认值和属性
        self.ui.TE_IP.setPlainText('45.32.117.183')
        self.ui.TE_port.setPlainText('220')
        self.ui.TE_interval.setPlainText('10')
        self.ui.TE_result.setPlainText('0.0 %')
        self.ui.TE_result.setReadOnly(True)
        self.ui.TE_log.setReadOnly(True)
        self.ui.Btn_start.setEnabled(True)
        self.ui.Btn_stop.setEnabled(False)

        # 设置控件的信号槽
        self.ui.Btn_start.clicked.connect(self.start_ping)
        self.ui.Btn_stop.clicked.connect(self.stop_ping)

    def start_ping(self):
        self.ui.Btn_start.setEnabled(False)
        self.ui.Btn_stop.setEnabled(True)

        # 获取输入的IP地址、端口号和间隔时间
        ip_address = self.ui.TE_IP.toPlainText().strip()
        port = int(self.ui.TE_port.toPlainText().strip())
        interval = int(self.ui.TE_interval.toPlainText().strip())

        # 初始化连接成功次数和总次数
        success_count = 0
        total_count = 0

        # 初始化定时器和日志输出
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.ping(ip_address, port, success_count, total_count))
        self.timer.start(interval * 1000)  # QTimer的单位为毫秒，需要乘以1000
        self.ui.TE_log.setPlainText('')  # 清空日志输出框

    def stop_ping(self):
        self.ui.Btn_start.setEnabled(True)
        self.ui.Btn_stop.setEnabled(False)

        # 停止定时器
        self.timer.stop()

    def ping(self, ip_address, port, success_count, total_count):
        # 尝试连接指定的IP地址和端口
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)  # 超时时间设为1秒
            start_time = QDateTime.currentDateTime()  # 记录连接开始时间
            s.connect((ip_address, port))
            end_time = QDateTime.currentDateTime()  # 记录连接结束时间
            s.close()
            success_count += 1
            ping_time = (end_time.toMSecsSinceEpoch() - start_time.toMSecsSinceEpoch())  # 计算连接时间
            self.ui.TE_log.appendPlainText(f"[{end_time.toString('yyyyMMdd hh:mm:ss')}] 连接成功，tcping {ping_time}ms")
        except Exception as e:
            self.ui.TE_log.appendPlainText(
                f"[{QDateTime.currentDateTime().toString('yyyyMMdd hh:mm:ss')}] 连接失败，{str(e)}")

        total_count += 1
        success_rate = success_count / total_count * 100
        self.ui.TE_result.setPlainText(f"{success_rate:.2f} %")  # 显示连接成功率

    def closeEvent(self, event):
        # 关闭程序时停止所有定时器
        timer_list = self.findChildren(QTimer)
        for timer in timer_list:
            timer.stop()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
