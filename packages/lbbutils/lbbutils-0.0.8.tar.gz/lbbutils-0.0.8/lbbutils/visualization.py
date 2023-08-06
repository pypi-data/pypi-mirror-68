import numpy as np
import torch
from torchvision import utils
import os
import time


class Visualization:
    def __init__(self, args):
        self.args = args
        from visdom import Visdom
        self.vis = Visdom()
        self.save_log = os.path.join(args.save_path, 'log', 'loss_log.txt')
        self.save_img = os.path.join(args.save_path, 'img')
        os.makedirs(os.path.dirname(self.save_log), exist_ok=True)
        os.makedirs(self.save_img, exist_ok=True)
        with open(self.save_log, 'w') as f:
            f.write('====================Train Loss(%s)========================\n' % time.strftime('%c'))

    def print_current_loss(self, e, iter, loss, iter_time, issave=True):
        """
        打印第e个epoch下第iter个batch损失值和的耗时
        :param issave:  是否保存loss记录。（默认保存）
        :param e:
        :param iter:
        :param loss:
        :param iter_time: 训练这个batch所需要的时间
        :return:
        """
        message = f'[Epoch {e}/{self.args.epochs}]-[batch {iter}/{self.args.len_dataloader}] ' \
                  f'\tLoss: {loss}\ttime: {iter_time}'
        print(message)
        if issave == True:
            with open(self.save_log, 'a') as f:
                f.write(message + '\n')

    def plot_current_loss(self, e, iter, loss):
        """
        将loss连成连线
        :param e:
        :param iter:
        :param loss:
        :return:
        """
        if not hasattr(self, 'plot_data'):
            self.plot_data = {'x': [], 'y': []}
        self.plot_data['x'].append(e + iter / self.args.len_dataloader)
        self.plot_data['y'].append(loss)
        x = np.stack(self.plot_data['x'])
        y = np.stack(self.plot_data['y'])
        self.vis.line(Y=y,
                      X=x,
                      opts={
                          'title': self.args.name + ' loss over time',
                          'xlabel': 'epoch',
                          'ylabel': 'loss'
                      })

    def display_current_result(self, e, visuals: dict, issave=True):
        """
        显示图像
        :param issave: boolean 是否保存网络输入输出、target和label
        :param epoch:
        :param visual:
        :return:
        """
        ncols = len(visuals)
        imgs = [np.array(img.cpu().detach()[0]) for img in visuals.values()]
        self.vis.images(imgs, nrow=ncols, padding=2, opts=dict(title=self.args.name + ' images'))
        if issave:
            for i, img in visuals.items():
                utils.save_image(img, os.path.join(self.save_img, f'{e}_{i}.png'))


if __name__ == '__main__':
    from lbbutils.easydict import EasyDict

    d = {'epochs': 100, 'len_dataloader': 58, 'name': 'four', 'save_path': 'save'}
    args = EasyDict(d)

    visualizer = Visualization(args)
    # visualizer.print_current_loss(1, 5, 0.088, 5.666)
    visualizer.plot_current_loss(2, 0.5, 1.8)
    #
    # dd = {'l': torch.rand((2, 3, 256, 256)),
    #       'r': torch.rand((2, 3, 256, 256)),
    #       'label': torch.rand((2, 3, 256, 256)),
    #       'y': torch.rand((2, 3, 256, 256))}
    #
    # visualizer.display_current_result(1,dd)
