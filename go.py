#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# go.py
"""Read an xml file, look for the corresponding ROMs (by CRC32 then SHA1) and save them for MAME.
Lionel Cordesses
"""

import xml.etree.ElementTree as ET
import sys
import hashlib
import os
import os.path
import datetime
import zlib # for CRC32, which is fastest than binascii (not ckeched recently, though)
from zipfile import ZipFile
import zipfile
try: 
    import zlib 
    zip_compression_method= zipfile.ZIP_DEFLATED 
except: 
    zip_compression_method= zipfile.ZIP_STORED     
import itertools


my_verbosity=1

# Some files are interleaved. Instead of writing a specific routine that would
# handle this case, I prefer to create two deinterleaved files that will be processed by the very same routine.
# This routine create_even_odd_files creates two deinterleaved files for every single file in the directory my_ROM_input_directory.
def create_even_odd_files(my_ROM_input_directory):
    my_ROM_input_directory=os.path.abspath(my_ROM_input_directory)
    for file in os.listdir(my_ROM_input_directory):
        my_filename=os.path.join(my_ROM_input_directory, file)
        #print(my_filename)
        with open(my_filename, 'rb') as my_file:
            buf = my_file.read()
            my_filelength=len(buf)
        with open(my_filename+'.e', 'wb') as my_file:
            my_file.write(buf[0:my_filelength:2])
        with open(my_filename+'.o', 'wb') as my_file:
            my_file.write(buf[1:my_filelength:2])    

# Some files are not stored as MAME expect them. It looks like they are stored as smalled chuncks (slices in my code). Example: a 32 kbyte file seems to be sliced into 4 chuncks of 8 kbytes. This routine looks for all the combinaisons of "my_size/my_nb_of_slices" bytes that makes one vector of length my_size.
# The main use of this routine is for the game Armored Scrum Object, more specifically for the file ASOArmoredScrumObject.sp
# my_output_filename, my_size, my_CRC32, my_SHA1 are for the output.
def move_slices(my_input_filename, my_output_filename, my_size, my_CRC32, my_SHA1, my_nb_of_slices):
    #print('Lionel')
    #sha1sum = hashlib.sha1()
    with open(my_input_filename,'rb') as f:
        my_data = f.read()
    # Each output vector (of length my_size) will have my_nb_of_slices slices.
    # We have to split the input vector in slices of length my_size/my_nb_of_slices.
    # The total number of slices for the input vector is: my_nb_of_slices*len(my_data)/my_size
    my_total_number_of_slices=int(my_nb_of_slices*len(my_data)/my_size)
    my_size_of_one_slice=int(my_size/my_nb_of_slices)
    print("Input vector length={}".format(len(my_data)))
    print("Total number of slices of length {0:5d} ={1:5d}".format(my_size_of_one_slice, my_total_number_of_slices))
    # Create all the combinations of slices
    for my_c in itertools.permutations(range(my_total_number_of_slices), my_nb_of_slices):
        #print(my_c)
        my_out=b''
        for i in my_c:
            #print(i)
            i_start=i*my_size_of_one_slice
            i_end=(i+1)*my_size_of_one_slice
            my_out=my_out+my_data[i_start:i_end]
        #print(my_out)
        p_crc='{:08x}'.format(zlib.crc32(bytes(my_out)))
        if p_crc==my_CRC32:
            my_computed_SHA1=hashlib.sha1(my_out)
            my_computed_SHA1_hex=my_computed_SHA1.hexdigest()
            if my_computed_SHA1_hex==my_SHA1:
                with open(my_output_filename,'wb') as f:
                    f.write(my_out)
                print('Found {}'.format(my_output_filename))
                break

def prepare_for_ASO(my_ROM_input_directory):
    my_ROM_input_directory=os.path.abspath(my_ROM_input_directory)
    my_filename_in=os.path.join(my_ROM_input_directory, "ASOArmoredScrumObject.sp")
    move_slices(my_filename_in,os.path.join(my_ROM_input_directory,"aso.11"), 32768, '7feac86c','13b81f006ec587583416c1e7432da4c3f0375924', 4)
    move_slices(my_filename_in, os.path.join(my_ROM_input_directory,"aso.12"), 32768, '6895990b','e84554cae9a768021c3dc7183bc3d28e2dd768ee', 4)    
    move_slices(my_filename_in, os.path.join(my_ROM_input_directory,"aso.13"), 32768, '87a81ce1','28c1069e6c08ecd579f99620c1cb6df01ad1aa74', 4)  

