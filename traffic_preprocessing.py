# Traffic Preprocessing Script for ET-BERT
# Author: Akizuki
# Description: Generates dummy TLS traffic and converts it into BERT token format ([CLS] Hex [SEP]).

from scapy.all import *
import os

PCAP_FILENAME = "generated_traffic.pcap"

def create_dummy_pcap():
    """Generates a PCAP file containing simulated TLS ClientHello packets."""
    print(f"Generating synthetic PCAP file: {PCAP_FILENAME}...")
    # Simulated TLS Client Hello Payload (Hex)
    dummy_payload = bytes.fromhex("16 03 01 00 85 01 00 00 81 03 03 62 34 b0 48 35 1f 26 89")
    
    pkts = []
    for i in range(5):
        # Add slight variation to simulate different packets
        current_payload = dummy_payload + bytes([i]) 
        pkt = Ether()/IP(src="192.168.1.100", dst="1.1.1.1")/TCP(dport=443)/current_payload
        pkts.append(pkt)
        
    wrpcap(PCAP_FILENAME, pkts)
    print("PCAP generation complete.")

def pcap_to_bert_format(pcap_file):
    """Reads PCAP and converts payload to ET-BERT token sequence."""
    print(f"Converting {pcap_file} to ET-BERT tokens...")
    try:
        packets = rdpcap(pcap_file)
    except Exception as e:
        print(f"Error reading PCAP: {e}")
        return []
    
    bert_output = []
    
    for i, pkt in enumerate(packets):
        if TCP in pkt:
            payload = bytes(pkt[TCP].payload)
            if len(payload) > 0:
                # Convert bytes to hex string (e.g., "16 03 01...")
                hex_str = payload.hex()
                # Split into 2-character tokens
                bert_tokens = " ".join([hex_str[i:i+2] for i in range(0, len(hex_str), 2)])
                # Add BERT special tokens
                final_seq = f"[CLS] {bert_tokens} [SEP]"
                bert_output.append(final_seq)
            
    return bert_output

if __name__ == "__main__":
    create_dummy_pcap()
    results = pcap_to_bert_format(PCAP_FILENAME)

    print("-" * 50)
    print("ET-BERT Tokenization Result:")
    print("-" * 50)
    for line in results:
        print(line)