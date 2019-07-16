import struct
from struct import unpack, pack


# 读取并存储 bmp 文件
class ReadBMPFile:
    def __init__(self, filePath):
        file = open(filePath, "rb")
        # 读取 bmp 文件的文件头    14 字节
        self.bfType = unpack("<h", file.read(2))[0]  # 0x4d42 对应BM 表示这是Windows支持的位图格式
        print(self.bfType)
        self.bfSize = unpack("<i", file.read(4))[0]  # 位图文件大小
        print(self.bfSize)
        self.bfReserved1 = unpack("<h", file.read(2))[0]  # 保留字段 必须设为 0
        self.bfReserved2 = unpack("<h", file.read(2))[0]  # 保留字段 必须设为 0
        self.bfOffBits = unpack("<i", file.read(4))[0]  # 偏移量 从文件头到位图数据需偏移多少字节（位图信息头、调色板长度等不是固定的，这时就需要这个参数了）
        print(self.bfOffBits)
        # 读取 bmp 文件的位图信息头 40 字节
        self.biSize = unpack("<i", file.read(4))[0]  # 所需要的字节数
        self.biWidth = unpack("<i", file.read(4))[0]  # 图像的宽度 单位 像素
        print(self.biSize)
        print('self.biWidth:', self.biWidth)
        self.biHeight = unpack("<i", file.read(4))[0]  # 图像的高度 单位 像素
        print(self.biHeight)
        self.biPlanes = unpack("<h", file.read(2))[0]  # 说明颜色平面数 总设为 1
        self.biBitCount = unpack("<h", file.read(2))[0]  # 说明比特数
        print('self.biBitCount:', self.biBitCount)
        self.biCompression = unpack("<i", file.read(4))[0]  # 图像压缩的数据类型
        print('self.biCompression:', self.biCompression)
        self.biSizeImage = unpack("<i", file.read(4))[0]  # 图像大小
        print(self.biSizeImage)
        self.biXPelsPerMeter = unpack("<i", file.read(4))[0]  # 水平分辨率
        self.biYPelsPerMeter = unpack("<i", file.read(4))[0]  # 垂直分辨率
        self.biClrUsed = unpack("<i", file.read(4))[0]  # 实际使用的彩色表中的颜色索引数
        self.biClrImportant = unpack("<i", file.read(4))[0]  # 对图像显示有重要影响的颜色索引的数目
        self.bmp_data = []

        if self.biBitCount != 24:
            print("输入的图片比特值为 ：" + str(self.biBitCount) + "\t 与程序不匹配")

        for height in range(self.biHeight):
            bmp_data_row = []
            # 四字节填充位检测
            count = 0
            for width in range(self.biWidth):
                bmp_data_row.append(
                    [unpack("<B", file.read(1))[0], unpack("<B", file.read(1))[0], unpack("<B", file.read(1))[0]])
                count = count + 3
            # bmp 四字节对齐原则
            while count % 4 != 0:
                file.read(1)
                count = count + 1
            self.bmp_data.append(bmp_data_row)
        # self.bmp_data.reverse()
        print(self.bmp_data[0])
        file.close()

    def get_head(self):
        width1 = ((self.biWidth // 3) * self.biBitCount + 31) // 32 * 4
        print('width1:', width1)
        num_0 = width1 - self.biWidth // 3 * 3
        # 切割后，3*3图片的像素尺寸
        h = self.biHeight // 3
        w = self.biWidth // 3
        for y in range(3):
            for x in range(3):
                with open(str(y)+'-'+str(x)+'s.bmp', 'wb+') as f:
                    # bmp文件头
                    f.write(pack("<h", self.bfType))
                    f.write(pack("<i", width1 * (self.biHeight // 3) + 54))
                    f.write(pack("<h", self.bfReserved1))
                    f.write(pack("<h", self.bfReserved2))
                    f.write(pack("<i", self.bfOffBits))
                    # 位图信息头
                    f.write(pack("<i", self.biSize))
                    f.write(pack("<i", self.biWidth // 3))
                    f.write(pack("<i", self.biHeight // 3))
                    f.write(pack("<h", self.biPlanes))
                    f.write(pack("<h", self.biBitCount))
                    f.write(pack("<i", self.biCompression))
                    f.write(pack("<i", self.biSizeImage))
                    f.write(pack("<i", self.biXPelsPerMeter))
                    f.write(pack("<i", self.biYPelsPerMeter))
                    f.write(pack("<i", self.biClrUsed))
                    f.write(pack("<i", self.biClrImportant))

                    for line in range(h * y, h * (y + 1)):
                        s = struct.Struct('B')
                        for col in range(w * x, w * (x + 1)):
                            f.write(s.pack(self.bmp_data[line][col][0]))
                            f.write(s.pack(self.bmp_data[line][col][1]))
                            f.write(s.pack(self.bmp_data[line][col][2]))
                        for n in range(num_0):
                            f.write(s.pack(0))


if __name__ == '__main__':
    a = ReadBMPFile('dfss.bmp')
    a.get_head()


