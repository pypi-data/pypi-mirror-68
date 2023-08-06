import random
from .config import CfgNode as CN

_C = CN()
_C.VERSION = 1


# ---------------------------------------------------------------------------- #
# input
# ---------------------------------------------------------------------------- #
_C.input = CN()
_C.input.size = (224, 224)

# ---------------------------------------------------------------------------- #
# dataset
# ---------------------------------------------------------------------------- #
_C.dataset = CN()
_C.dataset.name = 'cifar10'
_C.dataset.batch_size = 16
_C.dataset.dir = './datasets/skin100_dataset/train'
_C.dataset.train_list = './datasets/train_skin10.txt'
_C.dataset.valid_list = './datasets/valid_skin10.txt'
_C.dataset.test_list = './datasets/test_skin10.txt'
_C.dataset.is_train = False # specify to load training or testing set


# ---------------------------------------------------------------------------- #
# transforms
# ---------------------------------------------------------------------------- #

_C.transforms = CN() # image transforms
_C.transforms.name = 'DefaultTransforms'


## transforms for tensor
_C.transforms.tensor = CN()
# for skin100
_C.transforms.tensor.normalization = CN()
_C.transforms.tensor.normalization.mean = [0.6075, 0.4564, 0.4182] 
_C.transforms.tensor.normalization.std = [0.2158, 0.1871, 0.1826]
# _C.transforms.tensor.normalization = {
#             'mean':[0.6054, 0.4433, 0.4084], 
#             'std': [0.2125, 0.1816, 0.1786]  # for skin10
_C.transforms.tensor.random_erasing = CN()
_C.transforms.tensor.random_erasing.enable = 0
_C.transforms.tensor.random_erasing.p = 0.5
_C.transforms.tensor.random_erasing.scale = (0.02, 0.3) # range of proportion of erased area against input image.
_C.transforms.tensor.random_erasing.ratio = (0.3, 3.3), # range of aspect ratio of erased area.


# ---------------------------------------------------------------------------- #
# albumentations transforms (abtfs)
# ---------------------------------------------------------------------------- #

_C.abtfs = CN()
_C.abtfs.random_grid_shuffle = CN()
_C.abtfs.random_grid_shuffle.enable = 0
_C.abtfs.random_grid_shuffle.grid = 2

_C.abtfs.channel_shuffle = CN()
_C.abtfs.channel_shuffle.enable = 0

_C.abtfs.channel_dropout = CN()
_C.abtfs.channel_dropout.enable = 0
_C.abtfs.channel_dropout.drop_range = (1, 1)
_C.abtfs.channel_dropout.fill_value = 127

_C.abtfs.noise = CN()
_C.abtfs.noise.enable = 1

_C.abtfs.blur = CN()
_C.abtfs.blur.enable = 0
_C.abtfs.blur.blur_limit = 3

_C.abtfs.rotate = CN()
_C.abtfs.rotate.enable = 1
_C.abtfs.rotate.p = 1
_C.abtfs.rotate.shift_limit = 0.0625
_C.abtfs.rotate.scale_limit = 0.2
_C.abtfs.rotate.rotate_limit = 45
                 
_C.abtfs.bright = CN()
_C.abtfs.bright.enable = 1
_C.abtfs.bright.clip_limit = 1

_C.abtfs.distortion = CN()
_C.abtfs.distortion.enable = 0

_C.abtfs.hue = CN()
_C.abtfs.hue.enable = 0

_C.abtfs.cutout = CN()
_C.abtfs.cutout.enable = 1
_C.abtfs.cutout.num_holes = 10
_C.abtfs.cutout.size = 20
_C.abtfs.cutout.fill_value = 127

# ---------------------------------------------------------------------------- #
# torchvision transforms
# ---------------------------------------------------------------------------- #

## transforms for PIL image
_C.transforms.img = CN()

### modify the image size, only use one operation
# random_resized_crop
_C.transforms.img.random_resized_crop = CN()
_C.transforms.img.random_resized_crop.enable = 0
_C.transforms.img.random_resized_crop.scale = (0.5, 1.0)
_C.transforms.img.random_resized_crop.ratio = (3/4, 4/3)

