#!/usr/bin/python

# Includes for external modules, install lxml with pip
import urllib
import lxml.html

# String to integer conversion, rough!
def stoint(input_str):
  if input_str is None or input_str == '':
    return 0
  out_number = ''
  for ele in input_str:
    if ele.isdigit():
      out_number += ele
  if out_number == '':
    return 0
  else:
    return float(out_number)

# Configurable for list of drupal modules. Shouldnt change often.
drupal_modules_list = "https://ftp.drupal.org/files/projects/"
drupal_versions = "7.x","8.x"

# Varibles for looping and storing current/high versions/stability in list.
infile = "fileslist-all"
outfile = "fileslist-latest"
curproject = "",""
curdrupalver = ""
curver = ""
curstabver = ""
curstability = ""
curstabilitynum = ""
curdevver = ""
reltype = ""
projlatestver = ""
projlatestoth = ""
projlatestdev = ""

# Main execution code
print "Obtaining Drupal.org file list... please wait (this ones big!)"
connection = urllib.urlopen(drupal_modules_list)
dom = lxml.html.fromstring(connection.read())

# For all the links found (should be in alphanumeric order!)
for link in dom.xpath('//a/@href'):
 if (link.find ("tar.gz") > -1):
  # Need to sort through files like these to find the latest and get them
  # ctools-8.x-3.x-dev.tar.gz
  # ctools-8.x-3.0-alpha27.tar.gz
  # ctools-6.x-1.15.tar.gz
  # views-7.x-3.14.tar.gz
  pnoext = link.replace(".tar.gz","")
  pdeets = pnoext.split("-")
  if (len(pdeets) < 3):
    continue
  if (pdeets[1] not in drupal_versions):
    continue
  proj = pdeets[0],pdeets[1] #"ctools"
  dver = pdeets[1]           #"8.x"
  ver = pdeets[2]            #"3.0"
  if (len(pdeets) > 3):
    stability = pdeets[3] #"alpha27"
  else:
    stability = ""

  stabilitynum = stoint(stability)

  # Project changed, see what highest vals we had for vers
  if (proj != curproject):
    print "For project: ", curproject[0]
    print "High Full Version: ", curver
    print "High stability: ", curstabver, curstability
    print "High Dev version: ", curdevver

    if (curver != ""):
      mainvfile = curproject[0]+"-"+curproject[1]+"-"+curver+".tar.gz"
      print "Fetching: " + drupal_modules_list + mainvfile + " ... "
      urllib.urlretrieve (drupal_modules_list + mainvfile, mainvfile)
      print "-Saved."

    if (curstabver != ""):
      curstafile = curproject[0]+"-"+curproject[1]+"-"+curstabver+"-"+curstability+".tar.gz"
      print "Fetching: " + drupal_modules_list + curstafile + " ... "
      urllib.urlretrieve (drupal_modules_list + curstafile, curstafile)
      print "-Saved."

    if (curdevver != ""):
      curdevfile = curproject[0]+"-"+curproject[1]+"-"+curdevver+"-"+"dev.tar.gz"
      print "Fetching: " + drupal_modules_list + curdevfile + " ... "
      print "-Saved."

    # New project, reset the counters/high vers variables
    curproject = proj
    curver = ""
    curstability = ""
    curstabilitynum = 0
    curstabver = ""
    curdevver = ""
    print "---"

  # Full version - NO RC/BETA/ALPHA
  if (stability == ""):
    if (stoint(ver) > stoint(curver)):
      curver = ver

  # DEV VERSION - Has "dev" in stability text
  if (stability.find("dev") > -1):
    if (stoint(ver) > stoint(curdevver)):
      curdevver = ver

  # RC > BETA > ALPHA - Treat stabilities in an order/heirachy, store their high number with the stability.
  if ((stability.find("alpha") > -1) and (curstability.find("beta") == -1) and (curstability.find("rc") == -1)):
    if (ver > curstabver):
      curstabver = ver
    if ((stabilitynum > curstabilitynum) and (ver == curstabver)):
      curstabilitynum = stabilitynum
    curstability = stability

  if ((stability.find("beta") > -1) and (curstability.find("rc") == -1)):
    if (ver > curstabver):
      curstabver = ver
    if ((stabilitynum > curstabilitynum) and (ver == curstabver)):
      curstabilitynum = stabilitynum
    curstability = stability

  if ((stability.find("rc") > -1)):
    if (ver > curstabver):
      curstabver = ver
    if ((stabilitynum > curstabilitynum) and (ver == curstabver)):
      curstabilitynum = stabilitynum
    curstability = stability