my_list_of_pal=(('marvins','MarvinsMaze.pal','marvmaze.j1', 'marvmaze.j2', 'marvmaze.j3'),
('athena','Athena.pal','up02_c2.rom','up02_b1.rom', 'up02_c1.rom'),
('gwar','GuerillaWar.pal','guprom.3','guprom.2', 'guprom.1'),
('ikari','IkariWarriors.pal','7122er.prm','7122eg.prm', '7122eb.prm'),
('tnk3','TNKIII.pal','7122.2','7122.1', '7122.0'),
('victroad','VictoryRoad.pal','mb7122e.1k','mb7122e.2l', 'mb7122e.1l'),
('dogosoke','VictoryRoad.j.pal','up03_k1.rom','up03_l2.rom', 'up03_l1.rom'),
('aso','ASOArmoredScrumObject.pal','up02_f12.rom','up02_f13.rom', 'up02_f14.rom'))


def get_bit(x,i):
    if x & (1<<i)>0:
        return 1
    else:
        return 0

def set_bit(x,i,v):
    if v>0:
        return (x | (1<<i))
    else:
        return x

def change_bit_position(my_data, my_LUT, my_out_1, my_out_2,my_out_3):
    k=0
    for i in range(0,len(my_data),2):
        p=my_data[i]
        n1=(p>>4) & 0x0f
        n2=(p & 0x0f)
        p=my_data[i+1]
        n3=(p>>4) & 0x0f
        n4=(p & 0x0f)    
        if (my_verbosity>=3):
            if n3>0:
                print('Problem: high nibble at table[{:d}]={:d}'.format(i+1,n3))
        my_word_in=(n1*16+n2)*16+n4
        my_word_out=0
        if (my_verbosity>=3):
            print(' {:03x}'.format(my_word_in))
        for b in range(0,len(my_LUT)):
            my_bit_index=my_LUT[b]
            my_bit_value=get_bit(my_word_in, my_bit_index)
            my_word_out=set_bit(my_word_out, b, my_bit_value)
        if (my_verbosity>=3):
            print(' {:03x}'.format(my_word_out))
        # Saves the results
        my_out_1[k]= (my_word_out >> 8) & 0x0f
        my_out_2[k]= (my_word_out >> 4) & 0x0f
        my_out_3[k]= (my_word_out & 0x0f)
        k=k+1
    return my_out_1, my_out_2,my_out_3

def my_try_lionel(my_input_filename, my_CRC32, my_SHA1):
    print('Bit swaping original file to create the PROM file. Brute force: it may take a while.')
    try:
        with open(my_input_filename,'rb') as f:
            my_data = f.read()
    except Exception:
        print('Lionel error: {} not found'.format(my_input_filename))
        return [],[]
    else:
        t1=[0]*int(len(my_data)/2)
        t2=[0]*int(len(my_data)/2)
        t3=[0]*int(len(my_data)/2)    
        my_LUT=[0,1,2,3,4,5,6,7,8,9,10,11]
        my_LUT=[11,5,6,7,0,1,8,4,2,3,9,10]
        my_nb_permutations=len(my_LUT)*(len(my_LUT)-1)*(len(my_LUT)-2)*(len(my_LUT)-3)
        k=0
        for my_L in itertools.permutations(my_LUT, 4):
            #t3=change_bit_position_for_one(my_data, my_L, t1)
            t1, t2, t3 = change_bit_position(my_data, my_L, t1, t2, t3)
            p_crc='{:08x}'.format(zlib.crc32(bytes(t3)))
            if p_crc==my_CRC32:
                my_LUT_out=my_L
                break
            k=k+1
            if (k%int((my_nb_permutations/10)))==0:
                print('{}/{}'.format(k,my_nb_permutations))
        return my_LUT_out, t3

