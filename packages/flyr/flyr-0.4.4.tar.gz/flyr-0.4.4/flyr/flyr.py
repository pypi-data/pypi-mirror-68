#!/usr/bin/env python3

# FIXME stop depending on PIL and nptyping

# Standard library imports
import os
from io import BytesIO, BufferedIOBase
from math import sqrt, exp
from typing import Dict, List, Optional, BinaryIO, Any, Tuple, Union

# Third party imports
import numpy as np
from nptyping import Array
from PIL import Image


# Constants
segment_sep = b"\xff"
app1_marker = b"\xe1"
magic_flir_def = b"FLIR\x00"

chunk_app1_bytes_count = len(app1_marker)
chunk_length_bytes_count = 2
chunk_magic_bytes_count = len(magic_flir_def)
chunk_skip_bytes_count = 1
chunk_num_bytes_count = 1
chunk_tot_bytes_count = 1
chunk_partial_metadata_length = (
    chunk_app1_bytes_count + chunk_length_bytes_count + chunk_magic_bytes_count
)
chunk_metadata_length = (
    chunk_partial_metadata_length
    + chunk_skip_bytes_count
    + chunk_num_bytes_count
    + chunk_tot_bytes_count
)


def unpack(path_or_stream: Union[str, BinaryIO]) -> Array[float, ..., ...]:
    if isinstance(path_or_stream, str) and os.path.isfile(path_or_stream):
        with open(path_or_stream, "rb") as flirh:
            return unpack(flirh)
    elif isinstance(path_or_stream, BufferedIOBase):
        stream = path_or_stream
        flir_app1_stream = extract_flir_app1(stream)
        flir_records = parse_flir_app1(flir_app1_stream)
        thermal = parse_thermal(flir_app1_stream, flir_records)
        return thermal
    else:
        raise ValueError("Incorrect input")  # TODO improved error message


def extract_flir_app1(stream: BinaryIO) -> BinaryIO:
    """ Extracts the FLIR APP1 bytes.
    
        Parameters
        ---------
        stream : BinaryIO
            A full bytes stream of a JPEG file, expected to be a FLIR file.
        
        Raises
        ------
        ValueError
            When the file is invalid in one the next ways, a 
            ValueError is thrown.
            
            * File is not a JPEG
            * A FLIR chunk number occurs more than once
            * The total chunks count is inconsistent over multiple chunks
            * No APP1 segments are successfully parsed
        
        Returns
        -------
        BinaryIO
            A bytes stream of the APP1 FLIR segments
    """
    # Check JPEG-ness
    magic_bytes = stream.read(2)
    if False:  # TODO check whether image is a correct jpeg
        raise ValueError("Invalid FLIR: given file is not a jpeg")

    chunks_count: Optional[int] = None
    chunks: Dict[int, bytes] = {}
    while True:
        b = stream.read(1)
        if not b == segment_sep:
            continue

        parsed_chunk = parse_flir_chunk(stream, chunks_count)
        if not parsed_chunk:
            continue

        chunks_count, chunk_num, chunk = parsed_chunk
        chunk_exists = chunks.get(chunk_num, None) is not None
        if chunk_exists:
            raise ValueError("Invalid FLIR: duplicate chunk number")
        chunks[chunk_num] = chunk

        # Encountered all chunks, break out of loop to process found metadata
        if chunk_num == chunks_count:
            break

    if chunks_count is None:
        raise ValueError("Invalid FLIR: no metadata encountered")

    flir_app1_bytes = b""
    for chunk_num in range(chunks_count + 1):
        flir_app1_bytes += chunks[chunk_num]

    flir_app1_stream = BytesIO(flir_app1_bytes)
    flir_app1_stream.seek(0)
    return flir_app1_stream