# resize
_C.transforms.img.resize =  CN()
_C.transforms.img.resize.enable = 1

# random_crop
_C.transforms.img.random_crop = CN()
_C.transforms.img.random_crop.enable = 1
_C.transforms.img.random_crop.padding = 0

# center_crop
_C.transforms.img.center_crop = CN()
_C.transforms.img.center_crop.enable = 0

### without modifying the image size
_C.transforms.img.aug_imagenet = False
_C.transforms.img.aug_cifar = False

# color_jitter
_C.transforms.img.color_jitter = CN()
_C.transforms.img.color_jitter.enable = 0
_C.transforms.img.color_jitter.brightness = 0.
_C.transforms.img.color_jitter.contrast = 0.
_C.transforms.img.color_jitter.saturation = 0.
_C.transforms.img.color_jitter.hue = 0.

# horizontal_flip
_C.transforms.img.random_horizontal_flip = CN()
_C.transforms.img.random_horizontal_flip.enable = 1
_C.transforms.img.random_horizontal_flip.p = 0.5

# vertical_flip
_C.transforms.img.random_vertical_flip = CN()
_C.transforms.img.random_vertical_flip.enable = 1
_C.transforms.img.random_vertical_flip.p = 0.5

# random_rotation
_C.transforms.img.random_rotation = CN()
_C.transforms.img.random_rotation.enable = 1
_C.transforms.img.random_rotation.degrees = 10



_C.label_transforms = CN() # label transforms
_C.label_transforms.name = 'default'


# ---------------------------------------------------------------------------- #
# dataloader
# ---------------------------------------------------------------------------- #
_C.dataloader = CN()
_C.dataloader.num_workers = 4
_C.dataloader.sample_train = "default"
_C.dataloader.sample_test = "default"


# ---------------------------------------------------------------------------- #
# model
# ---------------------------------------------------------------------------- #
_C.model = CN()
_C.model.name = 'Resnet50'
_C.model.classes = 10
_C.model.pretrained = True
_C.model.finetune = False


# ---------------------------------------------------------------------------- #
# optimizer
# ---------------------------------------------------------------------------- #
_C.optim = CN()
_C.optim.name = 'adam'
_C.optim.momentum = 0.9
_C.optim.base_lr = 0.001
# _C.optim.lr = _C.optim.base_lr # will changed in v0.3.0.0
_C.optim.weight_decay = 0.0005

# scheduler
_C.optim.scheduler = CN()
_C.optim.scheduler.name = 'MultiStepLR'
_C.optim.scheduler.gamma = 0.1 # decay factor

# for CosineAnnealingLR
_C.optim.scheduler.t_max = 10 

# for CosineAnnealingLR
_C.optim.scheduler.t_0 = 5
_C.optim.scheduler.t_mul = 20

# for ReduceLROnPlateau
_C.optim.scheduler.mode = 'min' # min for loss, max for acc
_C.optim.scheduler.patience = 10
_C.optim.scheduler.verbose = True # print log once update lr

# for StepLR
_C.optim.scheduler.step_size = 10

# for MultiStepLR
_C.optim.scheduler.milestones = [10, 25, 35, 50]

# _C.optimizer = _C.optim # enhance compatibility. will changed in v0.3.0.0
# ---------------------------------------------------------------------------- #
# loss
# ---------------------------------------------------------------------------- #
_C.loss = CN()
_C.loss.name = 'CrossEntropy'
_C.loss.class_weight = []
_C.loss.label_smoothing = 0.1 # CrossEntropyLabelSmooth

_C.loss.focal_loss = CN()
_C.loss.focal_loss.alpha = [] # FocalLoss
_C.loss.focal_loss.gamma = 2
_C.loss.focal_loss.size_average = True
# ---------------------------------------------------------------------------- #
# hooks
# ---------------------------------------------------------------------------- #
_C.hooks = CN()