def create_pal_file(my_ROM_input_directory, my_game_name, name_of_MAME_game):
    # Look for the list with the pal files corresponding to the game name_of_MAME_game
    for i,p in enumerate(my_list_of_pal):
        if name_of_MAME_game in p:
            my_pal_input_file=p[1]
            my_pal_filenames=p[2:]
            print(my_pal_filenames,i)     
    myROM_size =[0]*3    
    myROM_CRC = [0]*3    
    myROM_SHA1 = [0]*3   
    myROM_filename = [0]*3
    for provi in my_game_name.iter('rom'):
        #print(provi.attrib)
        myROM_name=provi.get('name')
        #print(myROM_name)       
        if myROM_name in my_pal_filenames:          
            i=my_pal_filenames.index(myROM_name)
            myROM_size[i]=int(provi.get('size'))
            myROM_CRC_p=provi.get('crc')
            myROM_CRC[i]=myROM_CRC_p.lower()
            myROM_SHA1[i]=provi.get('sha1')
            myROM_filename[i]=myROM_name
            #print(f"\nROM name={myROM_name}, size={myROM_size} bytes, CRC={myROM_CRC}, SHA1={myROM_SHA1}")    
# Here, we should have the three filenames for the the PAL files, and their CRCs.
    if len(myROM_CRC)==3:
        #print(myROM_CRC)
        my_pal_input_file_with_dir=os.path.join(my_ROM_input_directory, my_pal_input_file)
        my_L1, my_t1=my_try_lionel(my_pal_input_file_with_dir, myROM_CRC[0], myROM_SHA1[0])
        print('LUT_1={}'.format(my_L1))
        if len(my_L1)>0:
            print("OK L1")
        my_L2, my_t2=my_try_lionel(my_pal_input_file_with_dir, myROM_CRC[1], myROM_SHA1[1])
        print('LUT_2={}'.format(my_L2))
        my_L3, my_t3=my_try_lionel(my_pal_input_file_with_dir, myROM_CRC[2], myROM_SHA1[2])
        print('LUT_3={}'.format(my_L3))    
        if len(my_L1)>0 and len(my_L2)>0 and len(my_L3)>0:
            with open(os.path.join(my_ROM_input_directory,myROM_filename[0]),'wb') as f:
                for b in my_t1:
                    f.write(b.to_bytes(1, byteorder='big'))
            with open(os.path.join(my_ROM_input_directory,myROM_filename[1]),'wb') as f:
                for b in my_t2:
                    f.write(b.to_bytes(1, byteorder='big'))        
            with open(os.path.join(my_ROM_input_directory,myROM_filename[2]),'wb') as f:
                for b in my_t3:
                    f.write(b.to_bytes(1, byteorder='big'))             


