"""news-23 b70 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
Verifies the source PNG first (signature, IHDR 1024x1024, IEND trailer, size cap),
then copies byte-for-byte and re-reads the output to confirm it matches.
"""
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(HERE)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo: " + out_dir)
    if not os.path.isfile(SRC):
        return fail("missing source entry.png next to main.py")
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        return fail("entry.png is %d bytes, over the 1 MiB cap" % len(data))
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("entry.png is not a PNG file")
    if len(data) < 33 or data[12:16] != b"IHDR":
        return fail("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    bit_depth, color_type = data[24], data[25]
    if (width, height) != (1024, 1024):
        return fail("entry.png is %dx%d, expected 1024x1024" % (width, height))
    if bit_depth != 8 or color_type not in (2, 6):
        return fail("unexpected PNG bit depth %d / colour type %d" % (bit_depth, color_type))
    if len(data) < 12 or data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        return fail("entry.png has a malformed IEND trailer")
    print("source verified: %d bytes, 1024x1024, bit depth %d, colour type %d"
          % (len(data), bit_depth, color_type))
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        return fail("output does not match source byte-for-byte")
    print("wrote %s (%d bytes, 1024x1024, sha256 %s)"
          % (dst, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
