# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_utils.convertion.ipynb (unless otherwise specified).

__all__ = ['generate_prediction', 'convert_to_pc', 'convert_stereo_to_pc']

# Cell
#skip

import sys
sys.path.append("../../lib/pslidar2/")

from src import main
from src.preprocess import generate_lidar_from_depth

# Cell
def generate_prediction(datapath, save_path, data_list, data_tag, split_train, split_val, pretrain, resume = None):
    # Set so the Pseudo-Lidar lib can use them
    args = main.Args
    args.datapath = datapath
    args.save_path = save_path
    args.data_list = data_list
    args.generate_depth_map = True
    args.data_tag = data_tag
    args.split_train = split_train
    args.split_val = split_val
    args.pretrain = pretrain
    args.resume = resume
    main.main(args)

# Cell
def convert_to_pc(calib_dir, depth_dir, save_dir):
    args = generate_lidar_from_depth.Args()
    args.calib_dir = calib_dir
    args.depth_dir = depth_dir
    args.save_dir = save_dir
    generate_lidar_from_depth.main(args)

# Cell
def convert_stereo_to_pc(data_dir, pretrain):
    # make dirs
    split_train = data_dir + 'train.txt'
    split_val = data_dir + 'subval.txt'
    train_data_list = '/home/qhs67/git/bachelorthesis_sven_thaele/code/lib/pslidar2/split/trainval.txt'
    test_data_list = '/home/qhs67/git/bachelorthesis_sven_thaele/code/lib/pslidar2/split/test.txt'

    training_source_dir = data_dir + '/training'
    testing_source_dir = data_dir + '/testing'

    training_depth_dir = training_source_dir + '/depth_maps/depth_maps/trainval'
    testing_depth_dir = testing_source_dir + '/depth_maps/depth_maps/test'

    training_calib_dir = training_source_dir + '/calib'
    testing_calib_dir = testing_source_dir + '/calib'
    training_velodyne_dir = training_source_dir + '/pseudo_lidar'
    testing_velodyne_dir = testing_source_dir + '/pseudo_lidar'

    # training set
    #generate_prediction(training_source_dir, training_depth_dir, train_data_list, "trainval", split_train, split_val, pretrain)
    convert_to_pc(training_calib_dir, training_depth_dir, training_velodyne_dir)

    # testing set
    #generate_prediction(testing_source_dir, testing_depth_dir, test_data_list, 'test', split_train, split_val, pretrain)
    convert_to_pc(testing_calib_dir, testing_depth_dir, testing_velodyne_dir)