# my_step=1 for a window sliding at each byte. my_step=4096 for a window sliding every 4096 bytes.
def look_for_romset(my_xml_filename,my_output_folder_name, my_ROM_input_directory, my_step=1):
    my_output_folder_name=os.path.abspath(my_output_folder_name)
    my_folder_name=my_output_folder_name+'_'+os.path.splitext(os.path.basename(my_xml_filename))[0]
    if os.path.isdir(my_folder_name):
        print("This directory exists: {:s}".format(my_folder_name))
    else:
        print("Let's create the output directory: {:s}".format(my_folder_name))
        os.mkdir(my_folder_name)
    my_out_directory=my_folder_name

    #sha1sum = hashlib.sha1()

    tree = ET.parse(my_xml_filename)
    root = tree.getroot()


    my_list_of_missing_files=[]
    my_list_of_complete_romsets=[]
    my_list_of_files_found=[]
    # string for dd commands for Linux.
    my_str_dd="my_tmp=$(date +\"%Y_%m_%d_%H_%M_%S\")\nmkdir -p ${my_tmp}\n"
    for my_game_name in root.findall('game'):
        name = my_game_name.get('name')
        #print(name)
        my_zip_name_with_path=os.path.join(my_out_directory,name+'.zip')
        f_one_missing_rom=False                             
        if name=='paddlema':
            create_even_odd_files(my_ROM_input_directory)  
        #if name=='samsho2':
        #    create_even_odd_files(my_ROM_input_directory)              
        if name=='aso':    
            prepare_for_ASO(my_ROM_input_directory)
        if name=='marvins' or name=='athena' or name=='gwar' or name=='ikari' or name=='dogosoke' or name=='victroad' or name=='tnk3' or name=='aso':          
            create_pal_file(my_ROM_input_directory, my_game_name, name)
        my_zip=None
        if name!='zzzz':              
            #print(name)
            for provi in my_game_name.iter('rom'):
                #print(provi.attrib)
                f_Next_ROM=False
                myROM_name=provi.get('name')
                #print(myROM_name)
                myROM_size=int(provi.get('size'))
                myROM_CRC=provi.get('crc')
                if myROM_CRC!=None:
                    myROM_CRC=myROM_CRC.lower()
                myROM_SHA1=provi.get('sha1')
                if myROM_SHA1==None and myROM_CRC==None:
                    print(f"ROM name={myROM_name}: no CRC, no SHA1 in the xml file.")
                    continue                    
                print(f"\nROM name={myROM_name}, size={myROM_size} bytes, CRC={myROM_CRC}, SHA1={myROM_SHA1}")
            
                print("\nLooking for {:s}\n".format(myROM_name), end='')
                #if myROM_name=="3ww.rom":
                #    break
                # We have not found yet the file that we are looking for (* Wars?)
                f_found_ROM=False
                for file in os.listdir(my_ROM_input_directory):
                    my_filename=os.path.join(my_ROM_input_directory, file)
                    #print(my_filename)
                    with open(my_filename, 'rb') as my_file:
                        buf = my_file.read()
                        my_filelength=len(buf)
                        print("in file {:s} (length={:d} bytes)\n".format(my_filename, my_filelength), end='')                    

                        my_percent_old=0
                        i_max=my_filelength-myROM_size+1
                        for i in range(0,i_max, my_step):
                            my_start=i
                            my_end=i+myROM_size
                            my_percent=int(i*100/i_max)
                            if (int(my_percent)>int(my_percent_old)):
                                print('\r{} % '.format(int(my_percent)), end='', flush=True)
                                my_percent_old=my_percent
                            #if my_outfilename=="zaxxon.u72":
                            #    print("{:6d}:{:6d}".format(i, my_end-1))
                            my_sliding_buf=buf[my_start:my_end]
                            my_sliding_CRC32='{:08x}'.format(zlib.crc32(my_sliding_buf) & 0xffffffff)
                            #print(my_sliding_CRC32)
                            if my_sliding_CRC32==myROM_CRC:
                                my_sliding_SHA1=hashlib.sha1(my_sliding_buf)
                                my_sliding_SHA1_hex=my_sliding_SHA1.hexdigest()
                                #print(my_sliding_SHA1_hex)
                                if my_sliding_SHA1_hex==myROM_SHA1 or myROM_SHA1==None:
                                    print("\nFound {:s} in {:s} at {:X}..{:X}".format(myROM_name, my_filename, i, my_end-1))
                                    my_list_of_files_found.append([myROM_name, my_filename, i, my_end-1])
                                    my_str_dd=my_str_dd+"\ndd if={:s} of=${{my_tmp}}/{:s} bs=1 count={:d} seek={:d}".format(my_filename, myROM_name, myROM_size, my_start)
                                    #print(my_sliding_SHA1_hex)
                                    my_new_directory_name=os.path.join(my_out_directory, name)
                                    if os.path.isdir(my_new_directory_name)==False:
                                        #os.mkdir(my_out_directory+f"/"+name)
                                        os.mkdir(my_new_directory_name)
                                    #my_output_filename=os.path.join(my_out_directory,name,myROM_name)
                                    my_output_filename=os.path.join(my_new_directory_name,myROM_name)
                                    f=open(my_output_filename,"wb")
                                    #f=open(my_out_directory+f"/{name}/"+myROM_name,"wb")
                                    f.write(my_sliding_buf)
                                    f.close()
                                    # We can create the zip file (my_zip_name) and add the newly created rom (my_output_filename).
                                    # It will be stored in the directory (my_out_directory).
                                    if os.path.isfile(my_zip_name_with_path)==False:
                                        # Create the zip file
                                        my_zip=ZipFile(my_zip_name_with_path, 'w', compression=zip_compression_method, compresslevel=9)
                                    # Add the file (my_output_filename) to the zip archive.
                                    my_zip.write(my_output_filename, arcname=myROM_name)
                                    f_Next_ROM=True
                                    f_found_ROM=True
                                    break
                        if (f_Next_ROM==True):
                            print("It should skip to the next file...")
                            break
                    # if (f_Next_ROM==False):
                    #     print(f'{myROM_name} not found!')
                    #     f_one_missing_rom=True
                    #     my_list_of_missing_files.append((name, myROM_name))
                if f_found_ROM==False:
                    print(f'{myROM_name} not found!')
                    f_one_missing_rom=True
                    my_list_of_missing_files.append((name, myROM_name))
            if my_zip!=None:
                my_zip.close()
            if f_one_missing_rom==False:
                my_list_of_complete_romsets.append(name)    
            else:
                if my_zip!=None:
                    # Closes the zip file and rename itso that we know it is not a complete ROM set.
                    print('Incomplete ROM set: rename the zip file to .zip.bad')
                    os.rename(my_zip_name_with_path,my_zip_name_with_path+'.bad')

    print("List of complete ROM sets:")
    print(my_list_of_complete_romsets)
    print("List of missing files:")
    print(my_list_of_missing_files)
    print("Summary of files found: filename, in_file, from, to")
    print(my_list_of_files_found)
    print(my_str_dd)
    return my_list_of_complete_romsets, my_list_of_missing_files


