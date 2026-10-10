import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def draw_pinyin_tianzige(filename):
    # 创建 A4 画布（默认纵向：宽595.27点，高841.89点）
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # 设置页面边距（单位：磅，1英寸=72磅）
    margin_left = 40
    margin_right = 40
    top_margin = 40
    bottom_margin = 40
    
    # 【新增】横向对折中央空白区的宽度（单位：磅，40磅大约 1.4 厘米，可根据需要调整）
    center_gap = 40
    
    # 每一行包含 12 个格子，自动计算每个田字格的尺寸
    available_width = width - margin_left - margin_right
    cols = 12
    cell_size = available_width / cols  
    pinyin_height = cell_size * 0.45    # 拼音格高度约为田字格的 45%
    
    row_height = cell_size + pinyin_height
    row_gap = 15  # 正常的行间距
    
    # 计算一页 A4 纸在扣除中间折叠区后，能完美容纳的总行数
    usable_height = height - top_margin - bottom_margin - center_gap
    num_rows = int(usable_height / (row_height + row_gap))
    
    # 为了保证上下两部分完全对称，总行数必须是偶数（如果计算出奇数则向下取偶）
    if num_rows % 2 != 0:
        num_rows -= 1
        
    half_rows = num_rows // 2  # 上半页和下半页各自的行数
    
    start_y = height - top_margin
    current_y = start_y
    
    for r in range(num_rows):
        # 【核心修改】当绘制到下半页的第一行时，额外加上中央对折的空白间距
        if r == half_rows:
            current_y -= center_gap
            
        pinyin_top = current_y
        pinyin_bottom = pinyin_top - pinyin_height
        
        tianzige_top = pinyin_bottom
        tianzige_bottom = tianzige_top - cell_size
        
        # 逐个格子绘制
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
    print(f"成功生成横向对折字帖：{filename}")

if __name__ == "__main__":
    draw_pinyin_tianzige("my_blank_pinyin_tianzige.pdf")
