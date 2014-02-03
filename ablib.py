# ablib.py 
#
# Python functions collection to easily manage the I/O lines and 
# Daisy modules with the following Acme Systems boards:
# TERRA Board (http://www.acmesystems.it/terra)
# FOX Board G20 (http://www.acmesystems.it/FOXG20)
# ARIA G25 (http://www.acmesystems.it/aria) 
#
# (C) 2013 Sergio Tanzilli <tanzilli@acmesystems.it>
# (C) 2012 Acme Systems srl (http://www.acmesystems.it)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import os.path
import platform
import smbus
import time
from serial import Serial
import fcntl
import struct
import thread
import threading
import select

if platform.platform().find("Linux-2")!=-1:
	legacy_id=True
else: 	
	legacy_id=False

serial_ports = {
	'D1' :  '/dev/ttyS2',
	'D2' :  '/dev/ttyS5',
	'D3' :  '/dev/ttyS1',
	'D5' :  '/dev/ttyS6',
	'D6' :  '/dev/ttyS4',
	'D8' :  '/dev/ttyS3',
	'D10':  '/dev/ttyS4',
	'D13':  '/dev/ttyS2'
}

# Connectors pin assignments
# 'pin name', 'kernel id'  # pin description

aria_north = {
	'2'  :  96,
	'3'  :  97,
	'4'  :  98,
	'5'  :  99,
	'6'  : 100,
	'7'  : 101,
	'8'  : 102,
	'9' :  103,
	'10' : 104,
	'11' : 105,
	'12' : 106,
	'13' : 107,
	'14' : 108,
	'15' : 109,
	'16' : 110,
	'17' : 111,
	'18' : 112,
	'19' : 113,
	'20' : 114,
	'21' : 115,
	'22' : 116,
	'23' : 117,
}

aria_east = {
	'2'  : 118,
	'3'  : 119,
	'4'  : 120,
	'5'  : 121,
	'6'  : 122,
	'7'  : 123,
	'8'  : 124,
	'9' :  125,
	'10' : 126,
	'11' : 127,
}

aria_south = {
	'2'  :  53,
	'3'  :  52,
	'4'  :  51,
	'5'  :  50,
	'6'  :  49,
	'7'  :  48,
	'8'  :  47,
	'9' :   46,
	'10' :  45,
	'11' :  44,
	'12' :  43,
	'13' :  42,
	'14' :  41,
	'15' :  40,
	'16' :  39,
	'17' :  38,
	'18' :  37,
	'19' :  36,
	'20' :  35,
	'21' :  34,
	'22' :  33,
	'23' :  32,
}

aria_west = {
	'9' :   54,
	'10' :  55,
	'11' :  56,
	'12' :  57,
	'13' :  58,
	'14' :  59,
	'15' :  60,
	'16' :  61,
	'17' :  62,
	'18' :  63,
	'20' :  75,
	'21' :  76,
	'22' :  77,
	'23' :  78,
}

J7_kernel_ids = {
	'3'  :  82,
	'4'  :  83,
	'5'  :  80,
	'6'  :  81,
	'7'  :  66,
	'8'  :  67,
	'9'  :  64,
	'10' :  65,
	'11' : 110,
	'12' : 111,
	'13' : 108,
	'14' : 109,
	'15' : 105,
	'16' : 106,
	'17' : 103,
	'18' : 104,
	'19' : 101,
	'20' : 102,
	'21' :  73,
	'22' :  72,
	'31' :  87,
	'32' :  86,
	'33' :  89,
	'34' :  88,
	'35' :  60,
	'36' :  59,
	'37' :  58,
	'38' :  57,
}

J6_kernel_ids = {
	'3'  :  92,
	'4'  :  71,
	'5'  :  70,
	'6'  :  93,
	'7'  :  90,
	'8'  :  69,
	'9'  :  68,
	'10' :  91,
	'13' :  75,
	'14' :  74,
	'15' :  77,
	'16' :  76,
	'17' :  85,
	'18' :  84,
	'19' :  95,
	'20' :  94,
	'21' :  63,
	'22' :  62,
	'24' :  38,
	'25' :  39,
	'26' :  41,
	'27' :  99,
	'28' :  98,
	'29' :  97,
	'30' :  96,
	'31' :  56,
	'32' :  55,
	'36' :  42,
	'37' :  54,
	'38' :  43,
}


D1_kernel_ids = {
	'1' :   0, #3V3
	'2' :  70, #PB6
	'3' :  71, #PB7
	'4' :  92, #PB28
	'5' :  93, #PB29
	'6' :   0, #N.C.
	'7' :  55, #PA23
	'8' :  56, #PA24
	'9' :   0, #5V0
	'10':   0, #GND
}

D2_kernel_ids = {
	'1' :   0, #3V3
	'2' :  63, #PA31
	'3' :  62, #PA30
	'4' :  61, #PA29
	'5' :  60, #PA28
	'6' :  59, #PA27
	'7' :  58, #PA26
	'8' :  57, #PA25
	'9' :  94, #PB30
	'10':   0, #GND
}

D3_kernel_ids = {
	'1' :   0, #3V3
	'2' :  68, #PB4
	'3' :  69, #PB5
	'4' :  90, #PB26
	'5' :  91, #PB27
	'6' :  86, #PB22
	'7' :  88, #PB24
	'8' :  89, #PB25
	'9' :  87, #PB23
	'10':   0, #GND
}

D4_kernel_ids = {
	'1' :   0, #3V3
	'2' :   0, #AVDD
	'3' :   0, #VREF
	'4' :   0, #AGND
	'5' :  96, #PC0
	'6' :  97, #PC1
	'7' :  98, #PC2
	'8' :  99, #PC3
	'9' :   0, #5V0
	'10':   0, #GND
}


D5_kernel_ids = {
	'1' :   0, #3V3
	'2' :  76, #PB12
	'3' :  77, #PB13
	'4' :  80, #PB16
	'5' :  81, #PB17
	'6' :  82, #PB18
	'7' :  83, #PB19
	'8' :  84, #PB20
	'9' :  85, #PB21
	'10':  0,  #GND
}