def test_complete_set():
    c,m = look_for_romset('/home/lionel/devel/snk_40th/python/tstXML/validation/ik2003small_OK.xml','/home/lionel/devel/snk_40th/python/tstXML/validation/tst_01','/home/lionel/devel/snk_40th/python/tstXML/validation/rawromsmall_OK')
    print(c)
    print(m)
    if c[0]=='ikari' and not m:
        print('Test of a complete fake set passed.')
        f_out=True
    else:
        print('Test of a complete fake set failed.')
        f_out=False
    return f_out        


def test_incomplete_set():
    c,m = look_for_romset('/home/lionel/devel/snk_40th/python/tstXML/validation/ik2003small_NOK.xml','/home/lionel/devel/snk_40th/python/tstXML/validation/tst_01','/home/lionel/devel/snk_40th/python/tstXML/validation/rawromsmall_OK')
    print(c)
    print(m)
    if not c and m==[('ikari', '16.rom')]:
        print('Test of an incomplete fake set passed.')
        f_out=True
    else:
        print('Test of an incomplete fake set failed.')
        f_out=False
    return f_out

# This test checks a regression when I switched to CRC32 and forgot to zero-pad the computed CRC. 
# A CRC looked like that: 0f and the correspondinf string was shortened to f, which did not match the CRC from the xml file.
def test_3_pal_set():
    c,m = look_for_romset('/home/lionel/devel/snk_40th/python/tstXML/validation/ik2003_3pal.xml','/home/lionel/devel/snk_40th/python/tstXML/validation/tst_01','/home/lionel/devel/snk_40th/python/tstXML/validation/rawrom_3pal')
    print(c)
    print(m)
    if c[0]=='ikari' and not m:
        print('Test of a 3 pal ROMs passed.')
        f_out=True
    else:
        print('Test of  pal ROMs failed.')
        f_out=False
    return f_out

def test_all():
    f1=test_complete_set()
    f2=test_incomplete_set()    
    f3=test_3_pal_set()
    if f1 and f2 and f3:
        print('All tests passed.')  
    else:
        print('One test failed.')

if __name__ == "__main__":
    #test_complete_set()
    #test_incomplete_set()
    #test_3_pal_set()
    #test_all()    
    now=datetime.datetime.now()
    my_output_folder_name=now.strftime("d_%Y_%m_%d_%H_%M_%S_%f")    
    #my_directory="./rawromVictory"
    if not sys.argv[1:]:
        #sys.exit(__doc__.strip())
        print('USE: python3 go.py rom_directory file.xml')    
        print('This program comes with ABSOLUTELY NO WARRANTY. This is free software.')        

        #c,m = look_for_romset(my_xml, my_output_folder_name, my_input_directory,4096*4)
    else:
        my_input_directory=sys.argv[1]    
        my_xml=sys.argv[2] 
  
        c,m = look_for_romset(my_xml, my_output_folder_name, my_input_directory)
        #print(c)
        #print(m)

