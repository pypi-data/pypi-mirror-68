import argparse
import pickle
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from pysy.toolbox.utils import Yaml, create_all_parents
from sklearn.metrics import mean_squared_error, median_absolute_error, r2_score
from sklearn.model_selection import KFold, train_test_split
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, utils

from libnn.dataloader import Loader, ToTensor
from libnn.networks.resnets import *


class Splitter():
    """
    random_split for single train/test
    kfold_split for cross validation
    """
    def __init__(self):
        pass

    def __call__(
        self, 
        workspace, data_folder, cv, 
        test_scale, n_splits,
        ext = "pkl", shuffle = True
        ):
        np.random.seed(0)
        self.random_state = 42 # for randomly split
        self.workspace = workspace
        # dataset supposed to be under dir "workspace/data/":    
        files_to_split = self.workspace.joinpath(data_folder).glob(f"*.{ext}")
        if cv:
            print("k-fold spliting...")
        else:
            print("random spliting...")
        for count, p in enumerate(files_to_split):
            self.filename = p.stem
            # load dataset: {
            with open(p.as_posix(), 'rb') as f:
                ds = pickle.load(f)
            Xs = ds["Xs"]
            ys = ds["ys"]
            # }
            if cv:
                self.kfold_split(Xs, ys, n_splits, shuffle)
            else:
                self.random_split(Xs, ys, test_scale)
            print(f"{str(count).zfill(3)}, {self.filename} splitted...")

    def random_split(self, Xs, ys, test_scale):
        # state static randomly split each dataset into train and test: {
        X_train, X_test, y_train, y_test = train_test_split(
            Xs, ys, test_size = test_scale, 
            random_state = self.random_state
            )
        # }
        # save splited train/test sets: {
            # save dir: "workspace/train_test"
        trainset = {"Xs": X_train, "ys": y_train}
        testset = {"Xs": X_test, "ys": y_test}
        save_folder = self.workspace.joinpath("train_test")
        create_all_parents(save_folder, flag = "d")
        with open(save_folder.joinpath(f"{self.filename}_train.pkl"), "wb") as f:
            pickle.dump(trainset, f)
        with open(save_folder.joinpath(f"{self.filename}_test.pkl"), "wb") as f:
            pickle.dump(testset, f)
        # }

    def kfold_split(self, Xs, ys, n_splits, shuffle):
        # state static kfold split for cross validation: {
        kf = KFold(
            n_splits = n_splits, 
            shuffle = shuffle, 
            random_state = self.random_state
        )
        # }

        # save splited train/test sets: {
            # save dir: "workspace/cross_val"
        for count, (train_index, test_index) in enumerate(kf.split(Xs)):
            print(f"CV{str(count).zfill(3)} TRAIN indices: {train_index}, TEST indices: {test_index}")
            X_train, X_test = Xs[train_index], Xs[test_index]
            y_train, y_test = ys[train_index], ys[test_index]
            trainset = {"Xs": X_train, "ys": y_train}
            testset = {"Xs": X_test, "ys": y_test}
            save_folder = self.workspace.joinpath("cross_val")
            create_all_parents(save_folder, flag = "d")
            with open(save_folder.joinpath(f"{self.filename}_cv_{str(count).zfill(3)}_train.pkl"), "wb") as f:
                pickle.dump(trainset, f)
            with open(save_folder.joinpath(f"{self.filename}_cv_{str(count).zfill(3)}_test.pkl"), "wb") as f:
                pickle.dump(testset, f)
        # }

