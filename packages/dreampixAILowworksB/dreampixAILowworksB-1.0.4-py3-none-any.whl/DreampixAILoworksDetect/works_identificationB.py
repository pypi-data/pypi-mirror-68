import torch
import requests
import time
from PIL import Image
from io import BytesIO
from .se_resnet import *
from torchvision import transforms

class LowQuaWorksB(object):
    def __init__(self,param_dir,_device="cpu"):
        '''
        :param param_dir: 模型参数文件地址
        :param _device: "cpu" or "cuda:0","cuda:1","cuda:2",...
        '''
        super(LowQuaWorksB)
        self.device = torch.device(_device)
        self.transforms = transforms.ToTensor()
        self.model_param_path = param_dir
        # model_param_path = "weights/24300_8.910774909054453e-07.pt"
        self.model = se_resnet50(num_classes=4)
        self.model.to(self.device)
        self.model.load_state_dict(torch.load(self.model_param_path, map_location=f"{self.device}"))
        self.model.eval()
    def downloadimg(self,url):
        try:
            t_start = time.time()
            response = requests.get(url)
            img = Image.open(BytesIO(response.content)).convert('RGB')
            img = img.resize((224,224))
            #img = self.normalizing(img).unsqueeze(0)
            t_end = time.time()
            cost_time = t_end - t_start
            #print(f"download img:{img.shape},cost time:{cost_time:.4f}")
            return img,cost_time

        except:
            return None
    def img2tensor(self,img):
        img = (self.transforms(img).unsqueeze(0)-0.5)*2
        return img
    def infer(self,url):
        '''
        模型推理（接口输入）
        :param url: 图像地址
        :return:0: 其他; 1: 打招呼图像3: 主页图像
        '''
        img ,download_time= self.downloadimg(url)
        if img is not None:
            img_ten = self.img2tensor(img)
            with torch.no_grad():
                predict = self.model(img_ten.to(self.device))
                out = predict.argmax(dim=1).item()
                if out==2:
                    out=0
                return out

if __name__ == "__main__":
    '''模型初始化'''
    # param_dir : 模型参数地址
    # _device : cpu or gpu, when using gpu,as "cuda:0",0 is the gpu index
    model = LowQuaWorksB(param_dir="model_path/24300_8.910774909054453e-07.pt",_device="cpu")
    #model = LowQuaWorksB(param_dir="model_path/24300_8.910774909054453e-07.pt", _device="cuda:0")

    '''模型推理'''
    '''元素样例在elements文件夹里'''
    zhaohu1 = "http://qnc.chumanapp.com/app/comics/titles/title_34725802_2_f66b9c52e6aa46da97a27932c309dd98.jpg"
    zhuye3 = "http://qnc.chumanapp.com/app/comics/titles/title_33932632_2_faff6e32c2534630bca68456c10b25eb.jpg"
    qita2 = "http://qnc.chumanapp.com/app/comics/titles/title_1e524df9a3afcd8ef8c5ca89346f46ad.jpg"
    qita0 = "http://qnc.chumanapp.com/app/comics/titles/title_35931874_4_20e7b8062552430aa2592c3b27adda50.jpg"

    result = model.infer(url=zhaohu1)
    print(result)




