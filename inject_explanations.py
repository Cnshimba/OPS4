import os
import re
import glob

# Maps a unique snippet of the code block to the explanation text
explanations = {
    # Week 3
    "ipaddr: 10.0.0.1": "A YAML configuration snippet defining the core network parameters and managed services (DHCP, TFTP, NFS) for the Warewulf controller.",
    "Only listen on the internal cluster interface": "Configuration file for `dnsmasq` that combines DNS, DHCP, and TFTP services, replacing Warewulf's system-managed services for simplicity.",
    "node add node01 --ipaddr=": "Registers a physical compute node to the cluster registry, explicitly binding its IP address to its hardware MAC address for stateless boot.",
    "profile add gpu-nodes": "Creates a new configuration profile tailored for GPU nodes and assigns a specific container image to this profile.",
    "profile set default --netmask": "Configures the default profile with a subnet mask. Because of inheritance, this netmask will automatically apply to all nodes in the cluster unless explicitly overridden.",
    "wwctl overlay list": "Lists all available overlays and displays the template structure used by Warewulf to generate the dynamic `/etc/hosts` file for compute nodes.",

    # Week 8
    "/home  10.0.0.0/24(rw,sync,no_root_squash)": "Configures an NFS export allowing the entire `10.0.0.0/24` subnet read-write access without root squashing, which is typical for HPC shared home directories.",

    # Week 6
    "int MPI_Send(void *buf": "C function signature for sending a message in MPI. It requires specifying the buffer, count, datatype, destination rank, message tag, and the communicator context.",
    "int MPI_Recv(void *buf": "C function signature for receiving a message in MPI. It blocks until a message matching the specified source rank and tag arrives.",
    "comm.send(obj, dest, tag=": "Python equivalent (mpi4py) for sending a Python object. Unlike C, it handles serialization (pickling) and datatypes automatically.",
    "data = comm.recv(source=MPI.ANY_SOURCE": "Python equivalent for receiving an object. Using `ANY_SOURCE` allows the program to accept a message from whichever rank sends it first.",
    "int MPI_Bcast(void *buffer": "C function signature for broadcasting data. The `root` argument defines which rank holds the original data that gets sent to everyone else.",
    "data = comm.bcast(data, root=0)": "Python syntax for a broadcast operation. The data variable on the root rank is distributed and returned on all other ranks.",
    "MPI_Bcast(&data, 1,": "A concrete C example of broadcasting an integer from rank 0 to all other processes in the communicator.",
    "data = {'key': 100}": "A Python example demonstrating that complex data structures like dictionaries can be directly broadcasted using mpi4py.",
    "int MPI_Scatter(void *sendbuf": "C function signature for scattering an array. It splits the `sendbuf` array from the root and distributes the chunks sequentially to all ranks.",
    "local_data = comm.scatter(sendbuf, root=0)": "Python syntax for scattering. The root rank provides a list, and each rank receives one element from that list as `local_data`.",
    "MPI_Scatter(global_data, 1, MPI_INT, &local_data": "A C example of scattering an array of four integers such that each of the four MPI ranks receives exactly one integer.",
    "if rank == 0:\n    data = [10, 20, 30, 40]": "Python scatter example where only rank 0 needs to define the full dataset. The other ranks can initialize their send buffer as `None`.",
    "int MPI_Gather(void *sendbuf": "C function signature for gathering data. It performs the inverse of scatter, collecting data chunks from all ranks into a single array on the root.",
    "all_data = comm.gather(local_data, root=0)": "Python syntax for gathering. Each rank contributes `local_data`, and rank 0 receives a complete list of all contributions.",
    "MPI_Gather(&local_result, 1, MPI_INT, global_results": "A C example demonstrating how to collect computed results from all ranks into a master array on rank 0.",
    "local_result = rank * 2\nall_data = comm.gather": "Python gather example. Each rank computes a unique value, which are then collected into a list on rank 0.",
    "int MPI_Reduce(void *sendbuf": "C function signature for a reduction operation. It collects data from all ranks and combines them using an operation (e.g., sum, max, min) on the root.",
    "global_result = comm.reduce(local_result, op=MPI.SUM": "Python syntax for reduction. It efficiently sums up the `local_result` from all ranks into a single variable on rank 0.",
    "MPI_Reduce(&local_sum, &global_sum, 1, MPI_INT": "A C example using `MPI_SUM` to add together local values from all ranks, placing the final total into `global_sum` on rank 0.",
    "local_sum = rank * 10\nglobal_sum = comm.reduce": "Python reduce example demonstrating how partial sums calculated by individual ranks are globally aggregated.",
    "module load openmpi5\n$ module load python": "Environment setup commands showing how to load the required software modules (MPI and Python) before running a parallel job.",
    "cblas_dgemm(CblasRowMajor": "An example of a highly optimized BLAS library call for matrix multiplication, which is orders of magnitude faster than a manual nested loop.",
    "// Each MPI rank defines its chunk": "Demonstrates parallel I/O using HDF5 hyperslabs, where multiple MPI ranks write concurrently to different regions of the same file without conflict.",
    "fftw_plan": "Demonstrates FFTW's plan creation, an optimization technique where the library measures system hardware characteristics to choose the fastest algorithmic execution path."
}

def main():
    for filepath in glob.glob('Week * - */Week_*_Student_Notes.html'):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split the document by </pre>
        parts = content.split('</pre>')
        if len(parts) == 1:
            continue
            
        new_content = parts[0]
        modified = False

        for i in range(len(parts) - 1):
            pre_block = parts[i]
            tail = parts[i+1]
            
            # Check if tail already starts with our explanation
            if tail.lstrip().startswith('<p class="text-sm text-slate-600'):
                new_content += '</pre>' + tail
                continue
                
            # If not, try to match the pre_block to our dictionary
            found_explanation = None
            for key, expl in explanations.items():
                if key in pre_block:
                    found_explanation = expl
                    break
            
            if found_explanation:
                explanation_html = f'\n<p class="text-sm text-slate-600 dark:text-slate-400 mt-2"><strong>Explanation:</strong> {found_explanation}</p>\n'
                new_content += '</pre>' + explanation_html + tail.lstrip('\n')
                modified = True
            else:
                new_content += '</pre>' + tail

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Injected explanations into {filepath}')

if __name__ == "__main__":
    main()