D6_kernel_ids = {
	'1' :   0, #3V3
	'2' :  74, #PB10
	'3' :  75, #PB11
	'4' : 104, #PC8
	'5' : 106, #PC10
	'6' :  95, #PB31
	'7' :  55, #PA23
	'8' :  56, #PA24
	'9' :   0, #5V0
	'10':   0, #GND
}

D7_kernel_ids = {
	'1' :  0,  #3V3
	'2' :  65, #PB1
	'3' :  64, #PB0
	'4' :  66, #PB2
	'5' :  67, #PB3
	'6' : 101, #PC5
	'7' : 100, #PC4
	'8' :  99, #PC3
	'9' :   0, #5V0
	'10':   0, #GND
}

D8_kernel_ids = {
	'1' :   0, #3V3
	'2' :  72, #PB8
	'3' :  73, #PB9
	'4' :   0, #N.C.
	'5' :   0, #N.C.
	'6' :   0, #N.C.
	'7' :  55, #PA23
	'8' :  56, #PA24
	'9' :   0, #5V0
	'10':   0, #GND
}

#Terra D10
D10_kernel_ids = {
	'1' :   0, #3V3
	'2' : 118, #PC22
	'3' : 119, #PC23
	'4' : 120, #PC24
	'5' : 121, #PC25
	'6' : 122, #PC26
	'7' :  62, #PA30
	'8' :  63, #PA31
	'9' :   0, #5V0
	'10':   0, #GND
}

#Terra D11
D11_kernel_ids = {
	'1' :   0,  #3V3
	'2' : 112, #PC16
	'3' : 113, #PC17
	'4' : 114, #PC18
	'5' : 115, #PC19
	'6' : 116, #PC20
	'7' : 117, #PC21
	'8' :  98, #PC2
	'9' :  99, #PC3
	'10':   0, #GND
}

#Terra D12
D12_kernel_ids = {
	'1' :   0, #3V3
	'2' : 104, #PC8
	'3' : 105, #PC9
	'4' : 106, #PC10
	'5' : 107, #PC11
	'6' : 108, #PC12
	'7' : 109, #PC13
	'8' : 110, #PC14
	'9' : 111, #PC15
	'10':   0, #GND
}

#Terra D13
D13_kernel_ids = {
	'1' :   0, #3V3
	'2' :  37, #PA5
	'3' :  38, #PA6
	'4' : 123, #PC27
	'5' : 124, #PC28
	'6' : 125, #PC29
	'7' :  96, #PC0
	'8' :  97, #PC1
	'9' :   0, #5V0
	'10':   0, #GND
}

#Terra D14
D14_kernel_ids = {
	'1' :   0, #3V3
	'2' :   0, #3V3
	'3' :   0, #VREF
	'4' :   0, #GND
	'5' :  75, #PB11
	'6' :  76, #PB12
	'7' :  77, #PB13
	'8' :  78, #PB14
	'9' :   0, #5V0
	'10':   0, #GND
}

#Terra D15
D15_kernel_ids = {
	'1' :   0, #3V3
	'2' :  44, #PA12
	'3' :  43, #PA11
	'4' :  45, #PA13
	'5' :  46, #PA14
	'6' :  39, #PA7
	'7' :  33, #PA1
	'8' :   0, #N.C.
	'9' :   0, #5V0
	'10':   0, #GND
}

#Terra D16
D16_kernel_ids = {
	'1' :   0, #3V3
	'2' :  61, #PA29
	'3' :  59, #PA27
	'4' :  56, #PA24
	'5' :  57, #PA25
	'6' :  58, #PA26
	'7' :  62, #PA30
	'8' :  63, #PA31.
	'9' :  60, #PA28
	'10':   0, #GND
}	


# Kernel IDs descriptors for each connector
connectors = {
	'N'   :  aria_north,
	'E'   :  aria_east,
	'S'   :  aria_south,
	'W'   :  aria_west,
	'J6'  :  J6_kernel_ids,
	'J7'  :  J7_kernel_ids,
	'D1'  :  D1_kernel_ids,
	'D2'  :  D2_kernel_ids,
	'D3'  :  D3_kernel_ids,
	'D4'  :  D4_kernel_ids,
	'D5'  :  D5_kernel_ids,
	'D6'  :  D6_kernel_ids,
	'D7'  :  D7_kernel_ids,
	'D8'  :  D8_kernel_ids,
	'D10' :  D10_kernel_ids,
	'D11' :  D11_kernel_ids,
	'D12' :  D12_kernel_ids,
	'D13' :  D13_kernel_ids,
	'D14' :  D14_kernel_ids,
	'D15' :  D15_kernel_ids,
	'D16' :  D16_kernel_ids,
}

