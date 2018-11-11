## TRAIN Model

import caffe


def Train(solver = "Data/solver.prototxt"):
    # Tell caffe to use cpu. switch to caffe.set_mode_gpu() to try using the gpu
    caffe.set_mode_cpu()


    # Load solver from file
    solver = caffe.get_solver(solver)
    #solver = caffe.restore("Data/snapshot-56_12_4_iter_10.solverstate")

    # Train a new model
    solver.solve();

if __name__ == "__main__":
    Train()