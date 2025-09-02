"""Load payloads from payload.txt"""
def load_payloads(path='payload.txt'):
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]