#New pin assigment table
pin2kid = {
	'N2'  :  96,
	'N3'  :  97,
	'N4'  :  98,
	'N5'  :  99,
	'N6'  : 100,
	'N7'  : 101,
	'N8'  : 102,
	'N9' :  103,
	'N10' : 104,
	'N11' : 105,
	'N12' : 106,
	'N13' : 107,
	'N14' : 108,
	'N15' : 109,
	'N16' : 110,
	'N17' : 111,
	'N18' : 112,
	'N19' : 113,
	'N20' : 114,
	'N21' : 115,
	'N22' : 116,
	'N23' : 117,
	'E2'  : 118,
	'E3'  : 119,
	'E4'  : 120,
	'E5'  : 121,
	'E6'  : 122,
	'E7'  : 123,
	'E8'  : 124,
	'E9' :  125,
	'E10' : 126,
	'E11' : 127,
	'S2'  :  53,
	'S3'  :  52,
	'S4'  :  51,
	'S5'  :  50,
	'S6'  :  49,
	'S7'  :  48,
	'S8'  :  47,
	'S9' :   46,
	'S10' :  45,
	'S11' :  44,
	'S12' :  43,
	'S13' :  42,
	'S14' :  41,
	'S15' :  40,
	'S16' :  39,
	'S17' :  38,
	'S18' :  37,
	'S19' :  36,
	'S20' :  35,
	'S21' :  34,
	'S22' :  33,
	'S23' :  32,
	'W9' :   54,
	'W10' :  55,
	'W11' :  56,
	'W12' :  57,
	'W13' :  58,
	'W14' :  59,
	'W15' :  60,
	'W16' :  61,
	'W17' :  62,
	'W18' :  63,
	'W20' :  75,
	'W21' :  76,
	'W22' :  77,
	'W23' :  78,
	'J7.3'  :  82,
	'J7.4'  :  83,
	'J7.5'  :  80,
	'J7.6'  :  81,
	'J7.7'  :  66,
	'J7.8'  :  67,
	'J7.9'  :  64,
	'J7.10' :  65,
	'J7.11' : 110,
	'J7.12' : 111,
	'J7.13' : 108,
	'J7.14' : 109,
	'J7.15' : 105,
	'J7.16' : 106,
	'J7.17' : 103,
	'J7.18' : 104,
	'J7.19' : 101,
	'J7.20' : 102,
	'J7.21' :  73,
	'J7.22' :  72,
	'J7.31' :  87,
	'J7.32' :  86,
	'J7.33' :  89,
	'J7.34' :  88,
	'J7.35' :  60,
	'J7.36' :  59,
	'J7.37' :  58,
	'J7.38' :  57,
	'J6.3'  :  92,
	'J6.4'  :  71,
	'J6.5'  :  70,
	'J6.6'  :  93,
	'J6.7'  :  90,
	'J6.8'  :  69,
	'J6.9'  :  68,
	'J6.10' :  91,
	'J6.13' :  75,
	'J6.14' :  74,
	'J6.15' :  77,
	'J6.16' :  76,
	'J6.17' :  85,
	'J6.18' :  84,
	'J6.19' :  95,
	'J6.20' :  94,
	'J6.21' :  63,
	'J6.22' :  62,
	'J6.24' :  38,
	'J6.25' :  39,
	'J6.26' :  41,
	'J6.27' :  99,
	'J6.28' :  98,
	'J6.29' :  97,
	'J6.30' :  96,
	'J6.31' :  56,
	'J6.32' :  55,
	'J6.36' :  42,
	'J6.37' :  54,
	'J6.38' :  43,
	'D1.1' :   0, #3V3
	'D1.2' :  70, #PB6
	'D1.3' :  71, #PB7
	'D1.4' :  92, #PB28
	'D1.5' :  93, #PB29
	'D1.6' :   0, #N.C.
	'D1.7' :  55, #PA23
	'D1.8' :  56, #PA24
	'D1.9' :   0, #5V0
	'D1.10':   0, #GND
	'D2.1' :   0, #3V3
	'D2.2' :  63, #PA31
	'D2.3' :  62, #PA30
	'D2.4' :  61, #PA29
	'D2.5' :  60, #PA28
	'D2.6' :  59, #PA27
	'D2.7' :  58, #PA26
	'D2.8' :  57, #PA25
	'D2.9' :  94, #PB30
	'D2.10':   0, #GND
	'D3.1' :   0, #3V3
	'D3.2' :  68, #PB4
	'D3.3' :  69, #PB5
	'D3.4' :  90, #PB26
	'D3.5' :  91, #PB27
	'D3.6' :  86, #PB22
	'D3.7' :  88, #PB24
	'D3.8' :  89, #PB25
	'D3.9' :  87, #PB23
	'D3.10':   0, #GND
	'D4.1' :   0, #3V3
	'D4.2' :   0, #AVDD
	'D4.3' :   0, #VREF
	'D4.4' :   0, #AGND
	'D4.5' :  96, #PC0
	'D4.6' :  97, #PC1
	'D4.7' :  98, #PC2
	'D4.8' :  99, #PC3
	'D4.9' :   0, #5V0
	'D4.10':   0, #GND
	'D5.1' :   0, #3V3
	'D5.2' :  76, #PB12
	'D5.3' :  77, #PB13
	'D5.4' :  80, #PB16
	'D5.5' :  81, #PB17
	'D5.6' :  82, #PB18
	'D5.7' :  83, #PB19
	'D5.8' :  84, #PB20
	'D5.9' :  85, #PB21
	'D5.10':  0,  #GND
	'D6.1' :   0, #3V3
	'D6.2' :  74, #PB10
	'D6.3' :  75, #PB11
	'D6.4' : 104, #PC8
	'D6.5' : 106, #PC10
	'D6.6' :  95, #PB31
	'D6.7' :  55, #PA23
	'D6.8' :  56, #PA24
	'D6.9' :   0, #5V0
	'D6.10':   0, #GND
	'D7.1' :  0,  #3V3
	'D7.2' :  65, #PB1
	'D7.3' :  64, #PB0
	'D7.4' :  66, #PB2
	'D7.5' :  67, #PB3
	'D7.6' : 101, #PC5
	'D7.7' : 100, #PC4
	'D7.8' :  99, #PC3
	'D7.9' :   0, #5V0
	'D7.10':   0, #GND
	'D8.1' :   0, #3V3
	'D8.2' :  72, #PB8
	'D8.3' :  73, #PB9
	'D8.4' :   0, #N.C.
	'D8.5' :   0, #N.C.
	'D8.6' :   0, #N.C.
	'D8.7' :  55, #PA23
	'D8.8' :  56, #PA24
	'D8.9' :   0, #5V0
	'D8.10':   0, #GND
	'D10.1' :   0, #3V3
	'D10.2' : 118, #PC22
	'D10.3' : 119, #PC23
	'D10.4' : 120, #PC24
	'D10.5' : 121, #PC25
	'D10.6' : 122, #PC26
	'D10.7' :  62, #PA30
	'D10.8' :  63, #PA31
	'D10.9' :   0, #5V0
	'D10.10':   0, #GND
	'D11.1' :   0,  #3V3
	'D11.2' : 112, #PC16
	'D11.3' : 113, #PC17
	'D11.4' : 114, #PC18
	'D11.5' : 115, #PC19
	'D11.6' : 116, #PC20
	'D11.7' : 117, #PC21
	'D11.8' :  98, #PC2
	'D11.9' :  99, #PC3
	'D11.10':   0, #GND
	'D12.1' :   0, #3V3
	'D12.2' : 104, #PC8
	'D12.3' : 105, #PC9
	'D12.4' : 106, #PC10
	'D12.5' : 107, #PC11
	'D12.6' : 108, #PC12
	'D12.7' : 109, #PC13
	'D12.8' : 110, #PC14
	'D12.9' : 111, #PC15
	'D12.10':   0, #GND
	'D13.1' :   0, #3V3
	'D13.2' :  37, #PA5
	'D13.3' :  38, #PA6
	'D13.4' : 123, #PC27
	'D13.5' : 124, #PC28
	'D13.6' : 125, #PC29
	'D13.7' :  96, #PC0
	'D13.8' :  97, #PC1
	'D13.9' :   0, #5V0
	'D13.10':   0, #GND
	'D14.1' :   0, #3V3
	'D14.2' :   0, #3V3
	'D14.3' :   0, #VREF
	'D14.4' :   0, #GND
	'D14.5' :  75, #PB11
	'D14.6' :  76, #PB12
	'D14.7' :  77, #PB13
	'D14.8' :  78, #PB14
	'D14.9' :   0, #5V0
	'D14.10':   0, #GND
	'D15.1' :   0, #3V3
	'D15.2' :  44, #PA12
	'D15.3' :  43, #PA11
	'D15.4' :  45, #PA13
	'D15.5' :  46, #PA14
	'D15.6' :  39, #PA7
	'D15.7' :  33, #PA1
	'D15.8' :   0, #N.C.
	'D15.9' :   0, #5V0
	'D15.10':   0, #GND
	'D16.1' :   0, #3V3
	'D16.2' :  61, #PA29
	'D16.3' :  59, #PA27
	'D16.4' :  56, #PA24
	'D16.5' :  57, #PA25
	'D16.6' :  58, #PA26
	'D16.7' :  62, #PA30
	'D16.8' :  63, #PA31.
	'D16.9' :  60, #PA28
	'D16.10':   0, #GND
}

