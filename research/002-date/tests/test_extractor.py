import tempfile
from pathlib import Path
import unittest
import subprocess
import json
from extract_prefix import RECORD, extract

class ExtractionTests(unittest.TestCase):
    def test_packed_record_length(self):
        self.assertEqual(RECORD.size, 24)

    def test_sanitization_prefix_and_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            raw = folder/'data.bin'
            raw.write_bytes(b''.join(RECORD.pack(i, i + 100, 999, i + 1) for i in range(10)))
            compressed=folder/'data.bin.zst'
            with compressed.open('wb') as out:
                subprocess.run(['zstd','-q','-c',str(raw)], stdout=out, check=True)
            extracted=folder/'subset.bin'
            meta=extract(compressed.as_uri(),extracted,4)
            self.assertEqual(extracted.stat().st_size,96)
            self.assertEqual(meta['records'],4)
            for i in range(4):
                self.assertEqual(RECORD.unpack(extracted.read_bytes()[i*24:(i+1)*24]),(i,i+100,1,-2))
            self.assertEqual(meta['subset_sha256'],json.loads(extracted.with_suffix('.bin.manifest.json').read_text())['subset_sha256'])

    def test_short_source_is_rejected_and_no_partial_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            raw=folder/'raw'
            raw.write_bytes(RECORD.pack(0,1,1,-1))
            zipped=folder/'short.zst'
            with zipped.open('wb') as out:
                subprocess.run(['zstd','-q','-c',str(raw)], stdout=out, check=True)
            target=folder/'out.bin'
            with self.assertRaises(EOFError):
                extract(zipped.as_uri(),target,2)
            self.assertFalse(target.exists())

if __name__=='__main__':unittest.main()
