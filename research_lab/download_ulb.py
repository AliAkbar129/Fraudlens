import argparse,hashlib
from pathlib import Path
import httpx
p=argparse.ArgumentParser();p.add_argument('--output',default='data/ulb');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
path=out/'creditcard.arff'
if not path.exists():
    with httpx.stream('GET','https://openml.org/data/v1/download/1673544/creditcard.arff',follow_redirects=True,timeout=120) as response:
        response.raise_for_status()
        with path.with_suffix('.partial').open('wb') as f:
            for chunk in response.iter_bytes():f.write(chunk)
    path.with_suffix('.partial').replace(path)
with path.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
if digest!='fdaf12730dc1fc426f318b71349f24f5c5fd00aa1152940be7e7509ae3d89d2a':raise ValueError('Dataset checksum mismatch')
print('Verified OpenML 1597',digest)
