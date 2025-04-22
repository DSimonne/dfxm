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

def rocking_curve_plot(
    path_to_hdf5,
    magnification,
    figsize=(10, 7),
    scale_dict={
        'Amplitude' : LogNorm(),
        "Background" : Normalize(),
        "Correlation" : Normalize(),
        "FWHM first motor" : Normalize(),
        'FWHM second motor' : Normalize(),
        "Peak position first motor" : Normalize(),
        "Peak position second motor" : Normalize(),
        "Residuals" : Normalize(),
    },
    cmap="jet",
    fontsize=12,
    pixel_size_10X=False,
    zoom=[None, None, None, None],
):
    """
    Plot the output of the `darfix` workflow for a strain scan (i.e., a mu/obpitch scan).
    
    This function reads an HDF5 file containing results from a mosaicity scan,
    extracts relevant data, and generates multiple plots to visualize mosaicity,
    orientation distribution, and motor scan results.

    Parameters
    ----------
    path_to_hdf5 : str
        Path to the HDF5 file containing the mosaicity scan results.
    magnification : str
        Magnification level used in the experiment ('2X' or other values).
    figsize : tuple of int, optional
        Figure size for the plot, default is (10, 12).
    cmap : str, optional
        Colormap used for motor scan result plots, default is 'jet'.
    fontsize : int, optional
        Font size for plot labels and titles, default is 12.
    pixel_size_10X : float or bool, optional
        Pixel size for the 10X magnification. If False, real-space extent is not defined.
        Default is False.
    zoom : x_min, x_max, y_min, y_max

    Returns
    -------
    None
        The function saves generated plots as PNG files in the same directory
        as the input HDF5 file and displays them.
    
    Notes
    -----
    - The function extracts the rocking curve fitting results.
    - It visualizes the extracted data using `matplotlib`.
    """
  
    # Load data from hdf5 result file
    motor_dict = {}
    with h5py.File(path_to_hdf5, "r") as f:
        print("Opening", path_to_hdf5)
        
        # Get fitting results
        result_dict = {
            'Amplitude' : f['entry']['Amplitude']["Amplitude"][...],
            "Background" : f['entry']['Background']["Background"][...],
            "Correlation" : f['entry']['Correlation']["Correlation"][...],
            "FWHM first motor" : f['entry']['FWHM first motor']["FWHM first motor"][...],
            'FWHM second motor' : f['entry']['FWHM second motor']['FWHM second motor'][...],
            "Peak position first motor" : f['entry']['Peak position first motor']["Peak position first motor"][...],
            "Peak position second motor" : f['entry']['Peak position second motor']["Peak position second motor"][...],
            "Residuals" : f['entry']['Residuals']["Residuals"][...],
        }
        print("\tLoaded rocking curves fitting results.") 

    # Create figure for the mosaicity
    fig, axes = plt.subplots(4, 2, figsize=figsize, sharex=True, sharey=True)

    # Define extent in real space
    if isinstance(pixel_size_10X, (int, float)):
        nx, ny = result_dict["Amplitude"][zoom[0]:zoom[1], zoom[2]:zoom[3]].shape[:2]
        if magnification == "2X":
            real_space_extent = [0, nx * pixel_size_10X*1e-3, 0, ny * pixel_size_10X*1e-3]
        elif magnification == "2X":
            pixel_size_2X = 5 * pixel_size_10X # nm
            real_space_extent = [0, nx * pixel_size_2X*1e-3, 0, ny * pixel_size_2X*1e-3]
            
        kwargs = {"extent": real_space_extent}
        y_label = "y (um)"
        x_label = "x (um)"
    else:
        kwargs = dict()
        y_label = "y (pixel)"
        x_label = "x (pixel)"
 
    for j, (key, values) in enumerate(tqdm(result_dict.items())):
        ax = axes.ravel()[j]
        image = ax.imshow(
            values[zoom[2]:zoom[3], zoom[0]:zoom[1]],
            norm=scale_dict[key],
            cmap=cmap,
            origin="lower",
            aspect='equal',
            **kwargs
        )
        ax.set_title(key, fontsize=fontsize + 2)
        ax.set_ylabel(y_label, fontsize=fontsize) # change here
        ax.set_xlabel(x_label, fontsize=fontsize)
        cbar_ax = make_axes_locatable(ax).append_axes(
            position='right', size='5%', pad=0.1)
        fig.colorbar(mappable=image, cax=cbar_ax)
    
    # Show final figure
    plt.tight_layout()
    save_path = os.path.join(os.path.dirname(path_to_hdf5), "rocking_curves.pdf")
    plt.savefig(save_path)
    plt.show()
    print("Saved as:", save_path)     
    
    