pinmode = {
	"OUTPUT" : "low",
	"LOW" : "low",
	"HIGH" : "high",
	"INPUT" : "in",
}

pinlevel = {
	"HIGH" : 1,
	"LOW"  : 0,
}

def get_gpio_path(kernel_id):
	global legacy_id
	kernel_id=kernel_id-32	
	
	if (legacy_id==True):
		iopath="/sys/class/gpio/gpio%d" % (kernel_id+32)
		
	if (legacy_id==False):
		iopath="/sys/class/gpio/pio" 
		if kernel_id>=0 and kernel_id<=31:
			iopath="%sA%d" % (iopath,kernel_id-0)
		if kernel_id>=32 and kernel_id<=63:
			iopath="%sB%d" % (iopath,kernel_id-32)
		if kernel_id>=64 and kernel_id<=95:
			iopath="%sC%d" % (iopath,kernel_id-64)
			
	return iopath		
			

def get_kernel_id(connector_name,pin_number):
	return connectors[connector_name][pin_number]

def export(kernel_id):
	global legacy_id

	iopath=get_gpio_path(kernel_id)
	if not os.path.exists(iopath): 
		f = open('/sys/class/gpio/export','w')
		if (legacy_id==True):
			f.write(str(kernel_id))
		else:
			f.write(str(kernel_id-32))
		f.close()

def unexport(kernel_id):
	global legacy_id

	iopath=get_gpio_path(kernel_id)
	if os.path.exists(iopath): 
		f = open('/sys/class/gpio/unexport','w')
		if (legacy_id==True):
			f.write(str(kernel_id))
		else:
			f.write(str(kernel_id-32))
		f.close()

def direction(kernel_id,direct):
	iopath=get_gpio_path(kernel_id)
	if os.path.exists(iopath): 
		f = open(iopath + '/direction','w')
		f.write(direct)
		f.close()

def set_value(kernel_id,value):
	iopath=get_gpio_path(kernel_id)
	if os.path.exists(iopath): 
		f = open(iopath + '/value','w')
		f.write(str(value))
		f.close()

def get_value(kernel_id):
	if kernel_id<>-1:
		iopath=get_gpio_path(kernel_id)
		if os.path.exists(iopath): 
			f = open(iopath + '/value','r')
			a=f.read()
			f.close()
			return int(a)

def set_edge(kernel_id,value):
	iopath=get_gpio_path(kernel_id)
	if os.path.exists(iopath): 
		if value in ('none', 'rising', 'falling', 'both'):
		    f = open(iopath + '/edge','w')
		    f.write(value)
		    f.close()

def soft_pwm_export(kernel_id):
	iopath='/sys/class/soft_pwm/pwm' + str(kernel_id)
	if not os.path.exists(iopath): 
		f = open('/sys/class/soft_pwm/export','w')
		f.write(str(kernel_id))
		f.close()

def soft_pwm_period(kernel_id,value):
	iopath='/sys/class/soft_pwm/pwm' + str(kernel_id)
	if os.path.exists(iopath): 
		f = open(iopath + '/period','w')
		f.write(str(value))
		f.close()

def soft_pwm_pulse(kernel_id,value):
	iopath='/sys/class/soft_pwm/pwm' + str(kernel_id)
	if os.path.exists(iopath): 
		f = open(iopath + '/pulse','w')
		f.write(str(value))
		f.close()

def soft_pwm_steps(kernel_id,value):
	iopath='/sys/class/soft_pwm/pwm' + str(kernel_id)
	if os.path.exists(iopath): 
		f = open(iopath + '/pulses','w')
		f.write(str(value))
		f.close()

