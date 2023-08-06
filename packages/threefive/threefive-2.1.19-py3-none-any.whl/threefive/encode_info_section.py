
def encode(isec):
    output =b''
    if isec.table_id != '0xfc':
        raise ValueError('splice_info_section.table_id should be 0xfc')   
    a= int(isec.table_id,16) # a
    abyte=int.to_bytes(a,1,byteorder='big')
    output+=abyte
    b=0
    if isec.section_syntax_indicator:
        raise ValueError('splice_info_section.section_syntax_indicator should be False')    
    c=0
     # c << 14
    if isec.private:
        raise ValueError('splice_info_section.private should be False')    
    if isec.reserved != '0x3':
        raise ValueError('splice_info_section.reserved should be 0x3')
    d = 3 << 12
    if isec.section_length > 4093:
        raise ValueError('splice_info_section.section_length cannot be greater than 4093') 
    e=isec.section_length
    ebytes=int.to_bytes(b+c+d+e,2,byteorder='big')
    output +=ebytes
    if isec.protocol_version != 0:
        raise ValueError('splice_info_section.protocol_version should be 0') 
    f=isec.protocol_version
    fbyte = int.to_bytes(f,1,byteorder='big')
    output+=fbyte
    g =0
    if isec.encrypted_packet:
        g= 1 << 39
    h = isec.encryption_algorithm  << 33
    i = isec.pts_adjustment  * 90000 
    ibytes = int.to_bytes(g+h+i,5,byteorder='big')
    output+=ibytes
    j = int(isec.cw_index,16)
    jbyte=int.to_bytes(j,1,byteorder='big')
    output +=jbyte
    if int(isec.tier,16) > 4095:
        raise ValueError('splice_info_section.tier should less than 0xfff')
    k = int(isec.tier,16)  << 12
    l = isec.splice_command_length
    lbytes= int.to_bytes(k+l,3,byteorder='big')
    m = isec.splice_command_type 
    mbytes=int.to_bytes(m,1,byteorder='big')
    output +=mbytes
    print(output)