def parse_flir_chunk(
    stream: BinaryIO, chunks_count: Optional[int]
) -> Optional[Tuple[int, int, bytes]]:
    # Parse the chunk header. Headers are as follows (definition with example):
    #
    #     \xff\xe1<length: 2 bytes>FLIR\x00\x01<chunk nr: 1 byte><chunk count: 1 byte>
    #     \xff\xe1\xff\xfeFLIR\x00\x01\x01\x0b
    #
    # Meaning: Exif APP1, 65534 long, FLIR chunk 1 out of 12
    marker = stream.read(chunk_app1_bytes_count)
    length = int.from_bytes(stream.read(chunk_length_bytes_count), "big")
    length -= chunk_metadata_length
    magic_flir = stream.read(chunk_magic_bytes_count)

    if not (marker == app1_marker and magic_flir == magic_flir_def):
        # Seek back to just after byte b and continue searching for chunks
        stream.seek(-chunk_partial_metadata_length, 1)
        return None

    stream.seek(1, 1)  # skip 1 byte, unsure what it is for

    chunk_num = int.from_bytes(stream.read(chunk_num_bytes_count), "big")
    chunks_tot = int.from_bytes(stream.read(chunk_tot_bytes_count), "big")

    # Remember total chunks to verify metadata consistency
    if not chunks_count:
        chunks_count = chunks_tot

    if (  # Check whether chunk metadata is consistent
        not chunks_tot
        or chunk_num < 0
        or chunk_num > chunks_tot
        or chunks_tot != chunks_count
    ):
        raise ValueError("Invalid FLIR: inconsistent total chunks")

    # FIXME There is  calculation error somewhere which causes length to be
    #       1 too small. So far it manually adding 1 seems sufficient to
    #       correct for it, but it's not the right way.
    #       Fix by figuring out what causes the off by 1 error.
    return chunks_tot, chunk_num, stream.read(length + 1)


def parse_thermal(
    stream: BinaryIO, records: Dict[int, Tuple[int, int, int, int]]
) -> Array[float, ..., ...]:
    # FIXME Support formats other than subtype == PNG
    RECORD_IDX_RAW_DATA = 1
    RECORD_IDX_CAMERA_INFO = 32

    raw_data_md = records[RECORD_IDX_RAW_DATA]
    camera_info_md = records[RECORD_IDX_CAMERA_INFO]
    width, height, raw_data = parse_raw_data(stream, raw_data_md)
    camera_info = parse_camera_info(stream, camera_info_md)

    return raw2temp(raw_data, **camera_info)


def parse_flir_app1(stream: BinaryIO) -> Dict[int, Tuple[int, int, int, int]]:
    # 0x00 - string[4] file format ID = "FFF\0"
    # 0x04 - string[16] file creator: seen "\0","MTX IR\0","CAMCTRL\0"
    # 0x14 - int32u file format version = 100
    # 0x18 - int32u offset to record directory
    # 0x1c - int32u number of entries in record directory
    # 0x20 - int32u next free index ID = 2
    # 0x24 - int16u swap pattern = 0 (?)
    # 0x28 - int16u[7] spares
    # 0x34 - int32u[2] reserved
    # 0x3c - int32u checksum

    # 1. Read 0x40 bytes and verify that its contents equals AFF\0 or FFF\0
    file_format_id = stream.read(4)  # TODO the check

    # 2. Read FLIR record directory metadata (ref 3)
    stream.seek(16, 1)
    file_format_version = int.from_bytes(stream.read(4), "big")
    record_dir_offset = int.from_bytes(stream.read(4), "big")
    record_dir_entries_count = int.from_bytes(stream.read(4), "big")
    stream.seek(28, 1)
    checksum = int.from_bytes(stream.read(4), "big")

    # 3. Read record directory (which is a FLIR record entry repeated
    # `record_dir_entries_count` times)
    stream.seek(record_dir_offset)
    record_dir_stream = BytesIO(stream.read(32 * record_dir_entries_count))

    # First parse the record metadata
    record_details: Dict[int, Tuple[int, int, int, int]] = {}
    for record_nr in range(record_dir_entries_count):
        record_dir_stream.seek(0)
        details = parse_flir_record_metadata(stream, record_nr)
        if details:
            record_details[details[1]] = details

    # Then parse the actual records
    # for (entry_idx, type, offset, length) in record_details:
    #     parse_record = record_parsers[type]
    #     stream.seek(offset)
    #     record = BytesIO(stream.read(length + 36))  # + 36 needed to find end
    #     parse_record(record, offset, length)

    return record_details


