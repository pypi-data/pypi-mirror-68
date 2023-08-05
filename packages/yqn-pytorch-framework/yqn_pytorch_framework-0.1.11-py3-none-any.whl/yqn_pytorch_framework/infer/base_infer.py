import os
from abc import abstractmethod

import torch
import numpy as np
from yqn_config.base_config import BaseConfig
from yqn_exception.exception import InputSizeException, InferModelException
from yqn_pytorch_framework.device import get_device
from yqn_pytorch_framework.train.base_engine import BaseModelEngine


class BaseModelInfer:
    def __init__(self, model_config: BaseConfig):
        self.config = model_config
        self.device = model_config.device
        with torch.no_grad():
            self.model = self.load_model().to(self.device)
            resume_file = self.get_infer_model_file()
            if os.path.exists(resume_file):
                print("=> loading checkpoint '{}'".format(resume_file))
                checkpoint = torch.load(resume_file, map_location=self.device)
                if hasattr(self.config, "saved_state"):
                    if self.config.saved_state:
                        self.model.load_state_dict(checkpoint, strict=False)
                    else:
                        self.model.load_state_dict(checkpoint['state_dict'])
                else:
                    self.model.load_state_dict(checkpoint['state_dict'])

                self.model.eval()
                print("=> loaded checkpoint '{}' ".format(resume_file))
            else:
                raise InferModelException("infer model not found " + str(resume_file))

        super(BaseModelInfer, self).__init__()

    def get_infer_model_file(self):
        """
        :return: infer_model 文件路径
        """
        directory = self.config.get_train_model_out_dir(self.config.split_date)
        infer_model_path = os.path.join(directory, 'model_best.pth')
        return infer_model_path

    @abstractmethod
    def load_model(self):
        """
        :return: model
        """
        pass

    @abstractmethod
    def get_input_size_without_batch(self):
        pass

    @abstractmethod
    def format_output(self, outputs, input_features):
        pass

    @abstractmethod
    def pre_handle(self, input_features):
        pass

    def infer(self, input_features):
        with torch.no_grad():
            input_features_handled = self.pre_handle(input_features)
            input_shape = input_features_handled.shape
            shape_len = len(input_shape)
            expect_input = self.get_input_size_without_batch()
            is_same_size = True
            for index in range(shape_len - 1):
                is_same_size = is_same_size & (input_shape[index + 1] == expect_input[index])
            if not is_same_size:
                raise InputSizeException("input shape error")
            per_size = self.config.batch_size
            loop_size = int(input_shape[0] / per_size) + (0 if input_shape[0] % per_size == 0 else 1)
            outputs = []
            for index in range(loop_size):
                input_converted = input_features_handled[
                                  index * per_size: min(input_shape[0], (index + 1) * per_size), ]
                input_tensor = torch.from_numpy(np.array(input_converted)).to(self.config.device)
                result = self.model(input_tensor)
                outputs.append(result)
            outputs = torch.cat(outputs, dim=0)
            return self.format_output(outputs, input_features)