class Trainer():
    def __init__(
        self, 
        ResNet, n_channel, num_classes,
        device, EPOCH, BATCH_SIZE, 
        NUM_WORKERS, lr, decay,
        early_stop_epoch, mean_loss_threshold, std_loss_threshold
        ):
        # params setting: {
            # num_classes: NN prediction dim
            # EPOCH: times of dataset iteration
            # BATCH_SIZE: size of data loader batch
            # NUM_WORKERS: workers number for loading dataset
            # lr: learning rate
            # decay: learning decay rate 
            # device: cpu/cuda
        self.ResNet = ResNet
        self.n_channel = n_channel
        self.num_classes = num_classes
        self.device = device
        self.EPOCH = EPOCH
        self.BATCH_SIZE = BATCH_SIZE
        self.NUM_WORKERS = NUM_WORKERS
        self.lr = lr
        self.decay = decay
        self.early_stop_epoch = early_stop_epoch
        self.mean_loss_threshold = mean_loss_threshold
        self.std_loss_threshold =  std_loss_threshold
        # }

    def train(self, train_path):
        # define dataset, dataloader, loss function and initial net: {
        dataset = Loader(
            file_path = train_path.as_posix(),
            transform = transforms.Compose([ToTensor()])
        )

        dataloader = DataLoader(
            dataset, 
            batch_size = self.BATCH_SIZE, 
            shuffle = True, 
            num_workers = self.NUM_WORKERS
        )
        loss_F = torch.nn.MSELoss()
        # net = ResNet18(num_classes = num_classes).to(device)
        net = self.ResNet(self.n_channel, num_classes = self.num_classes).to(self.device)
        # }

        # epach training: {
            # variable learning rate, and optimizer
            # optimizer: Adam
        for epoch in range(self.EPOCH):
            optimizer = torch.optim.Adam(net.parameters(), lr = self.lr)
            # decay the learning rate every self.EPOCH/4 epoches
            # for a better local minimum
            if self.EPOCH > 4:
                if epoch % (self.EPOCH // 4) == 0 and epoch != 0:
                    self.lr *= self.decay   
            losses = []
            # # print epoch count
            # print(f'Epoch: {epoch + 1}')

            # training each batch: {
            for step, data in enumerate(dataloader, 0):
                # load a batch, assign Xs, ys to device (cpu/cuda): {
                Xs, ys = data # print(Xs.shape)
                Xs, ys = Xs.to(self.device), ys.to(self.device)
                # }
                # apply net and calculate loss: {
                preds = net(Xs)
                loss = loss_F(preds, ys)
                # }
                # clean optimizer grad and backpropagate for next step: {
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                # }
                losses.append(loss.item())
                # print loss of each 10 batches: 
                if step % 10 == 0:
                    # sys.stdout.write(f"step {step} loss: {np.round(loss.item(), 4)}\r")
                    print(f"step {step} loss: {np.round(loss.item(), 4)}\r")
            # }            
            print(f"Epoch: {epoch}, loss: {np.round(np.mean(losses), 4)}, std: {np.round(np.std(losses), 4)}")
            # Early stopping:
            if epoch >= self.early_stop_epoch \
                and np.mean(losses) < self.mean_loss_threshold \
                and np.std(losses) < self.std_loss_threshold:
                break
        # }
        return net        

    def test(self, net_params_path, test_path, callback, run_mode = "test"):
        net = self.ResNet(self.n_channel, self.num_classes)
        net.load_state_dict(torch.load(net_params_path))
        net.eval()
        if self.device.type == "cuda":
            net.cuda()
        pred_val = []
        true_val = []
        # define dataset, dataloader: {
        dataset = Loader(
            file_path = test_path.as_posix(),
            transform = transforms.Compose([ToTensor()])
        )

        dataloader = DataLoader(
            dataset, 
            batch_size = self.BATCH_SIZE,
            shuffle = False, 
            num_workers = self.NUM_WORKERS
        )
        # }

        # testing each batch: {
        for _, data in enumerate(dataloader, 0):
            # load a batch, assign Xs, ys to device (cpu/cuda): {
            Xs, ys = data
            # # use 80% data to prevent cuda out of memory
            # Xs = Xs[0: np.int(0.8 * Xs.shape[0]), :, :, :]
            # ys = ys[0: np.int(0.8 * ys.shape[0])]
            Xs, ys = Xs.to(self.device), ys.to(self.device)
            # }
            pred = net(Xs)
            pred_val.extend(pred.data.cpu().numpy())
            true_val.extend(ys.cpu().numpy())
        # }
        # call the post proc function, like Postproc.save_csv:
        callback(pred_val = pred_val, true_val = true_val, net_params_path = net_params_path, run_mode = run_mode)

class Postproc(object):
    def __init__(self):
        pass

    def save_csv(self, **kwargs):
        # load params: {
        pred_val = kwargs["pred_val"]
        true_val = kwargs["true_val"]
        path = kwargs["net_params_path"]
        run_mode = kwargs["run_mode"]
        # }

        # covert pred_val, true_val to 1d array, which can be compared in dataframe.
        # {
        if isinstance(pred_val, list):
            pred_val = np.array(pred_val)
        if isinstance(true_val, list):
            true_val = np.array(true_val)
        if pred_val.ndim > 1:
            pred_val = pred_val.ravel()
        if true_val.ndim > 1:
            true_val = true_val.ravel()
        # }
        
        # save to dataframe:{
        df = pd.DataFrame(list(zip(pred_val, true_val)), columns = ["pred", "ys"])
        # print(mean_squared_error(df["ys"].values, df["pred"].values))
        # print(median_absolute_error(df["ys"].values, df["pred"].values))
        # print(r2_score(df["ys"].values, df["pred"].values))
        if run_mode == "test":
            filename = path.stem.split("_net_params")[0] + "_test.csv"
        elif run_mode == "apply":
            filename = path.stem.split("_net_params")[0] + ".csv"
        else:
            filename = path.stem.split("_net_params")[0] + f"_{run_mode}.csv"
        df.to_csv(path.parent.joinpath(filename).as_posix())
        # }

class Dispatcher(Splitter, Trainer, Postproc):

    def __init__(
        self, run_mode,
        workspace, ResNet, device,
        n_channel, num_classes,  
        data_folder = "data", cv = False, test_scale = 0.3, n_splits = 3, 
        EPOCH = 100, BATCH_SIZE = 128, 
        NUM_WORKERS = 4, lr = 0.001, decay = 0.25,
        early_stop_epoch = 20, mean_loss_threshold = 0.001, std_loss_threshold =  0.0005
        ):

        if not isinstance(workspace, Path):
            workspace = Path(workspace)

        Trainer.__init__(
            self, 
            ResNet, n_channel, num_classes,
            device, EPOCH, BATCH_SIZE, 
            NUM_WORKERS, lr, decay,
            early_stop_epoch, mean_loss_threshold, std_loss_threshold            
        )
        Postproc.__init__(self)
        self.num_classes = num_classes
        self.n_channel = n_channel


        if run_mode == "t2":
            print("Enter train & test mode...")
            Splitter.__init__(self)
            Splitter.__call__(
                self,
                workspace, data_folder, cv, 
                test_scale, n_splits
            )

            print("training & testing...")
            if cv == True:
                data_folder = workspace.joinpath("cross_val")
            else:
                data_folder = workspace.joinpath("train_test")
            train_test_paths = zip(
                data_folder.glob(r"*train.pkl"),
                data_folder.glob(r"*test.pkl")
            )

            for count, (train_path, test_path) in enumerate(train_test_paths):
                name = train_path.stem.split("_train")[0]
                # init model save paths: {
                # # cannot load model directly which is an error of package pickle
                # save_model = data_folder.joinpath(f"{name_}net.pth") 
                net_params_path = data_folder.joinpath(f"{name}_net_params.pth")
                # }
                print("training...")
                print("-" * 40)
                net = self.train(train_path)
                # torch.save(net, save_model)
                torch.save(net.state_dict(), net_params_path)
                print(f"{train_path.stem} is trained...")

                print("testing...")
                print("-" * 40)
                self.test(net_params_path, test_path, self.save_csv)
                print(f"{test_path.stem} is tested...")

    # neural net application
    def __call__(self, data_folder):
        print("Enter model application mode...")
        print("-" * 40)        
        paths = zip(
            data_folder.glob(r"*.pkl"),
            data_folder.glob(r"*.pth")
        )
        for data_path, model_path in paths:
            self.test(model_path, data_path, self.save_csv, run_mode = "apply")
            print(f"apply model to {data_path.stem}...")   

def run(run_mode, config_file):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    config = Yaml(config_file).load()

    nn_dict = {
        "ResNet18": ResNet18,
        "ResNet34": ResNet34,
        "ResNet50": ResNet50,
        "ResNet101": ResNet101,
        "ResNet152": ResNet152
    }

    # parse arguments:{
    workspace = config["workspace"]
    ResNet = nn_dict[config["nn_name"]]
    n_channel = config["n_channel"]
    num_classes = config["num_classes"]
    data_folder = config["data_folder"]
    apply_data_folder = config["apply_data_folder"]
    cv = config["cv"]
    test_scale = config["test_scale"]
    n_splits = config["n_splits"]
    EPOCH = config["EPOCH"]
    BATCH_SIZE = config["BATCH_SIZE"]
    NUM_WORKERS = config["NUM_WORKERS"]
    lr = config["lr"]
    decay = config["decay"]
    early_stop_epoch = config["early_stop_epoch"]
    mean_loss_threshold = config["mean_loss_threshold"]
    std_loss_threshold = config["std_loss_threshold"]
    # }

    if not isinstance(workspace, Path):
        workspace = Path(workspace)

    disp = Dispatcher(
            run_mode, workspace, ResNet, device, n_channel, num_classes,  
            data_folder = data_folder, cv = cv, test_scale = test_scale, n_splits = n_splits, 
            EPOCH = EPOCH, BATCH_SIZE = BATCH_SIZE, 
            NUM_WORKERS = NUM_WORKERS, lr = lr, decay = decay,
            early_stop_epoch = early_stop_epoch, mean_loss_threshold = mean_loss_threshold, std_loss_threshold =  std_loss_threshold
        )

    if run_mode == "a":
        disp(workspace.joinpath(apply_data_folder))

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    parse = argparse.ArgumentParser()
    parse.add_argument("action", type = str, help = "run type, train and test (t2) or application (a)")
    parse.add_argument("--config", type = str, help = "position of yaml config file.", default = "config.yaml")
    args = parse.parse_args()
    config_file = args.config
    run_mode = args.action
    run(run_mode, config_file)
    # # example:
    # python dispatch.py t2 --c=example_net_config.yaml