def parse_flir_record_metadata(
    stream: BinaryIO, record_nr: int
) -> Optional[Tuple[int, int, int, int]]:
    # FLIR record entry (ref 3):
    # 0x00 - int16u record type
    # 0x02 - int16u record subtype: RawData 1=BE, 2=LE, 3=PNG; 1 for other record types
    # 0x04 - int32u record version: seen 0x64,0x66,0x67,0x68,0x6f,0x104
    # 0x08 - int32u index id = 1
    # 0x0c - int32u record offset from start of FLIR data
    # 0x10 - int32u record length
    # 0x14 - int32u parent = 0 (?)
    # 0x18 - int32u object number = 0 (?)
    # 0x1c - int32u checksum: 0 for no checksum
    entry = 32 * record_nr
    stream.seek(entry)
    record_type = int.from_bytes(stream.read(2), "big")
    if record_type < 1:
        return None

    # TODO convert unnecessary reads to seeks
    record_subtype = int.from_bytes(stream.read(2), "big")
    record_version = int.from_bytes(stream.read(4), "big")
    index_id = int.from_bytes(stream.read(4), "big")
    record_offset = int.from_bytes(stream.read(4), "big")
    record_length = int.from_bytes(stream.read(4), "big")
    parent = int.from_bytes(stream.read(4), "big")
    object_numer = int.from_bytes(stream.read(4), "big")
    checksum = int.from_bytes(stream.read(4), "big")

    return (entry, record_type, record_offset, record_length)


def extract_optical(stream: BinaryIO) -> Array[int, ..., ..., ...]:
    pass  # TODO write optical data extractor


def parse_raw_data(
    stream: BinaryIO, metadata: Tuple[int, int, int, int]
) -> Tuple[int, int, Array[int, ..., ...]]:
    (entry_idx, _, offset, length) = metadata
    stream.seek(offset)

    # from PIL import ImageFile  # Uncomment to enable loading corrupt PNGs
    # ImageFile.LOAD_TRUNCATED_IMAGES = True

    stream.seek(2, 1)  # Skip first two bytes, TODO Explain the why of the skip
    width = int.from_bytes(stream.read(2), "little")
    height = int.from_bytes(stream.read(2), "little")

    stream.seek(offset + 2 * 16)  # TODO document why 2 * 16
    # data_format = stream.read(4)  # TODO Use format to support different FLIRs
    # print(width, height, type)
    # stream.seek(offset + 2*16)

    # Read the bytes with the raw thermal data
    thermal_bytes = stream.read(length)
    thermal_stream = BytesIO(thermal_bytes)
    thermal_img = Image.open(thermal_stream)
    thermal_np = np.array(thermal_img)

    # Check shape
    if thermal_np.shape != (height, width):
        raise ValueError(
            f"Invalid FLIR: metadata's width and height don't match thermal data's actual width and height ({thermal_np.shape} vs ({height}, {width})"
        )

    # FLIR PNG data is in the wrong byte order, fix that
    fix_byte_order = np.vectorize(lambda x: (x >> 8) + ((x & 0x00FF) << 8))
    thermal_np = fix_byte_order(thermal_np)

    return width, height, thermal_np


def parse_camera_info(
    stream: BinaryIO, metadata: Tuple[int, int, int, int]
) -> Dict[str, Union[int, float]]:
    (entry_idx, _, offset, length) = metadata
    stream.seek(offset + 32)
    stream.seek(offset + 32)

    emissivity = stream.read(4)
    object_distance = stream.read(4)
    refl_app_temp = stream.read(4)
    atmos_temp = stream.read(4)
    ir_window_temp = stream.read(4)
    ir_window_transm = stream.read(4)

    stream.seek(offset + 60)
    rel_humidity = stream.read(4)

    stream.seek(offset + 88)
    planck_r1 = stream.read(4)
    planck_b = stream.read(4)
    planck_f = stream.read(4)

    stream.seek(offset + 776)
    planck_o = stream.read(4)
    planck_r2 = stream.read(4)

    import struct

    float_from_bytes = lambda v: struct.unpack("f", v)[0]

    refl_app_temp_float = float_from_bytes(refl_app_temp)

    # return {
    #    'E': 1.0, #float_from_bytes(emissivity),
    #    'OD': 10.0, #float_from_bytes(object_distance),
    #    'RTemp': -0.0, #refl_app_temp_float - refl_app_temp_float,
    #    'ATemp': 10.0, #float_from_bytes(atmos_temp) - refl_app_temp_float,
    #    'IRWTemp': 20.0, #float_from_bytes(ir_window_temp) - refl_app_temp_float,
    #    'IRT': 1.0, #float_from_bytes(ir_window_transm),
    #    'RH': 94, #float_from_bytes(rel_humidity),
    #    'PR1': 15524.807, #float_from_bytes(planck_r1),
    #    'PB': 1408.7, #float_from_bytes(planck_b),
    #    'PF': 1, #float_from_bytes(planck_f),
    #    'PO': -4272, #struct.unpack('i', planck_o)[0],
    #    'PR2': 0.014428768, #float_from_bytes(planck_r2),
    # }

    return {
        "E": float_from_bytes(emissivity),
        "OD": float_from_bytes(object_distance),
        "RTemp": refl_app_temp_float - refl_app_temp_float,
        "ATemp": float_from_bytes(atmos_temp) - refl_app_temp_float,
        "IRWTemp": float_from_bytes(ir_window_temp) - refl_app_temp_float,
        "IRT": float_from_bytes(ir_window_transm),
        "RH": float_from_bytes(rel_humidity) * 100,
        "PR1": float_from_bytes(planck_r1),
        "PB": float_from_bytes(planck_b),
        "PF": float_from_bytes(planck_f),
        "PO": struct.unpack("i", planck_o)[0],
        "PR2": float_from_bytes(planck_r2),
    }


