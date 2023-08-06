import csv
import logging
import os

import numpy as np
import torch.utils.data
from PIL import Image

from .. import transforms


LOG = logging.getLogger(__name__)


class Human36m(torch.utils.data.Dataset):
    def __init__(self, image_dir, ann_dir, *, target_transforms=None,
                 n_images=None, preprocess=None):
        self.image_dir = image_dir
        self.ann_dir = ann_dir

        self.ids = [
            fn[:-4]
            for fn in os.listdir(ann_dir)
            if fn.endswith('.csv')
        ]
        if n_images:
            self.ids = self.ids[:n_images]
        LOG.info('Images: %d', len(self.ids))

        self.preprocess = preprocess or transforms.EVAL_TRANSFORM
        self.target_transforms = target_transforms

    def __getitem__(self, index):
        id_ = self.ids[index]
        image_path = os.path.join(self.image_dir, '{}.jpg'.format(id_))
        ann_path = os.path.join(self.ann_dir, '{}.csv'.format(id_))
        LOG.debug('image = %s, ann = %s', image_path, ann_path)

        with open(image_path, 'rb') as f:
            image = Image.open(f).convert('RGB')

        with open(ann_path, 'r') as f:
            filereader = csv.reader(f)
            keypoints3d = [
                [float(v) for v in row]
                for row in filereader
            ]
        anns = [{
            'keypoints3d': np.array(keypoints3d, dtype=np.float32),
            'iscrowd': False,
            'bbox': np.zeros((4,), dtype=np.float32)
        }]

        meta = {
            'dataset_index': index,
            'image_id': id_,
            'file_name': image_path,
        }

        # preprocess image and annotations
        image, anns, meta = self.preprocess(image, anns, meta)

        # transform targets
        if self.target_transforms is not None:
            anns = [t(image, anns, meta) for t in self.target_transforms]

        return image, anns, meta

    def __len__(self):
        return len(self.ids)