def grain_plot(
    path_to_hdf5,
    magnification,
    figsize_mosaicity=(12, 5),
    figsize_motors=(10, 7),
    cmap_motors="jet",
    fontsize=12,
    pixel_size_10X=False,
):
    """
    Plot the output of the `darfix` workflow for a mosaicity scan (i.e., a mu/chi scan).
    
    This function reads an HDF5 file containing results from a mosaicity scan,
    extracts relevant data, and generates multiple plots to visualize mosaicity,
    orientation distribution, and motor scan results.

    Parameters
    ----------
    path_to_hdf5 : str
        Path to the HDF5 file containing the mosaicity scan results.
    magnification : str
        Magnification level used in the experiment ('2X' or other values).
    figsize_mosaicity : tuple of int, optional
        Figure size for the mosaicity plot, default is (12, 5).
    figsize_motors : tuple of int, optional
        Figure size for motor scan result plots, default is (10, 7).
    cmap_motors : str, optional
        Colormap used for motor scan result plots, default is 'jet'.
    fontsize : int, optional
        Font size for plot labels and titles, default is 12.
    pixel_size_10X : float or bool, optional
        Pixel size for the 10X magnification. If False, real-space extent is not defined.
        Default is False.

    Returns
    -------
    None
        The function saves generated plots as PNG files in the same directory
        as the input HDF5 file and displays them.
    
    Notes
    -----
    - The function extracts mosaicity data, orientation distribution, and motor scan results.
    - It visualizes the extracted data using `matplotlib`.
    - Results for motors (center of mass, FWHM, kurtosis, skewness) are plotted separately.
    
    """
  
    # Load data from hdf5 result file
    motor_dict = {}
    with h5py.File(path_to_hdf5, "r") as f:
        print("Opening", path_to_hdf5)
        # Get mosaicity
        mosaicity_data = f['entry']['Mosaicity']['Mosaicity'][...]
        print("\tLoaded mosaicity results.") 
    
        orientation_data = f['entry']['Orientation distribution']['key']["data"][...]
        orientation_image = f['entry']['Orientation distribution']['key']["image"][...]
        orientation_origin = f['entry']['Orientation distribution']['key']["origin"][...]
        orientation_scale = f['entry']['Orientation distribution']['key']["scale"][...]
        orientation_x_label = f['entry']['Orientation distribution']['key']["xlabel"][...]
        orientation_y_label = f['entry']['Orientation distribution']['key']["ylabel"][...]
        motor_list=[orientation_x_label.item().decode(), orientation_y_label.item().decode()]
    
        print("\tLoaded orientation distribution.") 

        # Get results for each motor is motor_list
        for motor in motor_list:
            motor_dict[motor] = {
                "CenterOfMass": f['entry'][motor]["Center of mass"]["Center of mass"][...],
                "FWHM": f['entry'][motor]["FWHM"]["FWHM"][...],
                "Kurtosis": f['entry'][motor]["Kurtosis"]["Kurtosis"][...],
                "Skewness": f['entry'][motor]["Skewness"]["Skewness"][...],
            }
            print("\tLoaded results for motor", motor) 

    # Create figure for the mosaicity
    fig, axes = plt.subplots(1, 2, figsize=figsize_mosaicity)

    # Define extent in real space
    if isinstance(pixel_size_10X, (int, float)):
        nx, ny = mosaicity_data.shape[:2]
        if magnification == "2X":
            mosaicity_extent = [0, nx * pixel_size_10X*1e-3, 0, ny * pixel_size_10X*1e-3]
        else:
            pixel_size_2X = 5 * pixel_size_10X # nm
            mosaicity_extent = [0, nx * pixel_size_2X*1e-3, 0, ny * pixel_size_2X*1e-3]
    else:
        mosaicity_extent=None

    # Mosaicity Image
    mosaicity_image = axes[0].imshow(
        mosaicity_data,
        origin="lower",
        aspect='auto',
        extent=mosaicity_extent
    )
    axes[0].set_title("Mosaicity", fontsize=fontsize + 2)
    axes[0].set_ylabel("y (um)", fontsize=fontsize)
    axes[0].set_xlabel("x (um)", fontsize=fontsize)
        
    # Extent in angular space
    orientation_extent = [
        orientation_origin[0], 
        orientation_origin[0] + orientation_scale[0]* orientation_image.shape[1],
        orientation_origin[1], 
        orientation_origin[1] + orientation_scale[1]* orientation_image.shape[0],
    ]
    
    # Orientation image
    orientation_img = axes[1].imshow(
        orientation_image,
        origin="lower",
        aspect='equal',
        extent=orientation_extent,
    )
    
    axes[1].set_title("Orientation distribution", fontsize=fontsize + 2)
    axes[1].set_xlabel(motor_list[0] + " (°)", fontsize=fontsize)
    axes[1].set_ylabel(motor_list[0] + " (°)", fontsize=fontsize)

    plt.tight_layout()
    save_path = os.path.join(os.path.dirname(path_to_hdf5), "grain_plot_mosaicity.pdf")
    plt.savefig(save_path)
    plt.show()
    print("Saved as:", save_path)     
        
    # Plot motor results data
    for motor in motor_list:
        
        # Create figure
        fig, axes = plt.subplots(2, 2, figsize=figsize_motors, sharex=True)
        
        # COM
        img_0 = axes[0, 0].imshow(
            motor_dict[motor]["CenterOfMass"],
            norm=LogNorm(),
            cmap=cmap_motors,
            origin="lower",
            aspect='auto',
            extent=mosaicity_extent,
        )
        axes[0, 0].set_title("Center of mass", fontsize=fontsize + 2)
        axes[0, 0].set_ylabel("y", fontsize=fontsize)
        cbar_ax = make_axes_locatable(axes[0, 0]).append_axes(
            position='right', size='5%', pad=0.1)
        fig.colorbar(mappable=img_0, cax=cbar_ax)

        # FWHM
        img_0 = axes[0, 1].imshow(
            motor_dict[motor]["FWHM"],
            norm=LogNorm(),
            cmap=cmap_motors,
            origin="lower",
            aspect='auto',
            extent=mosaicity_extent,
        )
        axes[0, 1].set_title("FWHM", fontsize=fontsize + 2)
        axes[0, 1].set_ylabel("y", fontsize=fontsize)
        cbar_ax = make_axes_locatable(axes[0, 1]).append_axes(
            position='right', size='5%', pad=0.1)
        fig.colorbar(mappable=img_0, cax=cbar_ax)
        
        # Kurtosis
        img_0 = axes[1, 0].imshow(
            motor_dict[motor]["Kurtosis"],
            norm=LogNorm(),
            cmap=cmap_motors,
            origin="lower",
            aspect='auto',
            extent=mosaicity_extent,
        )
        axes[1, 0].set_title("Kurtosis", fontsize=fontsize + 2)
        axes[1, 0].set_xlabel("x", fontsize=fontsize)
        cbar_ax = make_axes_locatable(axes[1, 0]).append_axes(
            position='right', size='5%', pad=0.1)
        fig.colorbar(mappable=img_0, cax=cbar_ax)
        
        # Skewness
        img_0 = axes[1, 1].imshow(
            motor_dict[motor]["Skewness"],
            norm=LogNorm(),
            cmap=cmap_motors,
            origin="lower",
            aspect='auto',
            extent=mosaicity_extent,
        )
        axes[1, 1].set_title("Skewness", fontsize=fontsize + 2)
        axes[1, 1].set_xlabel("x", fontsize=fontsize)
        cbar_ax = make_axes_locatable(axes[1, 1]).append_axes(
            position='right', size='5%', pad=0.1)
        fig.colorbar(mappable=img_0, cax=cbar_ax)

        # Show figure
        plt.tight_layout()
        save_path = os.path.join(os.path.dirname(path_to_hdf5), f"grain_plot_{motor}.pdf")
        plt.savefig(save_path)
        plt.show()
        print("Saved as:", save_path) 