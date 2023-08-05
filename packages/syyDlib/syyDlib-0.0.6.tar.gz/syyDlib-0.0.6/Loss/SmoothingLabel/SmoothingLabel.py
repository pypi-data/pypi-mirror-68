import torch.nn as nn
import torch


class LabelSmoothSoftmaxCEV1(nn.Module):

    def __init__(self, lb_smoothing=0.1, reduction='mean', ignore_index=-100, keep_origin=[]):
        '''

        :param lb_smoothing: smoothing label value
        :param reduction: mean or sum or None
        :param ignore_index: what kind of label do you want to ignore, for example 1, the function will set the loss of
        label 1 to zero
        :param keep_origin: what kind of label do you want to keep, which means you do not want to change
        '''
        super(LabelSmoothSoftmaxCEV1, self).__init__()
        self.lb_smooth = lb_smoothing
        self.reduction = reduction
        self.lb_ignore = ignore_index
        self.log_softmax = nn.LogSoftmax(dim=1)
        self.keep_origin = keep_origin

    def forward(self, logits, label):
        '''

        :param logits: prediction of model
        :param label: not one hot format
        :return: loss
        '''
        # overcome ignored label
        with torch.no_grad():
            num_cls = logits.size(1)
            ori_label = label.clone().detach()
            ignore = ori_label == self.lb_ignore
            n_valid = (ignore == 0).sum()
            ori_label[ignore] = 0
            lb_pos, lb_neg = 1. - self.lb_smooth, self.lb_smooth / num_cls
            label = torch.empty_like(logits).fill_(lb_neg).scatter(1, ori_label.unsqueeze(1), lb_pos).detach()
            for i in self.keep_origin:
                keep = ori_label == i

                label[keep, :] = 0
                label[keep, i] = 1

        log = self.log_softmax(logits)
        loss = -torch.sum(log * label, dim=1)
        loss[ignore] = 0

        if self.reduction == 'mean':
            loss = loss.sum() / n_valid
        elif self.reduction == 'sum':
            loss = loss.sum()

        return loss
