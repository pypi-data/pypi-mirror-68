import sys
import pdb

print("Number of arguments: ", len(sys.argv))
print("The arguments are: ", str(sys.argv))
# import matplotlib.pyplot as plt
print("Number of arguments after import: ", len(sys.argv))
print("The arguments after import are: ", str(sys.argv))
import argparse
parser = argparse.ArgumentParser(description="Train baseline DDQN")
parser.add_argument("--name",
                    help="Name given to your model.")
args = parser.parse_args()
print("args.name: {}".format(args.name))

# from l2rpn_baselines import utils
#
#
# if __name__ == "__main__":
#     print("Number of arguments: ", len(sys.argv))
#     print("The arguments are: ", str(sys.argv))
#     import argparse
#     parser = argparse.ArgumentParser(description="Train baseline DDQN")
#     parser.add_argument("--name",
#                         help="Name given to your model.")
#     args = parser.parse_args()
#     print("args.name: {}".format(args.name))