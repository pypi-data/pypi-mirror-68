def not_zero(i):
    return i != 0

def gte_zero(i):
    return i >= 0

def MPU():
    pass

def MID():
    pass
"""
Table 20 from page 58 of
https://www.scte.org/SCTEDocs/Standards/ANSI_SCTE%2035%202019r1.pdf

Restrict Group 0 – This segment is restricted for a class of devices
defined by an out of band message that describes which devices are excluded.

Restrict Group 1 – This segment is restricted for a class of devices
defined by an out of band message that describes which devices are excluded.

Restrict Group 2 – This segment is restricted for a class of devices
defined by an out of band message that describes which devices are excluded.
"""
table20 = {
    0x00: "Restrict Group 0",
    0x01: "Restrict Group 1",
    0x02: "Restrict Group 2",
    0x03: "No Restrictions",
}

table21 = {
    0x00: [0, None],
    0x01: [gte_zero, "User Defined"],
    0x02: [8, "ISCI"],
    0x03: [12, "Ad-ID"],
    0x04: [32, "UMID"],
    0x05: [8, "ISAN"],
    0x06: [12, "ISAN"],
    0x07: [12, "TID"],
    0x08: [8, "AiringID"],
    0x09: [gte_zero, "ADI"],
    0x0A: [12, "EIDR"],
    0x0B: [gte_zero, "ATSC"],
    0x0C: [gte_zero, MPU],
    0x0D: [gte_zero, MID],
    0x0E: [gte_zero, "ADS Info"],
    0x0F: [gte_zero, "URI"],
    0x10 - 0xFF: [gte_zero, "Reserved"],
}

"""
table 22 from page 62 of
https://www.scte.org/SCTEDocs/Standards/ANSI_SCTE%2035%202019r1.pdf
I am using the segmentation_type_id as a key.

Segmentation_type_id : segmentation_message
	
"""
table22 = {
    0x00: "Not Indicated",
    0x01: "Content Identification",
    0x10: "Program Start",
    0x11: "Program End",
    0x12: "Program Early Termination",
    0x13: "Program Breakaway",
    0x14: "Program Resumption",
    0x15: "Program Runover Planned",
    0x16: "Program RunoverUnplanned",
    0x17: "Program Overlap Start",
    0x18: "Program Blackout Override",
    0x19: "Program Start – In Progress", 
    0x20: "Chapter Start",
    0x21: "Chapter End",
    0x22: "Break Start",
    0x23: "Break End", 
    0x24: "Opening Credit Start",
    0x25: "Opening Credit End", 
    0x26: "Closing Credit Start",
    0x27: "Closing Credit End",
    0x30: "Provider Advertisement Start",
    0x31: "Provider Advertisement End",
    0x32: "Distributor Advertisement Start",
    0x33: "Distributor Advertisement End", 
    0x34: "Provider Placement Opportunity Start",
    0x35: "Provider Placement Opportunity End", 
    0x36: "Distributor Placement Opportunity Start",
    0x37: "Distributor Placement Opportunity End", 
    0x38: "Provider Overlay Placement Opportunity Start",
    0x39: "Provider Overlay Placement Opportunity End",
    0x3A: "Distributor Overlay Placement Opportunity Start",
    0x3B: "Distributor Overlay Placement Opportunity End",
    0x40: "Unscheduled Event Start", 
    0x41: "Unscheduled Event End", 
    0x50: "Network Start", 
    0x51: "Network End", 
    0x3B: "Distributor Overlay Placement Opportunity End",
    0x40: "Unscheduled Event Start", 
    0x41: "Unscheduled Event End", 
    0x50: "Network Start",
    0x51: "Network End"}
