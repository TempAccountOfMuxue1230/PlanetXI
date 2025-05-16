"""
File: binary.py
File Version: 1.0
"""
import json
import pickle
import hashlib


def is_file_changed(bin_file, json_file):
    """
    Check file hash
    """
    old_hash = bin_file.read(64)
    new_hash = hashlib.sha512(json_file.read().encode('utf-8')).digest()
    return not old_hash == new_hash


def serialize_json2bin(bin_file, json_file):
    """
    Serialize json to bin
    """
    json_context = json_file.read()
    json_object = json.loads(json_context)
    json_bin = pickle.dumps(json_object)
    json_hash = hashlib.sha512(json_context.encode('utf-8')).digest()

    bin_file.write(json_hash+json_bin)


def get_bin_file_context(bin_file):
    """
    Get bin file context
    """
    bin_file_context = bin_file.read()
    bin_file_object = pickle.loads(bin_file_context)
    return bin_file_object
