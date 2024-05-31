import argparse
import asyncio
import aiohttp
import subprocess
import os
import pyfiglet

async def run_command(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode().splitlines()

async def collect_subdomains(domain):
    subdomains = set()

    # Run Subfinder
    subfinder_command = f"subfinder -silent -d {domain}"
    subfinder_result = await run_command(subfinder_command)
    subdomains.update(subfinder_result)

    # Run Sublist3r
    sublist3r_command = f"sublist3r -d {domain} -o sublist3r.txt"
    await run_command(sublist3r_command)
    with open("sublist3r.txt", "r") as file:
        sublist3r_result = file.read().splitlines()
    subdomains.update(sublist3r_result)
    os.remove("sublist3r.txt")

    # Run Assetfinder
    assetfinder_command = f"assetfinder --subs-only {domain}"
    assetfinder_result = await run_command(assetfinder_command)
    subdomains.update(assetfinder_result)

    return subdomains

async def check_status(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return url, response.status
    except aiohttp.ClientError:
        return url, "error"
    except asyncio.TimeoutError:
        return url, "timeout"

async def main(domain):
    subdomains = await collect_subdomains(domain)
    results = []
    
    async with aiohttp.ClientSession() as session:
        tasks = [check_status(session, f"http://{subdomain}") for subdomain in subdomains]
        results = await asyncio.gather(*tasks)
    
    return results

def categorize_results(results):
    status_200_301_302 = []
    status_403 = []
    status_error = []
    
    for url, status in results:
        if status in [200, 301, 302]:
            status_200_301_302.append(url)
        elif status == 403:
            status_403.append(url)
        else:
            status_error.append(url)
    
    return status_200_301_302, status_403, status_error

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        for item in data:
            file.write(f"{item}\n")

def display_banner():
    banner = pyfiglet.figlet_format("Subdomain Finder")
    print(banner)

if __name__ == "__main__":
    display_banner()
    
    parser = argparse.ArgumentParser(description="Subdomain Enumerator and Status Checker")
    parser.add_argument('-d', '--domain', required=True, help="The domain to scan for subdomains")
    parser.add_argument('-o', '--output', required=True, help="The output directory to save the results")

    args = parser.parse_args()

    domain = args.domain
    output_dir = args.output

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(domain))
    
    status_200_301_302, status_403, status_error = categorize_results(results)
    
    write_to_file(os.path.join(output_dir, "status_200_301_302.txt"), status_200_301_302)
    write_to_file(os.path.join(output_dir, "status_403.txt"), status_403)
    write_to_file(os.path.join(output_dir, "status_error.txt"), status_error)
    
    print(f"Results written to files in {output_dir}:")
    print(" - status_200_301_302.txt")
    print(" - status_403.txt")
    print(" - status_error.txt")
import argparse
import asyncio
import aiohttp
import subprocess
import os
import pyfiglet

async def run_command(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode().splitlines()

async def collect_subdomains(domain):
    subdomains = set()

    # Run Subfinder
    subfinder_command = f"subfinder -silent -d {domain}"
    subfinder_result = await run_command(subfinder_command)
    subdomains.update(subfinder_result)

    # Run Sublist3r
    sublist3r_command = f"sublist3r -d {domain} -o sublist3r.txt"
    await run_command(sublist3r_command)
    with open("sublist3r.txt", "r") as file:
        sublist3r_result = file.read().splitlines()
    subdomains.update(sublist3r_result)
    os.remove("sublist3r.txt")

    # Run Assetfinder
    assetfinder_command = f"assetfinder --subs-only {domain}"
    assetfinder_result = await run_command(assetfinder_command)
    subdomains.update(assetfinder_result)

    return subdomains

async def check_status(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return url, response.status
    except aiohttp.ClientError:
        return url, "error"
    except asyncio.TimeoutError:
        return url, "timeout"

async def main(domain):
    subdomains = await collect_subdomains(domain)
    results = []
    
    async with aiohttp.ClientSession() as session:
        tasks = [check_status(session, f"http://{subdomain}") for subdomain in subdomains]
        results = await asyncio.gather(*tasks)
    
    return results

def categorize_results(results):
    status_200_301_302 = []
    status_403 = []
    status_error = []
    
    for url, status in results:
        if status in [200, 301, 302]:
            status_200_301_302.append(url)
        elif status == 403:
            status_403.append(url)
        else:
            status_error.append(url)
    
    return status_200_301_302, status_403, status_error

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        for item in data:
            file.write(f"{item}\n")

def display_banner():
    banner = pyfiglet.figlet_format("SubHunt")
    print(banner)

if __name__ == "__main__":
    display_banner()
    
    parser = argparse.ArgumentParser(description="Subdomain Enumerator and Status Checker")
    parser.add_argument('-d', '--domain', required=True, help="The domain to scan for subdomains")
    parser.add_argument('-o', '--output', required=True, help="The output directory to save the results")

    args = parser.parse_args()

    domain = args.domain
    output_dir = args.output

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(domain))
    
    status_200_301_302, status_403, status_error = categorize_results(results)
    
    write_to_file(os.path.join(output_dir, "status_200_301_302.txt"), status_200_301_302)
    write_to_file(os.path.join(output_dir, "status_403.txt"), status_403)
    write_to_file(os.path.join(output_dir, "status_error.txt"), status_error)
    
    print(f"Results written to files in {output_dir}:")
    print(" - status_200_301_302.txt")
    print(" - status_403.txt")
    print(" - status_error.txt")
