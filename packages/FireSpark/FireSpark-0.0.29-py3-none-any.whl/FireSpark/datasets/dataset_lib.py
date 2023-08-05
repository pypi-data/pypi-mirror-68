
# FireSpark -- the Data Work
# Copyright 2020 The FireSpark Author. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""FireSpark custom dataset utility library """

import cv2
import numpy as np
from ..core.data_utils import SparkDataset


class L5ImageDataset(SparkDataset):
    """ Level5 image dataset class """
    def __init__(self, **job):
        super().__init__(**job)
    
    def _row_generator(self, pd):
        """ generate information from an image proto

            Args:
            pd: image proto message

            Return:
            dictionary of image data and annotation
        """		
        if self.prepare_label_fn:
            label = self.prepare_label_fn(pd.image_data.annotation)
        else:
            label = self.prepare_label(pd.image_data.annotation)
        im = cv2.imdecode(np.fromstring(pd.image_data.image.data, dtype=np.uint8), -1)

        if label.size == 0 or im is None:
            return None

        return {
            'width': pd.image_data.image.width,
            'height': pd.image_data.image.height,
            'depth': pd.image_data.image.depth,
            'format': pd.image_data.image.format,
            'imdata': im,
            'label': label
        }


class L5TLImageDataset(SparkDataset):
    """ Level5 traffic light image dataset class """
    def __init__(self, **job):
        super().__init__(**job)
        self.l2l = {5100:5100, 5101:5100, 5102:5100, 5103:5100}
    
    def prepare_label(self, annotation):
        label = []
        bbxs = []
        attributes = []
        for obj in annotation.objects:
            if not obj.oclass in self.l2l.keys(): continue
            label.append([self.l2l[obj.oclass]])
            bbxs.append((obj.cbox.x, obj.cbox.y, obj.cbox.w, obj.cbox.h))
            if obj.attributes:
                attri = []
                for a in obj.attributes:
                    attri.append(a)
                if len(attri)==1: attri.append(0)
                if len(attri)>2: attri=attri[:2]
                attributes.append(attri)
            else:
                attributes.append([0, 0])
        return np.array(label), np.array(bbxs), np.array(attributes)

    def _row_generator(self, pd):
        """ generate information from an image proto

            Args:
            pd: image proto message

            Return:
            dictionary of image data and annotation
        """		
        label, bbxs, attribs = self.prepare_label(pd.image_data.annotation)
        im = cv2.imdecode(np.fromstring(pd.image_data.image.data, dtype=np.uint8), -1)
        if label.size == 0 or im is None:
            return None

        return {
            'width': pd.image_data.image.width,
            'height': pd.image_data.image.height,
            'depth': pd.image_data.image.depth,
            'format': pd.image_data.image.format,
            'imdata': im,
            'label': label,
            'attributes': attribs,
            'bbxs': bbxs
        }