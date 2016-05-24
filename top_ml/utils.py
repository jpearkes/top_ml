""" Useful functions """
import re
import logging

def regex_search(file_name, regex):
  """ Performs a regex search given a string and a regex expression """
  search = re.compile(regex) 
  value = search.search(file_name)
  return value

def parse_file_name(file_name):
  """
  Parses input file name for event type (z-prime or dijet)
  and file number and creates a corresponding output file name
  """
  output_file_name = "" 
  jzxw = regex_search(file_name,'(JZ\dW)')
  zprimexxx = regex_search(file_name,'(zprime\d+)')
  daod_num = regex_search(file_name,'(\d+).pool.root')  
  if(jzxw):
     output_file_name = "dijet"+jzxw.group(1)
  elif(zprimexxx):
     output_file_name = zprimexxx.group(1)
  output_file_name = output_file_name+"_"+daod_num.group(1)+"jet_inv_mass.root"
  logging.info("Output file:"+output_file_name)
  return output_file_name

