import tkinter as tk
import tkinter.ttk as ttk

def copy_result():
    result = result_label.cget("text")
    result = result.replace("逆序结果：", "")
    result = result.replace("BCC异或校验值：", "")
    result = result.replace(" ", "")
    result = result.replace("\n", "")
    window.clipboard_clear()
    window.clipboard_append(result)

def convert_to_hex():
    decimal_str = entry.get()

    # 检测输入是否正确
    if len(decimal_str) != 10 or not decimal_str.isdigit():
        result_label.config(text="请输入10位的十进制字符串！")
        return

    # 将十进制字符串转换为十六进制
    hex_str = hex(int(decimal_str))[2:]

    # 检测转换后的十六进制字符串是否为8位,不足8位则在首位加0直至补足八位
    if len(hex_str) < 8:
        hex_str = '0' * (8 - len(hex_str)) + hex_str

    # 将十六进制字符串从右到左，以2位为单位逆序
    reversed_hex_str = ''
    for i in range(0, len(hex_str), 2):
        reversed_hex_str = hex_str[i:i+2] + reversed_hex_str

    # 计算BCC16进制校验值
    bcc = hex(sum(int(reversed_hex_str[i:i+2], 16) for i in range(0, len(reversed_hex_str), 2)) % 256)[2:]
    if len(bcc) == 1:
        bcc = '0' + bcc

    # 计算BCC异或校验值
    xor_result = int(reversed_hex_str[0:2], 16)
    for i in range(2, len(reversed_hex_str), 2):
        xor_result ^= int(reversed_hex_str[i:i+2], 16)
    bcc_xor = hex(xor_result)[2:]
    if len(bcc_xor) == 1:
        bcc_xor = '0' + bcc_xor

    result_label.config(text=f"逆序结果：{reversed_hex_str.upper()}\nBCC异或校验值：{bcc_xor.upper()}")
    copy_button.config(state="normal")

# 创建窗口
window = tk.Tk()
window.title("ID卡号转写NFC")
window.geometry("300x150")

# 创建标签和输入框
label = tk.Label(window, text="请输入10位的十进制字符串：")
label.pack()
entry = tk.Entry(window)
entry.pack()

# 创建转换按钮
button = tk.Button(window, text="转换", command=convert_to_hex)
button.pack()

# 创建结果标签
result_label = tk.Label(window, text="")
result_label.pack()

# 创建复制按钮
copy_button = ttk.Button(window, text="复制", state="disabled", command=copy_result)
copy_button.pack()

# 运行窗口
window.mainloop()