class Pin():
	"""
	FOX and AriaG25 pins related class
	"""
	kernel_id=None
	fd=None


	def __init__(self,pin,mode):
		self.kernel_id=pin2kid[pin]
		export(self.kernel_id)
		direction(self.kernel_id,pinmode[mode])

		iopath=get_gpio_path(self.kernel_id)
		if os.path.exists(iopath): 
			self.fd = open(iopath + '/value','r')

#	def __init__(self,connector_id,pin_name,direct="low"):
#		self.kernel_id=get_kernel_id(connector_id,pin_name)
#		export(self.kernel_id)
#		direction(self.kernel_id,direct)

#		iopath=get_gpio_path(self.kernel_id)
#		if os.path.exists(iopath): 
#			self.fd = open(iopath + '/value','r')

	def digitalWrite(self,level):
		set_value(self.kernel_id,pinlevel[level])

	def high(self):
		set_value(self.kernel_id,1)
		
	def low(self):
		set_value(self.kernel_id,0)

	def on(self):
		set_value(self.kernel_id,1)
		
	def off(self):
		set_value(self.kernel_id,0)

	def set_value(self,value):
		return set_value(self.kernel_id,value)

	def get_value(self):
		return get_value(self.kernel_id)

	def wait_edge(self,fd,callback,debouncingtime):
		debouncingtime=debouncingtime/1000.0 # converto in millisecondi
		timestampprec=time.time()
		counter=0
		po = select.epoll()
		po.register(fd,select.EPOLLET)
		while True:
			events = po.poll()
			timestamp=time.time()
			if (timestamp-timestampprec>debouncingtime) and counter>0:
				callback()
			counter=counter+1
			timestampprec=timestamp

	def set_edge(self,value,callback,debouncingtime=0):
		if self.fd!=None:
			set_edge(self.kernel_id,value)
			thread.start_new_thread(self.wait_edge,(self.fd,callback,debouncingtime))
			return
		else:		
			thread.exit()


class Daisy2():

	"""
	DAISY-2 Stepper motor controller
	http://www.acmesystems.it/DAISY-2
	"""

	ENABLE_kernel_id=-1
	DIR_kernel_id=-1
	STEP_kernel_id=-1
	LOWPOWER_kernel_id=-1

	control_line_A = {
		'ENABLE'   :  '2',
		'DIR'      :  '4',
		'STEP'     :  '6',
		'LOWPOWER' :  '8',
	}

	control_line_B = {
		'ENABLE'   :  '3',
		'DIR'      :  '5',
		'STEP'     :  '7',
		'LOWPOWER' :  '9',
	}

	def __init__(self,connector_id,S1="A",period=1400,pulse=700):
		if (S1=="A"):
			self.ENABLE_kernel_id = get_kernel_id(connector_id,self.control_line_A["ENABLE"])
			self.DIR_kernel_id = get_kernel_id(connector_id,self.control_line_A["DIR"])
			self.STEP_kernel_id = get_kernel_id(connector_id,self.control_line_A["STEP"])
			self.LOWPOWER_kernel_id = get_kernel_id(connector_id,self.control_line_A["LOWPOWER"])
		
		if (S1=="B"):
			self.ENABLE_kernel_id = get_kernel_id(connector_id,self.control_line_B["ENABLE"])
			self.DIR_kernel_id = get_kernel_id(connector_id,self.control_line_B["DIR"])
			self.STEP_kernel_id = get_kernel_id(connector_id,self.control_line_B["STEP"])
			self.LOWPOWER_kernel_id = get_kernel_id(connector_id,self.control_line_B["LOWPOWER"])

		export(self.ENABLE_kernel_id)
		export(self.DIR_kernel_id)
		unexport(self.STEP_kernel_id)
		soft_pwm_export(self.STEP_kernel_id)
		export(self.LOWPOWER_kernel_id)

		direction(self.ENABLE_kernel_id,'high')
		direction(self.DIR_kernel_id,'low')
		direction(self.LOWPOWER_kernel_id,'low')

		self.steps(0)
		self.period(period)
		self.pulse(pulse)

	def direction(self,value):
		set_value(self.DIR_kernel_id,value)
		
	def enable(self):
		set_value(self.ENABLE_kernel_id,0)

	def disable(self):
		set_value(self.ENABLE_kernel_id,1)

	def lowpower(self):
		time.sleep(0.1)
		set_value(self.LOWPOWER_kernel_id,1)

	def hipower(self):
		set_value(self.LOWPOWER_kernel_id,0)
		time.sleep(0.1)

	def period(self,value):
		soft_pwm_period(self.STEP_kernel_id,value)

	def pulse(self,value):
		soft_pwm_pulse(self.STEP_kernel_id,value)

	def steps(self,value):
		soft_pwm_steps(self.STEP_kernel_id,value)

	def stop(self):
		soft_pwm_steps(self.STEP_kernel_id,0)

class Daisy4():

	"""
	DAISY-4 (Relay module) related class
	http://www.acmesystems.it/DAISY-4
	"""
	kernel_id=-1

	dips = {
		'DIP1' :  '2',
		'DIP2' :  '3',
		'DIP3' :  '4',
		'DIP4' :  '5',
		'DIP5' :  '6',
		'DIP6' :  '7',
		'DIP7' :  '8',
		'DIP8' :  '9',
	}

	def __init__(self,connector_id,dip_id):
		pin=self.dips[dip_id]
		self.kernel_id = get_kernel_id(connector_id,pin)

		if (self.kernel_id!=0):
			export(self.kernel_id)
			direction(self.kernel_id,'low')

	def on(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,1)
		else:
			pass

		
	def off(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,0)
		else:
			pass
	
	
