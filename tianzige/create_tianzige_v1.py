import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def draw_pinyin_tianzige(filename):
    # 创建 A4 画布
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # 设置页面边距（单位：磅，1英寸=72磅）
    margin_left = 40
    margin_right = 40
    top_margin = 40
    bottom_margin = 40
    
    available_width = width - margin_left - margin_right
    
    # 设定每行 12 个格子
    cols = 12
    cell_size = available_width / cols  # 自动计算每个田字格的尺寸
    pinyin_height = cell_size * 0.45    # 拼音格高度约为田字格的 45%
    
    row_height = cell_size + pinyin_height
    row_gap = 15  # 每组（拼音+田字格）之间的行间距
    
    start_y = height - top_margin
    current_y = start_y
    
    # 计算一页 A4 纸能完美容纳的行数
    usable_height = height - top_margin - bottom_margin
    num_rows = int(usable_height / (row_height + row_gap))
    
    for r in range(num_rows):
        pinyin_top = current_y
        pinyin_bottom = pinyin_top - pinyin_height
        
        tianzige_top = pinyin_bottom
        tianzige_bottom = tianzige_top - cell_size
        
        # 逐个格子绘制，确保拼音与田字格左右完全对齐
        for c_idx in range(cols):
            x_left = margin_left + c_idx * cell_size
            x_right = x_left + cell_size
            
            # --- 1. 绘制拼音格 (带有外框以及内部两条虚线，形成四线三格) ---
            # 绘制拼音外框（深灰色实线）
            c.setStrokeColor(colors.HexColor("#555555"))
            c.setLineWidth(0.8)
            c.setDash()  # 恢复实线
            c.rect(x_left, pinyin_bottom, cell_size, pinyin_height, fill=0, stroke=1)
            
            # 绘制拼音内部的两条水平分隔线（浅灰色细虚线）
            c.setStrokeColor(colors.HexColor("#aaaaaa"))
            c.setLineWidth(0.5)
            c.setDash(2, 2)  # 设置虚线
            
            pinyin_space = pinyin_height / 3.0
            c.line(x_left, pinyin_bottom + pinyin_space, x_right, pinyin_bottom + pinyin_space)
            c.line(x_left, pinyin_bottom + 2 * pinyin_space, x_right, pinyin_bottom + 2 * pinyin_space)
            
            # --- 2. 绘制田字格 ---
            # 绘制田字格大外框（深灰色实线）
            c.setStrokeColor(colors.HexColor("#555555"))
            c.setLineWidth(0.8)
            c.setDash()  # 恢复实线
            c.rect(x_left, tianzige_bottom, cell_size, cell_size, fill=0, stroke=1)
            
            # 绘制田字格内部的十字中心线（浅灰色细虚线）
            c.setStrokeColor(colors.HexColor("#aaaaaa"))
            c.setLineWidth(0.5)
            c.setDash(2, 2)  # 设置虚线
            
            # 水平中心线
            c.line(x_left, tianzige_bottom + cell_size/2.0, x_right, tianzige_bottom + cell_size/2.0)
            # 垂直中心线
            c.line(x_left + cell_size/2.0, tianzige_bottom, x_left + cell_size/2.0, tianzige_top)
            
        # 移动到下一行
        current_y = tianzige_bottom - row_gap
        
    c.showPage()
    c.save()
    print(f"成功生成字帖：{filename}")

if __name__ == "__main__":
    draw_pinyin_tianzige("my_blank_pinyin_tianzige.pdf")