## EarlyStopping
_C.hooks.early_stopping = CN()
_C.hooks.early_stopping.setting = 2 # 0: True 1: False 2: custom
_C.hooks.early_stopping.monitor = 'valid_loss' # or 'valid_acc_1
_C.hooks.early_stopping.min_delta = 0.
_C.hooks.early_stopping.patience = 10
_C.hooks.early_stopping.mode = 'min' # or 'max
_C.hooks.early_stopping.verbose = 1

# ModelCheckpoint
_C.hooks.model_checkpoint = CN()
_C.hooks.model_checkpoint.setting = 2 # 0: True 1: False 2: custom
_C.hooks.model_checkpoint.filepath = '' # the empty file path is recommended
_C.hooks.model_checkpoint.monitor = 'valid_loss'
_C.hooks.model_checkpoint.mode = 'min'
_C.hooks.model_checkpoint.save_top_k = 1
_C.hooks.model_checkpoint.save_weights_only = False
_C.hooks.model_checkpoint.verbose = 1
_C.hooks.model_checkpoint.period = 1
_C.hooks.model_checkpoint.prefix = ''


# ---------------------------------------------------------------------------- #
# Module template 
# ---------------------------------------------------------------------------- #

_C.module = CN()
_C.module.name = 'DefaultModule'
_C.module.analyze_result = False 
# analyze the predictions and gt_laels, e.g., compute the f1_score, precision
# you can modify the `analyze_result(self, gt_labels, predictions)` in `default_module.py`


# ---------------------------------------------------------------------------- #
# Trainer 
# ---------------------------------------------------------------------------- #

_C.trainer = CN()
_C.trainer.name = 'DefaultTrainer'
_C.trainer.default_save_path = './output' # will be removed
_C.trainer.default_root_dir = './output'
_C.trainer.gradient_clip_val = 0 # 0 means don't clip.
_C.trainer.process_position = 0
_C.trainer.num_nodes = 1
_C.trainer.gpus = [] # list
_C.trainer.auto_select_gpus = False # If `auto_select_gpus` is enabled and `gpus` is an integer, pick available gpus automatically. 
                                    # This is especially useful when GPUs are configured to be  in "exclusive mode", such that 
                                    # only one process at a time can access them.
_C.trainer.num_tpu_cores = '' # How many TPU cores to train on (1 or 8).
_C.trainer.log_gpu_memory = "" # None, 'min_max', 'all'. Might slow performance
_C.trainer.show_progress_bar = False # will be removed
_C.trainer.progress_bar_refresh_rate = 0 # How often to refresh progress bar (in steps). Value ``0`` disables progress bar.
_C.trainer.overfit_pct = 0.0 # if 0<overfit_pct<1, (e.g. overfit_pct = 0.1) then train, val, test only 10% data.
_C.trainer.track_grad_norm = -1 # -1 no tracking. Otherwise tracks that norm. if equals to 2, then 2-norm will be traced
_C.trainer.check_val_every_n_epoch = 1 # Check val every n train epochs.
_C.trainer.fast_dev_run = False # everything only with 1 training and 1 validation batch.
_C.trainer.accumulate_grad_batches = 1 # Accumulates grads every k batches or as set up in the dict.
_C.trainer.max_epochs = 200 # Stop training once this number of epochs is reached.
_C.trainer.min_epochs = 100 # Force training for at least these many epochs
_C.trainer.max_steps = 999999999 # Stop training after this number of steps. Disabled by default (None).
_C.trainer.min_steps = 999999999 # Force training for at least these number of steps. Disabled by default (None).
_C.trainer.train_percent_check = 1.0 # How much of training dataset to check.
_C.trainer.val_percent_check = 1.0 # How much of validation dataset to check.
_C.trainer.test_percent_check = 1.0 # How much of test dataset to check.
_C.trainer.val_check_interval = 1.0 # How often within one training epoch to check the validation set
_C.trainer.log_save_interval = 100 # Writes logs to disk this often
_C.trainer.row_log_interval = 10 # How often to add logging rows (does not write to disk)
_C.trainer.distributed_backend = 'dp' # 'dp', 'ddp', 'ddp2', 'horovod'
_C.trainer.use_amp = False # will be removed, please use `precision` as below instead.
_C.trainer.amp_level = 'O1' # will be removed, please use `precision` as below instead.
_C.trainer.precision = 32 # Full precision (32), half precision (16).
_C.trainer.print_nan_grads = True # Prints gradients with nan values. will be removed
_C.trainer.weights_summary = '' # 'full', 'top', None.
_C.trainer.weights_save_path = '' # Where to save weights if specified. Will override default_root_dir for checkpoints only. 
                                  # Use this if for whatever reason you need the checkpoints stored in a different place 
                                  # than the logs written in `default_root_dir`.