class Daisy5():

	"""
	DAISY-5 (8 pushbuttons) related class
	http://www.acmesystems.it/DAISY-5
	"""
	kernel_id=None
	fd=None
	
	buttons = {
		'P1' :  '2',
		'P2' :  '3',
		'P3' :  '4',
		'P4' :  '5',
		'P5' :  '6',
		'P6' :  '7',
		'P7' :  '8',
		'P8' :  '9',
	}

	def __init__(self,connector_id,button_id):
		pin=self.buttons[button_id]
		self.kernel_id = get_kernel_id(connector_id,pin)

		if (self.kernel_id!=None):
			export(self.kernel_id)
			direction(self.kernel_id,'in')

			iopath=get_gpio_path(self.kernel_id)
			if os.path.exists(iopath): 
				self.fd = open(iopath + '/value','r')

	def pressed(self):
		return self.get()

	def get(self):
		if self.fd!=None:
			self.fd.seek(0)
			a=self.fd.read()
			if int(a)==0:
				return False
			else:
				return True
		return False

	def wait_edge(self,fd,callback):
		counter=0	
		po = select.epoll()
		po.register(fd,select.EPOLLET)
		while True:
			events = po.poll()
			if counter>0:	
				callback()
			counter=counter+1

	def set_edge(self,value,callback):
		if self.fd!=None:
			set_edge(self.kernel_id,value)
			thread.start_new_thread(self.wait_edge,(self.fd,callback))
			return
		else:		
			thread.exit()

class Daisy8():

	"""
	DAISY-8 (2 Relay - 2 input module) related class
	http://www.acmesystems.it/DAISY-8
	"""
	kernel_id=-1
	fd=None


	line_first = {
		'RL0' :  '2',
		'RL1' :  '3',
		'IN0' :  '4',
		'IN1' :  '5',
	}

	line_second = {
		'RL0' :  '6',
		'RL1' :  '7',
		'IN0' :  '8',
		'IN1' :  '9',
	}

	def __init__(self,connector="D11",position="first",id="RL0"):
		if (position=="first"): 
			pin=self.line_first[id]
		else:
			pin=self.line_second[id]
			
		self.kernel_id = get_kernel_id(connector,pin)

		if (self.kernel_id!=0 and id[0:2]=="RL"):
			export(self.kernel_id)
			direction(self.kernel_id,'low')

		if (self.kernel_id!=0 and id[0:2]=="IN"):
			export(self.kernel_id)
			direction(self.kernel_id,'in')

			iopath=get_gpio_path(self.kernel_id)
			if os.path.exists(iopath): 
				self.fd = open(iopath + '/value','r')

	def on(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,1)
		else:
			pass
		
	def off(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,0)
		else:
			pass

	def get(self):
		if self.fd!=None:
			self.fd.seek(0)
			a=self.fd.read()
			if int(a)==0:
				return False
			else:
				return True
		return False
			
	def wait_edge(self,fd,callback):
		counter=0	
		po = select.epoll()
		po.register(fd,select.EPOLLET)
		while True:
			events = po.poll()
			if counter>0:	
				callback()
			counter=counter+1

	def set_edge(self,value,callback):
		if self.fd!=None:
			set_edge(self.kernel_id,value)
			thread.start_new_thread(self.wait_edge,(self.fd,callback))
			return
		else:		
			thread.exit()
			


class Daisy10():

	"""
	DAISY-10 (RS422/RS485) related class
	http://www.acmesystems.it/DAISY-10'
	"""

	global serial_ports

	def __init__(self, *args, **kwargs):
		#print serial_ports[kwargs.get('port')]
		kwargs['port'] = serial_ports[kwargs.get('port')]
		Serial.__init__(self, *args, **kwargs)
		self.buf = ''

	def mode(self,mode):
		if mode=="RS485":
			#Read these doc to understand this part
			#http://lxr.free-electrons.com/source/Documentation/serial/serial-rs485.txt
			#http://docs.python.org/2/library/struct.html
			fd=self.fileno()
			serial_rs485 = struct.pack('hhhhhhhh', 1, 0, 0, 0, 0, 0, 0, 0)
			fcntl.ioctl(fd,0x542F,serial_rs485)
		if mode=="RS422":
			fd=self.fileno()
			serial_rs485 = struct.pack('hhhhhhhh', 0, 0, 0, 0, 0, 0, 0, 0)
			fcntl.ioctl(fd,0x542F,serial_rs485)

class Daisy11():

	"""
	DAISY-11 (8 led) related class
	http://www.acmesystems.it/DAISY-11
	"""

	kernel_id=-1

	leds = {
		'L1' :  '2',
		'L2' :  '3',
		'L3' :  '4',
		'L4' :  '5',
		'L5' :  '6',
		'L6' :  '7',
		'L7' :  '8',
		'L8' :  '9',
	}

	def __init__(self,connector_id,led_id):
		pin=self.leds[led_id]
		self.kernel_id = get_kernel_id(connector_id,pin)

		if (self.kernel_id!=0):
			export(self.kernel_id)
			direction(self.kernel_id,'low')


	def on(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,1)
		else:
			pass

		
	def off(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,0)
		else:
			pass

	def get(self):
		if get_value(self.kernel_id):
			return True
		else:
			return False


