import os
import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import matplotlib.patches as patches
from h5glance import H5Glance
import glob
from tqdm import tqdm

def compute_pixel_size(scan):
    """
    Depends on your energy and motor positions. 
    When we operate at 17, in 10x farfield, we usually have a pixel size of around 38 nm. 

    If you do no have any magnification scan, you can compute the pixel size,
    the magnification is m=d1/d2. d1 is the sample to lens distance, d2 is the lens
    to detector distance.
    
    The horizontal distance between the sample and the detector is `mainx`, 
    the distance between the sample and the objective is `obx`, the height of 
    the objextive is `obz3+obz`, the height of the detector is `ffz`. 
    The nominal pixel size for 20x objective in ff detector is 0.65 um (x5 for 2x objective). 
    Your effective pixel size is then 0.65/m.
    """
    
    with h5py.File(scan) as f:
        positioners = f["entry_0000"]["instrument"]["positioners"]

        horizontal_distance_sample_detector = abs(positioners["mainx"][...]) # mm
        horizontal_distance_sample_objective = positioners["obx"][...] # mm
        # objective_height = positioners["obz3"][...][0] + positioners["obz"][...][0] # mm
        detector_height = positioners["ffz"][...][0] # mm
        two_theta = positioners["obpitch"][...][0] # degrees
        print("Detector and lens positions:")
        print(f"\tHorizontal distance sample objective: {horizontal_distance_sample_objective:.3f} mm.")
        print(f"\tHorizontal distance sample detector: {horizontal_distance_sample_detector:.3f} mm.")
        print(f"\tDetector height: {detector_height:.3f} mm.")
        print(f"\tTwo theta: {two_theta:.3f} deg.")
    
    d1 = horizontal_distance_sample_objective / np.cos(np.deg2rad(two_theta)) # mm
    d2 = (horizontal_distance_sample_detector / np.cos(np.deg2rad(two_theta))) - d1 # mm
    magnification = d2 / d1 # no unit
    
    print("\nComputed distances in scattered beam direction:")
    print(f"\tDistance sample objective (d1): {d1:.3f} mm.")
    print(f"\tDistance sample detector (d1+d2): {d1+d2:.3f} mm.")
    print(f"\tDistance objective detector (d2): {d2:.3f} mm.")
    print(f"\tMagnification (d1/d2): {magnification:.3f}.")
    
    nominal_pixel_size = 650 # nm
    effective_pixel_size = nominal_pixel_size / magnification # um
    
    print(f"\nEffective pixel size: {effective_pixel_size:.3f} nm (10X objective)")
    print(f"Effective pixel size: {effective_pixel_size*5:.3f} nm (2X objective).")

    return np.round(effective_pixel_size, 3)