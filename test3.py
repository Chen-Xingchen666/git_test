import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, 
    QLabel, QTextEdit, QProgressBar, QTabWidget
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal

class HeavyComputationThread(QThread):
    """模拟繁重计算线程"""
    update_progress = pyqtSignal(int)
    result_ready = pyqtSignal(str)
    
    def run(self):
        for i in range(101):
            time.sleep(0.02)  # 模拟计算
            self.update_progress.emit(i)
        
        self.result_ready.emit("计算完成")

class PerformanceTestWindow(QWidget):
    """性能测试窗口，模拟真实应用场景"""
    def __init__(self, use_attribute=False, parent=None):
        super().__init__(parent)
        
        self.use_attribute = use_attribute
        self.setWindowTitle(f"性能测试 - 属性: {use_attribute}")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout(self)
        
        # 创建大量控件
        self.create_many_widgets(layout)
        
        # 启动性能测试
        self.start_performance_test()
    
    def create_many_widgets(self, layout):
        """创建大量重叠控件"""
        # 创建标签组
        labels = []
        for i in range(20):
            label = QLabel(f"标签 {i+1}")
            label.setStyleSheet(f"""
                background-color: rgba({(i*10)%255}, {(i*20)%255}, {(i*30)%255}, 100);
                padding: 2px;
                margin: 1px;
            """)
            labels.append(label)
            layout.addWidget(label)
        
        # 创建进度条组（会频繁更新）
        self.progress_bars = []
        for i in range(5):
            progress = QProgressBar()
            layout.addWidget(progress)
            self.progress_bars.append(progress)
        
        # 创建文本编辑区域
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText("性能测试输出区域\n" + "行\n" * 50)
        layout.addWidget(self.text_edit)
        
        # 启动计算线程
        self.start_btn = QPushButton("启动繁重计算")
        self.start_btn.clicked.connect(self.start_heavy_computation)
        layout.addWidget(self.start_btn)
    
    def start_performance_test(self):
        """启动性能监控"""
        self.frame_count = 0
        self.last_time = time.time()
        
        # 定时更新UI以测试性能
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_ui_performance)
        self.update_timer.start(16)  # ~60fps
    
    def update_ui_performance(self):
        """UI性能测试更新"""
        current_time = time.time()
        self.frame_count += 1
        
        # 每秒钟输出一次帧率
        if current_time - self.last_time >= 1.0:
            fps = self.frame_count / (current_time - self.last_time)
            status = f"属性:{self.use_attribute} - FPS: {fps:.1f}"
            self.setWindowTitle(status)
            self.frame_count = 0
            self.last_time = current_time
        
        # 轻微移动一些控件以测试渲染性能
        for i, progress in enumerate(self.progress_bars):
            value = (int(time.time() * 100) + i * 20) % 101
            progress.setValue(value)
    
    def start_heavy_computation(self):
        """启动繁重计算线程"""
        self.thread = HeavyComputationThread()
        self.thread.update_progress.connect(self.on_progress_update)
        self.thread.result_ready.connect(self.on_result_ready)
        self.thread.start()
    
    def on_progress_update(self, value):
        """更新进度"""
        for progress in self.progress_bars:
            progress.setValue(value)
    
    def on_result_ready(self, result):
        """计算完成"""
        self.text_edit.append(f"[{time.strftime('%H:%M:%S')}] {result}")

def test_performance(use_attribute=False):
    """测试性能"""
    app = QApplication(sys.argv)
    
    if use_attribute:
        app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    
    window = PerformanceTestWindow(use_attribute)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    # 分别运行两次测试，观察FPS差异
    # 第一次：use_attribute=False
    # 第二次：use_attribute=True
    
    use_attr = True  # 更改为 False 和 True 分别测试
    
    test_performance(use_attribute=use_attr)