def raw2temp(
    raw,
    E=1,
    OD=1,
    RTemp=20,
    ATemp=20,
    IRWTemp=20,
    IRT=1,
    RH=50,
    PR1=21106.77,
    PB=1501,
    PF=1,
    PO=-7340,
    PR2=0.012545258,
):
    """
    convert raw values from the flir sensor to temperatures in C
    # this calculation has been ported to python from
    # https://github.com/gtatters/Thermimage/blob/master/R/raw2temp.R
    # a detailed explanation of what is going on here can be found there
    """

    # constants
    ATA1 = 0.006569
    ATA2 = 0.01262
    ATB1 = -0.002276
    ATB2 = -0.00667
    ATX = 1.9

    # transmission through window (calibrated)
    emiss_wind = 1 - IRT
    refl_wind = 0

    # transmission through the air
    h2o = (RH / 100) * exp(
        1.5587
        + 0.06939 * (ATemp)
        - 0.00027816 * (ATemp) ** 2
        + 0.00000068455 * (ATemp) ** 3
    )
    tau1 = ATX * exp(-sqrt(OD / 2) * (ATA1 + ATB1 * sqrt(h2o))) + (1 - ATX) * exp(
        -sqrt(OD / 2) * (ATA2 + ATB2 * sqrt(h2o))
    )
    tau2 = ATX * exp(-sqrt(OD / 2) * (ATA1 + ATB1 * sqrt(h2o))) + (1 - ATX) * exp(
        -sqrt(OD / 2) * (ATA2 + ATB2 * sqrt(h2o))
    )

    # radiance from the environment
    raw_refl1 = PR1 / (PR2 * (exp(PB / (RTemp + 273.15)) - PF)) - PO
    raw_refl1_attn = (1 - E) / E * raw_refl1
    raw_atm1 = PR1 / (PR2 * (exp(PB / (ATemp + 273.15)) - PF)) - PO
    raw_atm1_attn = (1 - tau1) / E / tau1 * raw_atm1
    raw_wind = PR1 / (PR2 * (exp(PB / (IRWTemp + 273.15)) - PF)) - PO
    raw_wind_attn = emiss_wind / E / tau1 / IRT * raw_wind
    raw_refl2 = PR1 / (PR2 * (exp(PB / (RTemp + 273.15)) - PF)) - PO
    raw_refl2_attn = refl_wind / E / tau1 / IRT * raw_refl2
    raw_atm2 = PR1 / (PR2 * (exp(PB / (ATemp + 273.15)) - PF)) - PO
    raw_atm2_attn = (1 - tau2) / E / tau1 / IRT / tau2 * raw_atm2

    raw_obj = (
        raw / E / tau1 / IRT / tau2
        - raw_atm1_attn
        - raw_atm2_attn
        - raw_wind_attn
        - raw_refl1_attn
        - raw_refl2_attn
    )

    # temperature from radiance
    temp_celcius = PB / np.log(PR1 / (PR2 * (raw_obj + PO)) + PF) - 273.15
    return temp_celcius


if __name__ == "__main__":
    import sys

    if not len(sys.argv) == 2:
        print("Usage: flyr.py <path_to_flir_file>")
        exit()

    # TODO Do something useful when called as script
    file_path = sys.argv[1]
    thermal = unpack(file_path)
    print(thermal)
