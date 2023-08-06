from .myModel import MyModel


class MyModelLRSchedulerEvalLoss(MyModel):
    """ Model with LRScheduler monitoring evaluation loss. """

    def __init__(self, net, device=None):
        super().__init__(net, device)
        self.scheduler_type = "eval_loss"
