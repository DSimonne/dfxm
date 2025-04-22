import os
import sys
from ewoks import execute_graph

def main(
    hdf5_file, 
    graph, 
):
    """Execute the Darfix workflow using Ewoks."""
    output_dir = os.path.dirname(hdf5_file)

    results = execute_graph(
        graph,
        inputs=[
            {
                "name": "raw_input_file",
                "value": hdf5_file,
            },
            {
                "name": "raw_detector_data_path",
                "value": "/entry_0000/measurement/pco_ff",
            },
            {
                "name": "raw_positioners_group_path", 
                "value": "/entry_0000/instrument/positioners"},
            {
                "name": "in_memory",
                "value": True,
            },
            {
                "name": "treated_data_dir",
                "value": output_dir,
            },
        ],
        output_tasks=True,
    )
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python RunDarfixWorkflow.py <hdf5_file> <graph>")
        sys.exit(1)
    else:
        _, hdf5_file, graph = sys.argv
        main(hdf5_file, graph)
