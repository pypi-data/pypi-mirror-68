# The MIT License (MIT)
#
# Copyright (c) 2020 University of East Anglia, Norwich, UK
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Developed by Geoffrey French in collaboration with Dr. M. Fisher and
# Dr. M. Mackiewicz.

import torch


class PolynomialLR(torch.optim.lr_scheduler._LRScheduler):
    r"""Set the learning rate of each parameter group using a polynomial
    schedule.

    Args:
        optimizer (Optimizer): Wrapped optimizer.
        T_max (int): Maximum number of iterations.
        eta_min (float): Minimum learning rate. Default: 0.
        last_epoch (int): The index of last epoch. Default: -1.

    .. _SGDR\: Stochastic Gradient Descent with Warm Restarts:
        https://arxiv.org/abs/1608.03983
    """

    def __init__(self, optimizer, T_max, power=0.9, eta_min=0.0, last_epoch=-1):
        self.T_max = T_max
        self.power = power
        self.eta_min = eta_min
        super(PolynomialLR, self).__init__(optimizer, last_epoch)

    def get_lr(self):
        if self.last_epoch == 0:
            return self.base_lrs
        else:
            # Get progress through schedule
            progress = float(self.last_epoch) / float(self.T_max)
            # Clamp to [0,1]
            progress = min(max(progress, 0), 1)
            # Compute annealing factor
            fac = (1.0 - progress) ** self.power
            fac = max(fac, self.eta_min)
            return [base_lr * fac for base_lr in self.base_lrs]


def make_lr_scheduler(optimizer, total_iters, schedule_type, poly_power=0.9):
    if schedule_type == 'none':
        return None
    elif schedule_type == 'cosine':
        return torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer=optimizer, T_max=total_iters, eta_min=0.0
        )
    elif schedule_type == 'poly':
        return PolynomialLR(
            optimizer=optimizer, T_max=total_iters, power=poly_power, eta_min=0.0)
    elif callable(schedule_type):
        return schedule_type(optimizer=optimizer, T_max=total_iters)
    else:
        raise ValueError('Unknown schedule_type {}'.format(schedule_type))
