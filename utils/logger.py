import re

def filter_logs(full_logs: str) -> str:
    pattern = re.compile(r'iteration: \d+ / \d+')
    full_logs_lines = full_logs.split('\n')
    matched_lines = [line for line in full_logs_lines if pattern.search(line)]
    return '\n'.join(matched_lines)

def parse_logs(logs: str) -> list[dict[str,]]:
    return [parse_single_log(log) for log in logs.split('\n') if log.strip()]

def parse_single_log(log: str) -> dict[str,]:
    iteration_re = re.compile(r'iteration: \d+ / \d+')
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    kv_pattern = re.compile(r'(\S+?) : ([-+]?\d*\.\d+|\d+)')
    
    # clean ANSI escape sequences
    clean_line = ansi_escape.sub('', log)
    
    # extract str after 'iteration:'
    iteration_match = iteration_re.search(clean_line)
    if not iteration_match:
        raise ValueError(f"No iteration found in {log}")
    metrics_str = log.partition(iteration_match.group(0))[-1]
    
    # extract all key-value pairs
    metrics = {}
    for match in kv_pattern.finditer(metrics_str):
        key = match.group(1).strip()
        value = match.group(2)
        
        try:
            value = int(value)
        except ValueError:
            value = float(value)
            
        metrics[key] = value
    return {
        **metrics
    }

if __name__ == '__main__':
    import wandb
    from pathlib import Path
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument('--log_path', '-l', type=str, required=True, help='Path to the log file')
    parser.add_argument('--project', '-p', type=str, default='huawei_test')
    args = parser.parse_args()
    
    log_path = Path(args.log_path)
    with open(log_path, 'r') as f:
        logs = f.read()
        
    filtered_logs = filter_logs(logs)
    print(filtered_logs)
    
    parsed_logs = parse_logs(filtered_logs)
    print(parsed_logs)
    
    wandb.init(project=args.project, name=log_path.stem)
    for log in parsed_logs:
        wandb.log(log)
    wandb.finish()
        