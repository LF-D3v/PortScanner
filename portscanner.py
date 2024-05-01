from rich.console import Console  # for colorful output
from multiprocessing.pool import ThreadPool  # for parallel execution
import json  # for json file handling
import socket  # for net communication (to connect to host & scan ports)
import sys  # for system-related functs 
import os  # to count the number of cpus to work with

console = Console()  # Creating a Console instance for colorful output

# Main class for port scanning
class Main:
    
    
#########################################################################################
#########################################################################################



    # JSON file containing ports to scan
    PORTS = "ports/common_ports.json"  # Path to the JSON file containing common ports to scan
    
    
    def __init__(self):
        self.hostname = ""  # Initializing hostname as empty string
        self.open_ports = []  # List to store open ports found during scanning



    # Method to load ports information from the JSON file
    # If modified, it could also include port description.
    def ports_to_scan(self):
        with open(main.PORTS, "r") as file:  
            data = json.load(file)  
            
        # Create a dictionary 
        self.ports_info = {int(port_number): data[port_number] for port_number in data}



#########################################################################################
#########################################################################################



     # Method to perform port scanning
    def scan(self):
        cpus = os.cpu_count()  # Get number of CPU cores
        console.print("\n[bold yellow]Scanning...[/bold yellow]\n")  
        
        # Create a ThreadPool with number of threads equal to number of CPU cores
        with ThreadPool(cpus) as operation:
            # Iterate over each port in the ports_info dictionary and scan it in parallel
            for i, _ in enumerate(
                operation.imap(self.scan_single_port, self.ports_info.keys()), 1
            ):
                progress_bar(i, len(self.ports_info))  
                
        print("\n")  
        self.finish_message()         
    
    

    # Method to scan a single port
    def scan_single_port(self, port):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        connection.settimeout(1)  
        
        # Attempt to establish a connection with the target on the specified port
        connection_status = connection.connect_ex((self.hostname, port))
        if connection_status == 0:  # If connection is successful (port is open)
            self.open_ports.append(port)  # Add the open port to the list
            
        connection.close()  # Close the socket connection



    # Method to display final message after scanning
    def finish_message(self):
        if self.open_ports:  # If there is at least 1 open port found
            console.print("{:<10}".format("[bold yellow]PORT[/bold yellow]"))  
            
            # Print each open port along with its status
            for port in self.open_ports:
                console.print("{:<10}".format(f"[green]{str(port)} (OPEN)[/green]"))
                
        else:  
            console.print("[bold red]No open ports.[/bold red]") 
            
        print("")
     



    # Static method to resolve hostname to IP address
    @staticmethod
    def resolve_hostname(target):
        try:
            ipv4 = socket.gethostbyname(target)  # Resolve hostname to IPv4 address
        except socket.gaierror as errorID: 
            console.print(f"[bold red]{errorID}. Exiting program.[/bold red]")  
            sys.exit() 
            
        console.print(f"[bold blue]IP: [/bold blue]{ipv4}")  
        return ipv4 



    # Print logo
    @staticmethod
    def logo():
        console.print(
            """
            [bold blue]
            _____                   _        _____                                              
            |  __ \                 | |      / ____|                                             
            | |__) |   ___    _ __  | |_    | (___     ___    __ _   _ __    _ __     ___   _ __ 
            |  ___/   / _ \  | '__| | __|    \___ \   / __|  / _` | | '_ \  | '_ \   / _ \ | '__|
            | |      | (_) | | |    | |_     ____) | | (__  | (_| | | | | | | | | | |  __/ | |   
            |_|       \___/  |_|     \__|   |_____/   \___|  \__,_| |_| |_| |_| |_|  \___| |_|   
                                                                                                
                                       By LF-D3v  
                                https://github.com/LF-D3v                                                                             
            [/bold blue]
            """
        ) 
        
        
    # Method to start the program
    def start_program(self):
        self.logo()  # Print logo
        self.ports_to_scan()  # Load ports information from JSON file
        
        try:
            target = console.input("[bold blue]Insert hostname or IP: ") 
        except KeyboardInterrupt:  # Handle keyboard interrupt (Ctrl+C)
            console.print(f"[bold red]\nExiting.[/bold red]") 
            sys.exit()  
            
        self.hostname = self.resolve_hostname(target)  # Resolve hostname to IP address
        
        self.scan()  # Start port scanning               
        
        
        
# Function to display progress bar
def progress_bar(index, indexTotal):
    length = 50 
    current_length = length * index // indexTotal 
    symbol = "+" * current_length + "-" * (length - current_length)  
    
    progress = "%.1f" % (index / indexTotal * 100)  
    
    console.print(f"[bold red]<[bold yellow]{symbol}[bold red]> [bold blue]({progress}%)[/bold blue]", end="\r")  # Print progress bar



# Entry point of the program
if __name__ == "__main__":
    main = Main()  # Create an instance of Main class
    main.start_program()  # Start the program