class Daisy14():

	"""
	DAISY-14 (I2C LCD adapter)
	http://www.acmesystems.it/DAISY-14
	"""

	i2c_bus=-1
	i2c_address = -1
	backled = -1
	rs = -1
	e = -1

	def __init__(self,bus_id=0,i2c_address=0x20):
		self.i2c_address = i2c_address
		self.i2c_bus = smbus.SMBus(bus_id)
		self.rs=Daisy22(bus_id,i2c_address,4)
		self.e=Daisy22(bus_id,i2c_address,5)
		self.rs.off()
		self.e.off()
		time.sleep(0.015)

		#LCD initialization sequence
        #http://web.alfredstate.edu/weimandn/lcd/lcd_initialization/lcd_initialization_index.html

		self.sendnibble(0x03)
		self.sendnibble(0x03)
		self.sendnibble(0x03)
		self.sendnibble(0x02)

		#4 bit interface
		#2 lines display
		self.sendcommand(0x28)

		#Command ENTRY MODE SET
		#Increase 0x02
		#Display is shifted 0x01
		self.sendcommand(0x06+0x02)

		#Command DISPLAY ON/OFF
		#Display ON   0x04
		#Cursor OFF   0x02
		#Blinking OFF 0x01
		self.sendcommand(0x08+0x04)

		#Command DISPLAY CLEAR
		self.sendcommand(0x01)

		self.backled=Daisy22(bus_id,i2c_address,6)
		return

	def e_strobe(self):
		self.e.on()
		self.e.off()
		
	def sendnibble(self,value):
		currentvalue=self.i2c_bus.read_byte(self.i2c_address)
		self.i2c_bus.write_byte(self.i2c_address,value&0x0F|currentvalue&0xF0)
		self.e_strobe()
		return

	def sendcommand(self,value):
		self.rs.off()
		self.sendnibble((value>>4)&0x0F)
		self.sendnibble(value&0x0F)
		return

	def senddata(self,value):
		self.rs.on()
		self.sendnibble((value>>4)&0x0F)
		self.sendnibble(value&0x0F)
		return

	def clear(self):
		"""
		Clear the display content
		"""
		self.sendcommand(0x01)
		time.sleep(0.001)
		return

	def home(self):
		"""
		Place the curson at home position
		"""
		self.sendcommand(0x03)
		time.sleep(0.001)
		return

	def setcurpos(self,x,y):
		if y<0 or y>3:
			return
		if x<0 or x>19:
			return

		if y==0:
			self.sendcommand(0x80+0x00+x)
		if y==1:
			self.sendcommand(0x80+0x40+x)
		if y==2:
			self.sendcommand(0x80+0x14+x)
		if y==3:
			self.sendcommand(0x80+0x54+x)
		return

	def putchar(self,value):
		self.senddata(value)
		return

	def putstring(self,string):
		if len(string)==0:
			return
		if len(string)>20:
			string=string[0:20]

		for char in string:
			self.putchar(ord(char))
		return

	def backlighton(self):
		self.backled.on()
		return

	def backlightoff(self):
		self.backled.off()
		return

class Daisy15():

	"""
	DAISY-15 (4DSystems lcd display) related class
	http://www.acmesystems.it/DAISY-15
	"""

	serial = None

	def __init__(self,connector_id):
		self.serial = serial.Serial(
			port=serial_ports[connector_id], 
			baudrate=9600, 
			timeout=1,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
		)

		self.serial.write("U")		# Autobaud char
		rtc = self.serial.read(1)	# Wait for a reply

		self.serial.write("E")		# Clear screen
		rtc = self.serial.read(1)	# Wait for a reply

	def send(self,col,row,str):
		self.serial.write("s%c%c%c%c%c%s%c" % (int(row),int(col),2,0xFF,0xFF,str,0x00))		
		rtc = self.serial.read(1)

class Daisy18():

	"""
	DAISY-18 (4 mosfet input) related class
	http://www.acmesystems.it/DAISY-18
	"""

	fd=None
	kernel_id=-1

	line_first = {
		'CH1' :  '2',
		'CH2' :  '3',
		'CH3' :  '4',
		'CH4' :  '5',
		'I1'  :  '2',
		'I2'  :  '3',
		'I3'  :  '4',
		'I4'  :  '5'
	}

	line_second = {
		'CH1' :  '6',
		'CH2' :  '7',
		'CH3' :  '8',
		'CH4' :  '9',
		'I1'  :  '6',
		'I2'  :  '7',
		'I3'  :  '8',
		'I4'  :  '9'
	}


	def __init__(self,connector="D11",position="first",id="CH1"):
		if (position=="first"): 
			pin=self.line_first[id]
		else:
			pin=self.line_second[id]
			
		self.kernel_id = get_kernel_id(connector,pin)

		export(self.kernel_id)
		direction(self.kernel_id,'in')

		iopath=get_gpio_path(self.kernel_id)
		if os.path.exists(iopath): 
			self.fd = open(iopath + '/value','r')
		
	def get(self):
		if self.fd!=None:
			self.fd.seek(0)
			a=self.fd.read()
			if int(a)==0:
				return False
			else:
				return True
		return False

	def state(self):
		return self.get()

	def wait_edge(self,fd,callback):
		counter=0	
		po = select.epoll()
		po.register(fd,select.EPOLLET)
		while True:
			events = po.poll()
			if counter>0:	
				callback()
			counter=counter+1

	def set_edge(self,value,callback):
		if self.fd!=None:
			set_edge(self.kernel_id,value)
			thread.start_new_thread(self.wait_edge,(self.fd,callback))
			return
		else:		
			thread.exit()



class Daisy19():

	"""
	DAISY-19 (4 mosfet output) related class
	http://www.acmesystems.it/DAISY-19
	"""

	kernel_id=-1

	outputs_first = {
		'CH1' :  '2',
		'CH2' :  '3',
		'CH3' :  '4',
		'CH4' :  '5',
		'O1'  :  '2',
		'O2'  :  '3',
		'O3'  :  '4',
		'O4'  :  '5',
	}

	outputs_second = {
		'CH1' :  '6',
		'CH2' :  '7',
		'CH3' :  '8',
		'CH4' :  '9',
		'O1'  :  '6',
		'O2'  :  '7',
		'O3'  :  '8',
		'O4'  :  '9',
	}

	def __init__(self,connector_id,position,output_id):
		if (position=="first"): 
			pin=self.outputs_first[output_id]
		else:
			pin=self.outputs_second[output_id]
			
		self.kernel_id = get_kernel_id(connector_id,pin)

		if (self.kernel_id!=0):
			export(self.kernel_id)
			direction(self.kernel_id,'low')


	def on(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,1)
		else:
			pass

	def off(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,0)
		else:
			pass

	def get(self):
		if get_value(self.kernel_id):
			return True
		else:
			return False

class Daisy20():

	"""
	DAISY-20 (ADC module)
	http://www.acmesystems.it/DAISY-20
	"""
	
	maxvoltage=0
	volt_per_point=0
	adcpath="/sys/bus/platform/devices/at91_adc/"

	def __init__(self,maxvoltage=10):
		self.maxvoltage=maxvoltage	
		self.volt_per_point=float(maxvoltage)/float(2**10)
		return

	def get(self,ch=0):
		fd = open(self.adcpath + "chan" + str(ch),"r")
		value = fd.read()
		fd.close()
		return(float(value)*self.volt_per_point)
		

