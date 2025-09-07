#!/usr/bin/env python3
"""
Generate VAPID keys for push notifications
"""

from py_vapid import Vapid
import base64

# Generate VAPID keys
vapid = Vapid()
vapid.generate_keys()

# Get raw keys
private_key_raw = vapid.private_key
public_key_raw = vapid.public_key

# Get the keys in the format needed for Django settings
# For private key, we'll use the DER format encoded as base64
from cryptography.hazmat.primitives import serialization

private_der = private_key_raw.private_numbers().private_value.to_bytes(32, 'big')
private_key_b64 = base64.b64encode(private_der).decode()

# For public key, we need the uncompressed format for web push
public_key_point = public_key_raw.public_numbers()
x = public_key_point.x.to_bytes(32, 'big')
y = public_key_point.y.to_bytes(32, 'big')
public_key_uncompressed = b'\x04' + x + y
public_key_b64 = base64.b64encode(public_key_uncompressed).decode()

print("Add these to your Django settings:")
print("=" * 50)
print(f"VAPID_PRIVATE_KEY = '{private_key_b64}'")
print(f"VAPID_PUBLIC_KEY = '{public_key_b64}'")
print("VAPID_CLAIM_EMAIL = 'mailto:admin@bikegarage.com'")
print("=" * 50)

# Also show the public key for JavaScript (URL-safe base64)
public_key_url_safe = base64.urlsafe_b64encode(public_key_uncompressed).decode().strip('=')
print(f"Public key for JavaScript (URL-safe): {public_key_url_safe}")