_C.trainer.num_sanity_val_steps = 5 # Sanity check runs n batches of val before starting the training routine.
_C.trainer.truncated_bptt_steps = ''
_C.trainer.resume_from_checkpoint = ''
# _C.trainer.profiler = ''
_C.trainer.reload_dataloaders_every_epoch = False # Set to True to reload dataloaders every epoch
_C.trainer.auto_lr_find = False # If set to True, will `initially` run a learning rate finder,
                                # trying to optimize initial learning for faster convergence. Sets learning
                                # rate in self.hparams.lr | self.hparams.learning_rate in the lightning module.
                                # To use a different key, set a string instead of True with the key name.

_C.trainer.replace_sampler_ddp = True # Explicitly enables or disables sampler replacement. 
                                      # If not specified this will toggled automatically ddp is used

_C.trainer.benchmark = False # If true enables cudnn.benchmark.
_C.trainer.terminate_on_nan = False# If set to True, will terminate training (by raising a `ValueError`) at the
    # end of each training batch, if any of the parameters or the loss are NaN or +/-inf.

_C.trainer.auto_scale_batch_size = False # If set to True, will `initially` run a batch size
                                        # finder trying to find the largest batch size that fits into memory.
                                        # The result will be stored in self.hparams.batch_size in the LightningModule.
                                        # Additionally, can be set to either `power` that estimates the batch size through
                                        # a power search or `binsearch` that estimates the batch size through a binary search.

_C.trainer.logger = CN()
_C.trainer.logger.type = 'test_tube'
_C.trainer.logger.setting = 2 # 0: True  1: False  2: custom
_C.trainer.logger.mlflow = CN()
_C.trainer.logger.mlflow.experiment_name = 'torchline_logs'
_C.trainer.logger.mlflow.tracking_uri = _C.trainer.default_root_dir
_C.trainer.logger.test_tube = CN()
_C.trainer.logger.test_tube.name = 'torchline_logs'
_C.trainer.logger.test_tube.save_dir = _C.trainer.default_root_dir
_C.trainer.logger.test_tube.version = -1 #  # if <0, then use default version. Otherwise, it will restore the version.


# ---------------------------------------------------------------------------- #
# log
# ---------------------------------------------------------------------------- #

_C.log = CN()
_C.log.path = ''
_C.log.name = 'log.txt'

# ---------------------------------------------------------------------------- #
# Misc 
# ---------------------------------------------------------------------------- #

_C.SEED = random.randint(0, 10000)
_C.DEFAULT_CUDNN_BENCHMARK = True

_C.topk = [1, 3] # save the top k results., e.g. acc@1 and acc@3

_C.predict_only = CN()
_C.predict_only.type = 'ckpt'
_C.predict_only.to_pred_file_path = '' # specify the path of images

_C.predict_only.load_ckpt = CN() # load from checkpoint
_C.predict_only.load_ckpt.checkpoint_path = '' # load_from_checkpoint

_C.predict_only.load_metric = CN()
_C.predict_only.load_metric.weights_path = '' # load_from_metrics
_C.predict_only.load_metric.tags_csv = ''
_C.predict_only.load_metric.on_gpu = True
_C.predict_only.load_metric.map_location = 'cuda:0'