class Daisy22():

	"""
	DAISY-22 (8 bit I2C expander)
	http://www.acmesystems.it/DAISY-22
	"""

	i2c_bus=-1
	i2c_address=-1
	line=-1

	def __init__(self,bus_id=0,address=0x20,line=0):
		self.i2c_bus = smbus.SMBus(bus_id)
		self.i2c_address=address
		self.line=line
		return

	def writebyte(self,value):
   		self.i2c_bus.write_byte(self.i2c_address,value)		
		return

	def readbyte(self):
		return 	self.i2c_bus.read_byte(self.i2c_address)

	def on(self):
		currentvalue=self.i2c_bus.read_byte(self.i2c_address)
   		self.i2c_bus.write_byte(self.i2c_address,currentvalue|1<<self.line)		
		return

	def off(self):
		currentvalue=self.i2c_bus.read_byte(self.i2c_address)
   		self.i2c_bus.write_byte(self.i2c_address,currentvalue&(255-(1<<self.line)))		
		return

	def get(self):
		currentvalue=self.i2c_bus.read_byte(self.i2c_address)
   		self.i2c_bus.write_byte(self.i2c_address,currentvalue|(1<<self.line))		
		linevalue=self.i2c_bus.read_byte(self.i2c_address) & (1<<self.line)
		return linevalue >> self.line

	def pressed(self):
		if self.get()==0:
			return True
		else:
			return False

class Daisy24():

	"""
	DAISY-24 (16x2 LCD module)
	http://www.acmesystems.it/DAISY-24
	"""

	i2c_bus=-1
	lcd_address = 0x3E
	exp_address = -1
	backled = -1
	K0 = -1 
	K1 = -1 
	K2 = -1 
	K3 = -1 

	def __init__(self,bus_id=0,exp_address=0x27):
		self.exp_address = exp_address
		self.i2c_bus = smbus.SMBus(bus_id)
		self.sendcommand(0x38)
		self.sendcommand(0x39)
		self.sendcommand(0x14) #Internal OSC freq
		self.sendcommand(0x72) #Set contrast 
		self.sendcommand(0x54) #Power/ICON control/Contrast set
		self.sendcommand(0x6F) #Follower control
		self.sendcommand(0x0C) #Display ON
		self.clear()
		self.K0=Daisy22(bus_id,exp_address,0)
		self.K1=Daisy22(bus_id,exp_address,1)
		self.K2=Daisy22(bus_id,exp_address,2)
		self.K3=Daisy22(bus_id,exp_address,3)
		self.backled=Daisy22(bus_id,exp_address,4)
		return

	def sendcommand(self,value):
		self.i2c_bus.write_byte_data(self.lcd_address,0x00,value)
		return

	def senddata(self,value):
		self.i2c_bus.write_byte_data(self.lcd_address,0x40,value)
		return

	def clear(self):
		"""
		CLear the display content
		"""
		self.sendcommand(0x01)
		time.sleep(0.001)
		return

	def home(self):
		"""
		Place the curson at home position
		"""
		self.sendcommand(0x03)
		time.sleep(0.001)
		return

	def setcontrast(self,value):
		"""
		Set the display contrast
		value = 0 to 15
		"""
		self.sendcommand(0x70 + value)
		return

	def setdoublefont(self):
		self.sendcommand(0x30 + 0x0C + 0x01)
		return

	def setsinglefont(self):
		self.sendcommand(0x30 + 0x08 + 0x01)
		return

	def setcurpos(self,x,y):
		if y<0 or y>1:
			return
		if x<0 or x>15:
			return

		if y==0:
			self.sendcommand(0x80+0x00+x)
		else:
			self.sendcommand(0x80+0x40+x)
		return

	def putchar(self,value):
		self.senddata(value)
		return

	def putstring(self,string):
		if len(string)==0:
			return
		if len(string)>16:
			string=string[0:16]

		for char in string:
			self.putchar(ord(char))
		return

	def backlighton(self):
		self.backled.on()		
		return

	def backlightoff(self):
		self.backled.off()
		return

	def pressed(self,keyid):
		if keyid==0:
			return self.K0.pressed()
		if keyid==1:
			return self.K1.pressed()
		if keyid==2:
			return self.K2.pressed()
		if keyid==3:
			return self.K3.pressed()

		return False

#--------------------------------------------------------------

w1path = "/sys/bus/w1/devices/w1 bus master"

def w1buslist():

		if not os.path.exists(w1path): 
			print "1-wire bus not found"
			print "Check if the 1-wire bus is installed"
			return

		deviceList = os.listdir(w1path)

#		for deviceId in deviceList:
#			print deviceId

		return [deviceId[3:] for deviceId in deviceList if deviceId[0:2]=="28"]

class DS18B20():

	sensor_path=""

	def __init__(self,w1Id):
		if not os.path.exists(w1path): 
			print "1-wire bus not found"
			return

		self.sensor_path = os.path.join(w1path,"28-" + w1Id)

		if not os.path.exists(self.sensor_path): 
			print "Sensor %s not found" % (w1Id)
			return

#		print self.sensor_path

	def getTemp(self):

		f = open(self.sensor_path + '/w1_slave','r')
		tString=f.read()
		f.close()

		if tString.find("NO")>=0:
			print "Wrong CRC"
			return
			
		p=tString.find("t=")
		return float(tString[p+2:-1])/1000

class DS28EA00():

	sensor_path=""

	def __init__(self,w1Id):
		if not os.path.exists(w1path): 
			print "1-wire bus not found"
			return

		self.sensor_path = os.path.join(w1path,"42-" + w1Id)

		if not os.path.exists(self.sensor_path): 
			print "Sensor %s not found" % (w1Id)
			return

#		print self.sensor_path

	def getTemp(self):

		f = open(self.sensor_path + '/therm','r')
		tString=f.read()
		f.close()

		if tString.find("NO")>=0:
			print "Wrong CRC"
			return
			
		p=tString.find("t=")
		return float(tString[p+2:-1])

