# SubHunt

SubHunt is a powerful subdomain enumeration and status checking tool. It utilizes multiple sources to discover subdomains and categorizes them based on their HTTP status codes.

## Features

- Enumerates subdomains using Subfinder, Sublist3r, and Assetfinder.
- Categorizes subdomains based on HTTP status codes: 200, 301, 302, 403, and errors.
- Saves the results into specified output directory.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/SubHunt.git
    cd SubHunt
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure you have Subfinder and Assetfinder installed:

    - Install Subfinder:

        ```bash
        go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
        ```

    - Install Assetfinder:

        ```bash
        go install github.com/tomnomnom/assetfinder@latest
        ```

## Usage

Run SubHunt with the desired domain and output directory:

```bash
python subhunt.py -d domain.com -o /path/to/output
Command-line Options
-d, --domain : The domain to scan for subdomains (required).
-o, --output : The output directory to save the results (required).
Example
bash

python subhunt.py -d example.com -o /home/user/Desktop/results
Output
The results will be saved in the specified output directory with the following files:

status_200_301_302.txt : Subdomains returning HTTP status 200, 301, or 302.
status_403.txt : Subdomains returning HTTP status 403.
status_error.txt : Subdomains that resulted in an error or timeout.
