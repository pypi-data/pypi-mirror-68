from fnmatch import fnmatchcase as match
from os import listdir
from os.path import join
from typing import Tuple, List, Any

import torchvision.transforms.functional as F
from PIL import Image
from PIL import ImageFilter
from torch import Tensor
from torchvision.transforms import ToPILImage


class BlurImage(object):
    def __init__(self, num_div, style='C'):
        self.num_div = num_div
        self.style = style

    def __call__(self, image):
        l = Image.new('L', image.size)
        r = Image.new('L', image.size)
        blocks = []
        block_size = image.size[0] // self.num_div
        for row in range(1, self.num_div + 1):
            for col in range(1, self.num_div + 1):
                box = (block_size * (col - 1), block_size * (row - 1), block_size * (col - 1) + block_size + 1,
                       block_size * (row - 1) + block_size + 1)
                block = image.crop(box)
                blocks.append(block)
                blur_block = block.filter(ImageFilter.GaussianBlur(radius=3))
                if self.style == 'C':
                    if row % 2 == 1:
                        if (self.num_div * (row - 1) + (col - 1)) % 2 == 0:
                            l.paste(blur_block, box)
                            r.paste(block, box)
                        else:
                            l.paste(block, box)
                            r.paste(blur_block, box)
                    else:
                        if (self.num_div * (row - 1) + (col - 1)) % 2 == 1:
                            l.paste(blur_block, box)
                            r.paste(block, box)
                        else:
                            l.paste(block, box)
                            r.paste(blur_block, box)
                elif self.style == 'P':
                    if (self.num_div * (row - 1) + (col - 1)) % 2 == 0:
                        l.paste(blur_block, box)
                        r.paste(block, box)
                    else:
                        l.paste(block, box)
                        r.paste(blur_block, box)
        return l, r, image


class ToTensors(object):
    def __call__(self, pic):
        return F.to_tensor(pic[0]), F.to_tensor(pic[1]), F.to_tensor(pic[2])


def save_img(imgs: Tuple[Tensor]) -> List[Any]:
    ret = list()
    for i, img in enumerate(imgs):
        if img.is_cuda:
            img = img.cpu().clone()
        else:
            img = img.clone()
        img.squeeze_(0)
        img_PIL = ToPILImage()(img)
        ret.append(img_PIL)
    return ret


def path_match(root, word):
    items = listdir(root)
    tmp = [item for item in items if match(item, '*-' + word + '-*')]
    return join(root, tmp[-1])


if __name__ == '__main__':
    pass
