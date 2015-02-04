# ablib.py 
#
# Python functions collection to easily manage the I/O lines and 
# Daisy modules with the following Acme Systems boards:
# ARIETTA G25 SoM (http://www.acmesystems.it/arietta)
# ARIAG25-EK Board (http://www.acmesystems.it/ariag25ek)
# TERRA Board (http://www.acmesystems.it/terra)
# ARIA G25 SoM (http://www.acmesystems.it/aria) 
# ACQUA A5 SoM (http://www.acmesystems.it/acqua)
# FOX Board G20 (http://www.acmesystems.it/FOXG20)
#
# (C) 2014 Sergio Tanzilli <tanzilli@acmesystems.it>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

__version__ = 'v1.0.0'

import os.path
import platform
import smbus
import time
import serial
import fcntl
import struct
import thread
import threading
import select
import math

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
	'D13':  '/dev/ttyS2',
	'D17':  '/dev/ttyS1'
}

#Pin to Kernel ID table
pin2kid = {


#Arietta G25
	'J4.7'   :  55, #PA23
	'J4.8'   :  54, #PA22
	'J4.10'  :  53, #PA21
	'J4.11'  :  56, #PA24
	'J4.12'  :  63, #PA31
	'J4.13'  :  57, #PA25
	'J4.14'  :  62, #PA30
	'J4.15'  :  58, #PA26
	'J4.17'  :  59, #PA27
	'J4.19'  :  60, #PA28
	'J4.21'  :  61, #PA29
	'J4.23'  :  32, #PA0
	'J4.24'  :  33, #PA1
	'J4.25'  :  40, #PA8
	'J4.26'  :  39, #PA7
	'J4.27'  :  38, #PA6
	'J4.28'  :  37, #PA5
	'J4.29'  : 124, #PC28
	'J4.30'  : 123, #PC27
	'J4.31'  : 100, #PC4
	'J4.32'  : 127, #PC31
	'J4.33'  :  99, #PC3
	'J4.34'  :  75, #PB11
	'J4.35'  :  98, #PC2
	'J4.36'  :  76, #PB12
	'J4.37'  :  97, #PC1
	'J4.38'  :  77, #PB13
	'J4.39'  :  96, #PC0
	'J4.40'  :  78, #PB14

#Aria G25
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

#FOX Board G20

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
	
#Daisy modules	
	
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
	'D17.1' :   0, #3V3
	'D17.2' :  32, #PA0
	'D17.3' :  33, #PA1
	'D17.4' :  34, #PA2
	'D17.5' :  35, #PA3
	'D17.6' :  36, #PA4
	'D17.7' :  96, #PC0
	'D17.8' :  97, #PC1
	'D17.9' :   0, #5V0
	'D10.10':   0, #GND

#Acqua A5

	'J1.9'  :   1+32,
	'J1.10'  :   0+32,
	'J1.11'  :   3+32,
	'J1.12'  :   2+32,
	'J1.13'  :   5+32,
	'J1.14'  :   4+32,
	'J1.15'  :   7+32,
	'J1.16'  :   6+32,
	'J1.17'  :   9+32,
	'J1.18'  :   8+32,
	'J1.19'  :  11+32,
	'J1.20'  :  10+32,
	'J1.21'  :  13+32,
	'J1.22'  :  12+32,
	'J1.23'  :  15+32,
	'J1.24'  :  14+32,
	'J1.25'  :  77+32,
	'J1.26'  :  78+32,
	'J1.27'  :  75+32,
	'J1.28'  :  76+32,
	'J1.29'  :  79+32,
	'J1.30'  :  74+32,
	'J1.31'  : 156+32,
	'J1.32'  : 155+32,
	'J1.33'  :  25+32,
	'J1.35'  :  27+32,
	'J1.36'  :  28+32,
	'J1.37'  :  29+32,
	'J1.38'  :  26+32,
	'J1.39'  :  24+32,
	'J1.40'  : 116+32,
	'J1.41'  : 117+32,
	'J1.42'  : 118+32,
	'J1.43'  : 119+32,
	'J1.44'  : 120+32,
	'J1.45'  : 121+32,
	'J1.46'  : 122+32,
	'J1.47'  : 123+32,
	'J1.48'  : 124+32,
	'J1.49'  : 125+32,
	
	 'J2.1'  : 127+32,
	 'J2.2'  : 126+32,
	 'J2.3'  : 115+32,
	 'J2.5'  : 109+32,
	 'J2.6'  : 108+32,
	 'J2.7'  : 107+32,
	 'J2.8'  : 106+32,
	 'J2.9'  : 111+32,
	'J2.10'  : 110+32,
	'J2.11'  : 113+32,
	'J2.12'  : 112+32,
	'J2.13'  :  34+32,
	'J2.14'  : 114+32,
	'J2.15'  :  38+32,
	'J2.16'  :  35+32,
	'J2.17'  :  39+32,
	'J2.18'  :  43+32,
	'J2.19'  :  42+32,
	'J2.23'  :  36+32,
	'J2.25'  :  37+32,
	'J2.29'  :  32+32,
	'J2.31'  :  33+32,
	'J2.32'  :  46+32,
	'J2.33'  :  40+32,
	'J2.34'  :  47+32,
	'J2.35'  :  41+32,
	'J2.36'  :  48+32,
	'J2.37'  :  44+32,
	'J2.38'  :  49+32,
	'J2.39'  :  45+32,
	'J2.40'  :  50+32,
	'J2.42'  :  59+32,
	'J2.43'  :  58+32,
	'J2.44'  :  57+32,
	'J2.45'  :  60+32,
	'J2.46'  :  61+32,

	 'J3.5'  : 145+32, #PE17
	 'J3.6'  : 144+32, #PE16
	 'J3.7'  : 147+32, #PE19
	 'J3.8'  : 146+32, #PE18
	 'J3.9'  : 143+32, #PE15
	'J3.10'  : 151+32, #PE23
	'J3.11'  : 152+32, #PE24
	'J3.12'  : 153+32, #PE25
	'J3.13'  : 154+32, #PE26
	'J3.14'  : 148+32, #PE20
	'J3.15'  :  54+32, #PB22
	'J3.16'  :  55+32, #PB23
	'J3.17'  :  51+32, #PB19
	'J3.18'  :  53+32, #PB21
	'J3.19'  :  56+32, #PB24
	'J3.20'  :  52+32, #PB20
	'J3.22'  :  87+32, #PC23
	'J3.23'  :  89+32, #PC25
	'J3.24'  :  86+32, #PC22
	'J3.25'  :  88+32, #PC24
	'J3.26'  :  90+32, #PC26
	'J3.28'  :  91+32, #PC27
	'J3.29'  :  92+32, #PC28
	'J3.30'  :  94+32, #PC30
	'J3.31'  :  93+32, #PC29
	'J3.32'  :  95+32, #PC31
	'J3.33'  :  17+32, #PA17
	'J3.34'  :  16+32, #PA16
	'J3.35'  :  19+32, #PA19
	'J3.36'  :  18+32, #PA18
	'J3.37'  :  21+32, #PA21
	'J3.38'  :  20+32, #PA20
	'J3.39'  :  23+32, #PA23
	'J3.40'  :  22+32, #PA22
	'J3.41'  :  31+32, #PA31
	'J3.42'  :  30+32, #PA30
	'J3.43'  : 159+32, #PE31
	'J3.44'  : 157+32, #PE29
	'J3.45'  :  80+32, #PC16
	'J3.46'  :  81+32, #PC17
	'J3.47'  :  82+32, #PC18
	'J3.48'  :  83+32, #PC19
	'J3.49'  :  84+32, #PC20
	'J3.50'  :  85+32 #PC21
}

pinmode = {
	"OUTPUT" : "low",
	"LOW" : "low",
	"HIGH" : "high",
	"INPUT" : "in"
}

pinlevel = {
	"HIGH" : 1,
	"LOW"  : 0
}

mcuName2pinname = {
#Arietta G25
    'Arietta_G25' : {
        'PA23' :  'J4.7',
        'PA22' :  'J4.8',
        'PA21' : 'J4.10',
        'PA24' : 'J4.11',
        'PA31' : 'J4.12',
        'PA25' : 'J4.13',
        'PA30' : 'J4.14',
        'PA26' : 'J4.15',
        'PA27' : 'J4.17',
        'PA28' : 'J4.19',
        'PA29' : 'J4.21',
         'PA0' : 'J4.23',
         'PA1' : 'J4.24',
         'PA8' : 'J4.25',
         'PA7' : 'J4.26',
         'PA6' : 'J4.27',
         'PA5' : 'J4.28',
        'PC28' : 'J4.29',
        'PC27' : 'J4.30',
         'PC4' : 'J4.31',
        'PC31' : 'J4.32',
         'PC3' : 'J4.33',
        'PB11' : 'J4.34',
         'PC2' : 'J4.35',
        'PB12' : 'J4.36',
         'PC1' : 'J4.37',
        'PB13' : 'J4.38',
         'PC0' : 'J4.39',
        'PB14' : 'J4.40'
        },

#Daisy modules
    'Daisy' : {
         'PB6' :  'D1.2',
         'PB7' :  'D1.3',
        'PB28' :  'D1.4',
        'PB29' :  'D1.5',
        'PA23' :  'D1.7',
        'PA24' :  'D1.8',

        'PA31' :  'D2.2',
        'PA30' :  'D2.3',
        'PA29' :  'D2.4',
        'PA28' :  'D2.5',
        'PA27' :  'D2.6',
        'PA26' :  'D2.7',
        'PA25' :  'D2.8',
        'PB30' :  'D2.9',

         'PB4' :  'D3.2',
         'PB5' :  'D3.3',
        'PB26' :  'D3.4',
        'PB27' :  'D3.5',
        'PB22' :  'D3.6',
        'PB24' :  'D3.7',
        'PB25' :  'D3.8',
        'PB23' :  'D3.9',

         'PC0' :  'D4.5',
         'PC1' :  'D4.6',
         'PC2' :  'D4.7',
         'PC3' :  'D4.8',

        'PB12' :  'D5.2',
        'PB13' :  'D5.3',
        'PB16' :  'D5.4',
        'PB17' :  'D5.5',
        'PB18' :  'D5.6',
        'PB19' :  'D5.7',
        'PB20' :  'D5.8',
        'PB21' :  'D5.9',

        'PB10' :  'D6.2',
        'PB11' :  'D6.3',
         'PC8' :  'D6.4',
        'PC10' :  'D6.5',
        'PB31' :  'D6.6',
        'PA23' :  'D6.7',
         'PA24' :  'D6.8',

         'PB1' :  'D7.2',
         'PB0' :  'D7.3',
         'PB2' :  'D7.4',
         'PB3' :  'D7.5',
         'PC5' :  'D7.6',
         'PC4' :  'D7.7',
         'PC3' :  'D7.8',

         'PB8' :  'D8.2',
         'PB9' :  'D8.3',
        'PA23' :  'D8.7',
        'PA24' :  'D8.8',

        'PC22' : 'D10.2',
        'PC23' : 'D10.3',
        'PC24' : 'D10.4',
        'PC25' : 'D10.5',
        'PC26' : 'D10.6',
        'PA30' : 'D10.7',
        'PA31' : 'D10.8',

        'PC16' : 'D11.2',
        'PC17' : 'D11.3',
        'PC18' : 'D11.4',
        'PC19' : 'D11.5',
        'PC20' : 'D11.6',
        'PC21' : 'D11.7',
         'PC2' : 'D11.8',
         'PC3' : 'D11.9',

         'PC8' : 'D12.2',
         'PC9' : 'D12.3',
        'PC10' : 'D12.4',
        'PC11' : 'D12.5',
        'PC12' : 'D12.6',
        'PC13' : 'D12.7',
        'PC14' : 'D12.8',
        'PC15' : 'D12.9',

         'PA5' : 'D13.2',
         'PA6' : 'D13.3',
        'PC27' : 'D13.4',
        'PC28' : 'D13.5',
        'PC29' : 'D13.6',
         'PC0' : 'D13.7',
         'PC1' : 'D13.8',

        'PB11' : 'D14.5',
        'PB12' : 'D14.6',
        'PB13' : 'D14.7',
        'PB14' : 'D14.8',

        'PA12' : 'D15.2',
        'PA11' : 'D15.3',
        'PA13' : 'D15.4',
        'PA14' : 'D15.5',
         'PA7' : 'D15.6',
         'PA1' : 'D15.7',

        'PA29' : 'D16.2',
        'PA27' : 'D16.3',
        'PA24' : 'D16.4',
        'PA25' : 'D16.5',
        'PA26' : 'D16.6',
        'PA30' : 'D16.7',
        'PA31' : 'D16.8',
        'PA28' : 'D16.9',

         'PA0' : 'D17.2',
         'PA1' : 'D17.3',
         'PA2' : 'D17.4',
         'PA3' : 'D17.5',
         'PA4' : 'D17.6',
         'PC0' : 'D17.7',
         'PC1' : 'D17.8'
    },
    
#Acqua A5
    'Acqua_A5' : {
         'PA1' :  'J1.9',
         'PA0' : 'J1.10',
         'PA3' : 'J1.11',
         'PA2' : 'J1.12',
         'PA5' : 'J1.13',
         'PA4' : 'J1.14',
         'PA7' : 'J1.15',
         'PA6' : 'J1.16',
         'PA9' : 'J1.17',
         'PA8' : 'J1.18',
        'PA11' : 'J1.19',
        'PA10' : 'J1.20',
        'PA13' : 'J1.21',
        'PA12' : 'J1.22',
        'PA15' : 'J1.23',
        'PA14' : 'J1.24',
        'PC13' : 'J1.25',
        'PC14' : 'J1.26',
        'PC11' : 'J1.27',
        'PC12' : 'J1.28',
        'PC15' : 'J1.29',
        'PC10' : 'J1.30',
        'PE28' : 'J1.31',
        'PE27' : 'J1.32',
        'PA25' : 'J1.33',
        'PA27' : 'J1.35',
        'PA28' : 'J1.36',
        'PA29' : 'J1.37',
        'PA26' : 'J1.38',
        'PA24' : 'J1.39',
        'PD20' : 'J1.40',
        'PD21' : 'J1.41',
        'PD22' : 'J1.42',
        'PD23' : 'J1.43',
        'PD24' : 'J1.44',
        'PD25' : 'J1.45',
        'PD26' : 'J1.46',
        'PD27' : 'J1.47',
        'PD28' : 'J1.48',
        'PD29' : 'J1.49',

        'PD31' :  'J2.1',
        'PD30' :  'J2.2',
        'PD19' :  'J2.3',
        'PD13' :  'J2.5',
        'PD12' :  'J2.6',
        'PD11' :  'J2.7',
        'PD10' :  'J2.8',
        'PD15' :  'J2.9',
        'PD14' : 'J2.10',
        'PD17' : 'J2.11',
        'PD16' : 'J2.12',
         'PB2' : 'J2.13',
        'PD18' : 'J2.14',
         'PB6' : 'J2.15',
         'PB3' : 'J2.16',
         'PB7' : 'J2.17',
        'PB11' : 'J2.18',
        'PB10' : 'J2.19',
         'PB4' : 'J2.23',
         'PB5' : 'J2.25',
         'PB0' : 'J2.29',
         'PB1' : 'J2.31',
        'PB14' : 'J2.32',
         'PB8' : 'J2.33',
        'PB15' : 'J2.34',
         'PB9' : 'J2.35',
        'PB16' : 'J2.36',
        'PB12' : 'J2.37',
        'PB17' : 'J2.38',
        'PB13' : 'J2.39',
        'PB18' : 'J2.40',
        'PB27' : 'J2.42',
        'PB26' : 'J2.43',
        'PB25' : 'J2.44',
        'PB28' : 'J2.45',
        'PB29' : 'J2.46',

        'PE17' :  'J3.5',
        'PE16' :  'J3.6',
        'PE19' :  'J3.7',
        'PE18' :  'J3.8',
        'PE15' :  'J3.9',
        'PE23' : 'J3.10',
        'PE24' : 'J3.11',
        'PE25' : 'J3.12',
        'PE26' : 'J3.13',
        'PE20' : 'J3.14',
        'PB22' : 'J3.15',
        'PB23' : 'J3.16',
        'PB19' : 'J3.17',
        'PB21' : 'J3.18',
        'PB24' : 'J3.19',
        'PB20' : 'J3.20',
        'PC23' : 'J3.22',
        'PC25' : 'J3.23',
        'PC22' : 'J3.24',
        'PC24' : 'J3.25',
        'PC26' : 'J3.26',
        'PC27' : 'J3.28',
        'PC28' : 'J3.29',
        'PC30' : 'J3.30',
        'PC29' : 'J3.31',
        'PC31' : 'J3.32',
        'PA17' : 'J3.33',
        'PA16' : 'J3.34',
        'PA19' : 'J3.35',
        'PA18' : 'J3.36',
        'PA21' : 'J3.37',
        'PA20' : 'J3.38',
        'PA23' : 'J3.39',
        'PA22' : 'J3.40',
        'PA31' : 'J3.41',
        'PA30' : 'J3.42',
        'PE31' : 'J3.43',
        'PE29' : 'J3.44',
        'PC16' : 'J3.45',
        'PC17' : 'J3.46',
        'PC18' : 'J3.47',
        'PC19' : 'J3.48',
        'PC20' : 'J3.49',
        'PC21' : 'J3.50'
    }
}

def getVersion ():
	return __version__

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
		if kernel_id>=96 and kernel_id<=127:
			iopath="%sD%d" % (iopath,kernel_id-96)
		if kernel_id>=128 and kernel_id<=159:
			iopath="%sE%d" % (iopath,kernel_id-128)
	return iopath		


def get_kernel_id(connector_name,pin_number):
	return pinname2kernelid(connector_name + "." +pin_number)


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

def existI2Cdevice(bus_id,i2c_address):
	i2c_bus = smbus.SMBus(bus_id)
	try:
		i2c_bus.write_byte(i2c_address,0x00)
		return True
	except:
		return False

def pinname2kernelid(pinname):
	"""
	Return the Kernel ID of any Pin using the MCU name
	or the board name
	"""

	offset=-1
	if pinname[0:2]=="PA":
		offset=32+0
	if pinname[0:2]=="PB":
		offset=32+32
	if pinname[0:2]=="PC":
		offset=32+64
	if pinname[0:2]=="PD":
		offset=32+96
	if pinname[0:2]=="PE":
		offset=32+128

	if offset!=-1:
		return offset+int(pinname[2:4])
	else:	
		return pin2kid[pinname]

def readU8(bus,address,reg):
  result = bus.read_byte_data(address, reg)
  return result

def readS8(bus,address,reg):
	result = bus.read_byte_data(address, reg)
	if result > 127: 
		result -= 256
	return result

def readS16(bus,address,register):
	hi = readS8(bus,address,register)
	lo = readU8(bus,address,register+1)
	return (hi << 8) + lo

def readU16(bus,address,register):
	hi = readU8(bus,address,register)
	lo = readU8(bus,address,register+1)
	return (hi << 8) + lo

def write8(bus,address,reg,value):
	bus.write_byte_data(address,reg,value)

class Pin():
	"""
	FOX and AriaG25 pins related class
	"""
	kernel_id=None
	fd=None


	def __init__(self,pin,mode):
		self.kernel_id=pinname2kernelid(pin)
		export(self.kernel_id)
		direction(self.kernel_id,pinmode[mode])

		iopath=get_gpio_path(self.kernel_id)
		if os.path.exists(iopath): 
			self.fd = open(iopath + '/value','r')

	def high(self):
		set_value(self.kernel_id,1)
		
	def low(self):
		set_value(self.kernel_id,0)

	def on(self):
		set_value(self.kernel_id,1)
		
	def off(self):
		set_value(self.kernel_id,0)

	def digitalWrite(self,level):
		set_value(self.kernel_id,pinlevel[level])

	def set_value(self,value):
		return set_value(self.kernel_id,value)

	def digitalRead(self):
		return get_value(self.kernel_id)

	def get_value(self):
		return get_value(self.kernel_id)

	get = get_value

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

## DAISY-4 #############################################################

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
		self.kernel_id = pinname2kernelid(connector_id + "." + pin)

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

## DAISY-5 #############################################################


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
		self.kernel_id = pinname2kernelid(connector_id + "." + pin)

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

## DAISY-7 #############################################################

class Daisy7():

	"""
	DAISY-7 (GPR/MEMS) related class
	http://www.acmesystems.it/DAISY-7
	"""

	# Linear accellerometer registers LIS331DLH
	acc_registers = {
		'WHO_AM_I'			:	0x0F,
		'CTRL_REG1'			:	0x20,
		'CTRL_REG2'			:	0x21,	
		'CTRL_REG3'			:	0x22,	
		'CTRL_REG4'			:	0x23,
		'CTRL_REG5'			:	0x24,	
		'HP_FILTER_RESET'	:	0x25,
		'REFERENCE'			:	0x26,
		'STATUS_REG'		:   0x27,
		'OUT_X_L'			:	0x28,	
		'OUT_X_H'			:	0x29,	
		'OUT_Y_L'			:	0x2A,	
		'OUT_Y_H'			:	0x2B,	
		'OUT_Z_L'			:	0x2C,	
		'OUT_Z_H'			:	0x2D,
		'INT1_CFG'			:	0x30,
		'INT1_SRC'			:	0x31,
		'INT1_THS'			:	0x32,
		'INT1_DURATION'		:	0x33,
		'INT2_CFG'			:	0x34,
		'INT2_SRC' 			:	0x35,
		'INT1_THS'			:	0x36,
		'INT2_DURATION'		:	0x37,

		#I2C Address
		'I2C_ADDR'			: 	0x18,		
	}

	# Gyroscope registers L3G4200D
	gyro_registers = {
		'WHO_AM_I'			:	0x0F,
		'CTRL_REG1'			:	0x20,
		'CTRL_REG2'			:	0x21,	
		'CTRL_REG3'			:	0x22,	
		'CTRL_REG4'			:	0x23,
		'CTRL_REG5'			:	0x24,	
		'REFERENCE'			:	0x25,
		'OUT_TEMP'			:	0x26,
		'STATUS_REG'		:	0x27,
		'OUT_X_L'			:	0x28,	
		'OUT_X_H'			:	0x29,	
		'OUT_Y_L'			:	0x2A,	
		'OUT_Y_H'			:	0x2B,	
		'OUT_Z_L'			:	0x2C,	
		'OUT_Z_H'			:	0x2D,
		'FIFO_CTRL_REG'		:	0x2E,
		'FIFO_SRC_REG'		:	0x2F,
		'INT1_CFG'			:	0x30,
		'INT1_SRC'			:	0x31,
		'INT1_THS_XH'		:	0x32,
		'INT1_THS_XL'		:	0x33,
		'INT1_THS_YH'		:	0x34,
		'INT1_THS_YL'		:	0x35,
		'INT1_THS_ZH'		:	0x36,
		'INT1_THS_ZL'		:	0x37,
		'INT1_DURATION'		:	0x38,

		#I2C Address
		'I2C_ADDR'			: 	0x68,		
	}

	# Compass registers HMC5883L
	compass_registers = {
		'CONF_REG_A'		:	0x00,
		'CONF_REG_B'		:	0x01,
		'MODE_REG'			:	0x02,
		'OUT_X_H'			:	0x03,
		'OUT_X_L'			:	0x04,
		'OUT_Z_H'			:	0x05,
		'OUT_Z_L'			:	0x06,
		'OUT_Y_H'			:	0x07,
		'OUT_Y_L'			:	0x08,
		'STATUS_REG'		:   0x09,
		'ID_REG_A'			:	0x0A,
		'ID_REG_B'			:	0x0B,
		'ID_REG_C'			:	0x0C,
		
		#I2C Address
		'I2C_ADDR'			: 	0x1E,		
	}

	MeasurementContinuous = 0x00
	MeasurementSingleShot = 0x01
	MeasurementIdle = 0x03

	# Barometer registers BMP085
	baro_registers = {
	
		#Registers address
		'CAL_AC1'           :   0xAA,
		'CAL_AC2'			: 	0xAC,
		'CAL_AC3'			:	0xAE,
		'CAL_AC4'			:	0xB0,
		'CAL_AC5'			:	0xB2,
		'CAL_AC6'			:	0xB4,
		'CAL_B1'			:	0xB6,
		'CAL_B2'			:	0xB8,
		'CAL_MB'			:	0xBA,
		'CAL_MC'			:	0xBC,
		'CAL_MD'			:	0xBE,
		'CONTROL'			:	0xF4,
		'TEMPDATA'			:	0xF6,
		'PRESSUREDATA'		:	0xF6,
		'READTEMPCMD'		:	0x2E,
		'READPRESSURECMD'	:	0x34,

		#Buffer for calibration data
		'BUF_AC1' 			:	0,
		'BUF_AC2' 			:	0,
		'BUF_AC3' 			:	0,
		'BUF_AC4' 			:	0,
		'BUF_AC5' 			:	0,
		'BUF_AC6' 			:	0,
		'BUF_B1' 			:	0,
		'BUF_B2' 			:	0,
		'BUF_MB' 			:	0,
		'BUF_MC' 			:	0,
		'BUF_MD' 			:	0,
		
		#Operating mode
		'ULTRALOWPOWER' 	:	0,
		'STANDARD'			:	1,
		'HIGHRES'			: 	2,
		'ULTRAHIGHRES'		: 	3,		
		
		#I2C Address
		'I2C_ADDR'			: 	0x77,		
	}	

	i2c_bus=-1
	acc_address=0x18
	gyro_address=0x68
	compass_address=0x1E
	ser=-1
	mode = baro_registers["STANDARD"]
	
	def __init__(self,connector_id):
		self.ser = serial.Serial(
			port=serial_ports[connector_id], 
			baudrate=115200, 
			timeout=1,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
		)  
		self.ser.flushInput()

		self.i2c_bus = smbus.SMBus(0)
		
		if self.checkChipAdresses()==False:
			raise IOError, "I2C chip not found"
				
		#Accellerometer setup
		#Chip in Normal mode. Turn on all axis
		self.i2c_bus.write_byte_data(self.acc_address,self.acc_registers['CTRL_REG1'],0x27)	

		#Gyroscope setup
		#Chip in Normal mode. Turn on all axis
		self.i2c_bus.write_byte_data(self.gyro_address,self.gyro_registers['CTRL_REG1'],0x0F)
		#Full 2000dps to control REG4
		self.i2c_bus.write_byte_data(self.gyro_address,self.gyro_registers['CTRL_REG4'],0x20)
		
		#Compass setup
		self.compass_setScale(1.3)
		self.compass_setContinuousMode()
		self.compass_setDeclination(9,54)

		#Read the calibration data
		self.baro_getCalibrationData()	
		
		return

	def __str__(self):
		ret_str = ""
		(x, y, z) = self.acc_getAxes()
		ret_str += "Accellerator: "+"\n"       
		ret_str += "  Axis X: "+str(x)+"\n"       
		ret_str += "  Axis Y: "+str(y)+"\n" 
		ret_str += "  Axis Z: "+str(z)+"\n\n" 

		(x, y, z) = self.gyro_getAxes()
		ret_str += "Gyroscope: "+"\n"       
		ret_str += "  Axis X: "+str(x)+"\n"       
		ret_str += "  Axis Y: "+str(y)+"\n" 
		ret_str += "  Axis Z: "+str(z)+"\n\n" 

		(x, y, z) = self.compass_getAxes()
		ret_str += "Compass: "+"\n"       
		ret_str += "  Axis X: "+str(x)+"\n"       
		ret_str += "  Axis Y: "+str(y)+"\n" 
		ret_str += "  Axis Z: "+str(z)+"\n\n" 

		ret_str += "Barometer: "+"\n"       
		ret_str += "  Temperature: "+str(self.baro_getTemperature())+"\n"       
		ret_str += "     Pressure: "+str(self.baro_getPressure())+"\n"       
		ret_str += "     Altitude: "+str(self.baro_getAltitude())+"\n\n"       

		(latitude,longitude) = self.gps_getGoogleCoordinates()
		ret_str += "GPS: "+"\n"       
		ret_str += "  Latidute: "+str(latitude)+"\n"       
		ret_str += "  Longitude: "+str(longitude)+"\n\n" 
		
		return ret_str

	def readNMEAmsg(self):
		self.ser.flushInput()
		return self.ser.readline().replace("\r\n","")
		

	def checkChipAdresses(self):
		rtc=True
		
		try:
			self.i2c_bus.write_byte(self.acc_registers['I2C_ADDR'],self.acc_registers['WHO_AM_I'])		
		except IOError, err:
			print "Accellerometer not found"	
			rtc=False
		
		try:
			self.i2c_bus.write_byte(self.gyro_registers['I2C_ADDR'],self.gyro_registers['WHO_AM_I'])		
		except IOError, err:
			print "Gyroscope not found"	
			rtc=False
			
		return rtc


	#converts 16 bit two's compliment reading to signed int
	def getSignedNumber(self,number):
		if number & (1 << 15):
			return number | ~65535
		else:
			return number & 65535

	# GPS functions
	
	def gps_getGoogleCoordinates(self):
		#Read a line from the GPS chip
		NMEA_line = self.ser.readline()

		#Split the fields in NMEA line
		values=NMEA_line.split(",")

		#Select just the GGA message line with GPS quality indicator = 1
		#(see the GPS datasheet)
		if values[0]=="$GPGGA" and values[6]=="1":
			H=float(values[2][0:2])
			M=float(values[2][2:4])+(float(values[2][5:9])/10000)
			latitude=H+M/60

			H=float(values[4][0:3])
			M=float(values[4][3:5])+(float(values[4][6:10])/10000)
			longitude=H+M/60
			
			return (latitude,longitude)
		else:
			return (-1,-1)

	# ACCELLEROMETER functions

	def acc_getAxes(self):
		while True:
			self.i2c_bus.write_byte(self.acc_address,self.acc_registers['STATUS_REG'])		
			status_reg=self.i2c_bus.read_byte(self.acc_address)		
			if (status_reg&0x08)!=0:
				break	

		#Read X axis value
		self.i2c_bus.write_byte(self.acc_address,self.acc_registers['OUT_X_L'])		
		OUT_X_L=self.i2c_bus.read_byte(self.acc_address)		
		self.i2c_bus.write_byte(self.acc_address,self.acc_registers['OUT_X_H'])		
		OUT_X_H=self.i2c_bus.read_byte(self.acc_address)		

		#Read Y axis value
		self.i2c_bus.write_byte(self.acc_address,self.acc_registers['OUT_Y_L'])		
		OUT_Y_L=self.i2c_bus.read_byte(self.acc_address)		
		self.i2c_bus.write_byte(self.acc_address,self.acc_registers['OUT_Y_H'])		
		OUT_Y_H=self.i2c_bus.read_byte(self.acc_address)		

		#Read Z axis value
		self.i2c_bus.write_byte(self.acc_address,self.acc_registers['OUT_Z_L'])		
		OUT_Z_L=self.i2c_bus.read_byte(self.acc_address)		
		self.i2c_bus.write_byte(self.acc_address,self.acc_registers['OUT_Z_H'])		
		OUT_Z_H=self.i2c_bus.read_byte(self.acc_address)		

		xValue=self.getSignedNumber(OUT_X_H<<8|OUT_X_L)
		yValue=self.getSignedNumber(OUT_Y_H<<8|OUT_Y_L)
		zValue=self.getSignedNumber(OUT_Z_H<<8|OUT_Z_L)

		return (xValue,yValue,zValue)

	# GYRO functions

	def gyro_getAxes(self):
		while True:
			self.i2c_bus.write_byte(self.gyro_address,self.gyro_registers['STATUS_REG'])		
			status_reg=self.i2c_bus.read_byte(self.gyro_address)		
			if (status_reg&0x08)!=0:
				break

		#Read X axis value
		self.i2c_bus.write_byte(self.gyro_address,self.gyro_registers['OUT_X_L'])		
		OUT_X_L=self.i2c_bus.read_byte(self.gyro_address)		
		self.i2c_bus.write_byte(self.gyro_address,self.gyro_registers['OUT_X_H'])		
		OUT_X_H=self.i2c_bus.read_byte(self.gyro_address)		
		xValue=self.getSignedNumber(OUT_X_H<<8 | OUT_X_L)

		#Read Y axis value
		self.i2c_bus.write_byte(self.gyro_address,self.gyro_registers['OUT_Y_L'])		
		OUT_Y_L=self.i2c_bus.read_byte(self.gyro_address)		
		self.i2c_bus.write_byte(self.gyro_address,self.gyro_registers['OUT_Y_H'])		
		OUT_Y_H=self.i2c_bus.read_byte(self.gyro_address)		
		yValue=self.getSignedNumber(OUT_Y_H<<8 | OUT_Y_L)

		#Read Z axis value
		self.i2c_bus.write_byte(self.gyro_address,self.gyro_registers['OUT_Z_L'])		
		OUT_Z_L=self.i2c_bus.read_byte(self.gyro_address)		
		self.i2c_bus.write_byte(self.gyro_address,self.gyro_registers['OUT_Z_H'])		
		OUT_Z_H=self.i2c_bus.read_byte(self.gyro_address)		
		zValue=self.getSignedNumber(OUT_Z_H<<8 | OUT_Z_L)

		xValue=self.getSignedNumber(OUT_X_H<<8|OUT_X_L)
		yValue=self.getSignedNumber(OUT_Y_H<<8|OUT_Y_L)
		zValue=self.getSignedNumber(OUT_Z_H<<8|OUT_Z_L)

		return (xValue,yValue,zValue)

	# BAROMETER functions
	# Some parts of this code become from the Adafruit I2C libraries
	# https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/blob/master/Adafruit_BMP085/Adafruit_BMP085.py

	def baro_getRawTemperature(self):
		self.i2c_bus.write_byte_data(self.baro_registers['I2C_ADDR'],self.baro_registers['CONTROL'],self.baro_registers['READTEMPCMD'])	
		time.sleep(0.005)
		temperature=readU16(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers['TEMPDATA'])		
		return temperature

	def baro_getTemperature(self):
		UT = 0
		X1 = 0
		X2 = 0
		B5 = 0
		temp = 0.0

		# Read raw temp before aligning it with the calibration values
		UT = self.baro_getRawTemperature()
		X1 = ((UT - self.baro_registers["BUF_AC6"]) * self.baro_registers["BUF_AC5"]) >> 15
		X2 = (self.baro_registers["BUF_MC"] << 11) / (X1 + self.baro_registers["BUF_MD"])
		B5 = X1 + X2
		temp = ((B5 + 8) >> 4) / 10.0
		return temp
		
	def baro_getCalibrationData(self):
		self.baro_registers["BUF_AC1"]=readS16(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers['CAL_AC1'])	
		self.baro_registers["BUF_AC2"]=readS16(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers['CAL_AC2'])	
		self.baro_registers["BUF_AC3"]=readS16(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers['CAL_AC3'])	
		self.baro_registers["BUF_AC4"]=readU16(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers['CAL_AC4'])	
		self.baro_registers["BUF_AC5"]=readU16(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers['CAL_AC5'])	
		self.baro_registers["BUF_AC6"]=readU16(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers['CAL_AC6'])	
		self.baro_registers["BUF_B1"]=readS16(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers['CAL_B1'])	
		self.baro_registers["BUF_B2"]=readS16(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers['CAL_B2'])	
		self.baro_registers["BUF_MB"]=readS16(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers['CAL_MB'])	
		self.baro_registers["BUF_MC"]=readS16(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers['CAL_MC'])	
		self.baro_registers["BUF_MD"]=readS16(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers['CAL_MD'])	
		
	def baro_showCalibrationData(self):
		print "CAL_AC1 = %6d" % (self.baro_registers["BUF_AC1"])
		print "CAL_AC2 = %6d" % (self.baro_registers["BUF_AC2"])
		print "CAL_AC3 = %6d" % (self.baro_registers["BUF_AC3"])
		print "CAL_AC4 = %6d" % (self.baro_registers["BUF_AC4"])
		print "CAL_AC5 = %6d" % (self.baro_registers["BUF_AC5"])
		print "CAL_AC6 = %6d" % (self.baro_registers["BUF_AC6"])
		print " CAL_B1 = %6d" % (self.baro_registers["BUF_B1"])
		print " CAL_B2 = %6d" % (self.baro_registers["BUF_B2"])
		print " CAL_MB = %6d" % (self.baro_registers["BUF_MB"])
		print " CAL_MC = %6d" % (self.baro_registers["BUF_MC"])
		print " CAL_MD = %6d" % (self.baro_registers["BUF_MD"])
		  
	def baro_getRawPressure(self):
		write8(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers["CONTROL"], self.baro_registers["READPRESSURECMD"] + (self.mode << 6))

		if (self.mode == self.baro_registers["ULTRALOWPOWER"]):
			time.sleep(0.005)
		elif (self.mode == self.baro_registers["HIGHRES"]):
			time.sleep(0.014)
		elif (self.mode == self.baro_registers["ULTRAHIGHRES"]):
			time.sleep(0.026)
		else:
			time.sleep(0.008)

		msb =  readU8(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers["PRESSUREDATA"])
		lsb =  readU8(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers["PRESSUREDATA"]+1)
		xlsb = readU8(self.i2c_bus,self.baro_registers['I2C_ADDR'],self.baro_registers["PRESSUREDATA"]+2)
		
		raw = ((msb << 16) + (lsb << 8) + xlsb) >> (8 - self.mode)
		return raw		  

	def baro_getPressure(self):
		"Gets the compensated pressure in pascal"
		UT = 0
		UP = 0
		B3 = 0
		B5 = 0
		B6 = 0
		X1 = 0
		X2 = 0
		X3 = 0
		p = 0
		B4 = 0
		B7 = 0

		UT = self.baro_getRawTemperature()
		UP = self.baro_getRawPressure()

		# True Temperature Calculations
		X1 = ((UT - self.baro_registers["CAL_AC6"]) * self.baro_registers["CAL_AC5"]) >> 15
		X2 = (self.baro_registers["CAL_MC"] << 11) / (X1 + self.baro_registers["CAL_MD"])
		B5 = X1 + X2

		# Pressure Calculations
		B6 = B5 - 4000
		X1 = (self.baro_registers["CAL_B2"] * (B6 * B6) >> 12) >> 11
		X2 = (self.baro_registers["CAL_AC2"] * B6) >> 11
		X3 = X1 + X2
		B3 = (((self.baro_registers["CAL_AC1"] * 4 + X3) << self.mode) + 2) / 4

		X1 = (self.baro_registers["CAL_AC3"] * B6) >> 13
		X2 = (self.baro_registers["CAL_B1"] * ((B6 * B6) >> 12)) >> 16
		X3 = ((X1 + X2) + 2) >> 2
		B4 = (self.baro_registers["CAL_AC4"] * (X3 + 32768)) >> 15
		B7 = (UP - B3) * (50000 >> self.mode)


		if (B7 < 0x80000000):
			p = (B7 * 2) / B4
		else:
			p = (B7 / B4) * 2
      
		X1 = (p >> 8) * (p >> 8)
		X1 = (X1 * 3038) >> 16
		X2 = (-7357 * p) >> 16

		p = p + ((X1 + X2 + 3791) >> 4)

		return p

	def baro_getAltitude(self, seaLevelPressure=101325):
		"Calculates the altitude in meters"
		altitude = 0.0
		pressure = float(self.baro_getPressure())
		altitude = 44330.0 * (1.0 - pow(pressure / seaLevelPressure, 0.1903))
		return altitude
		  
	# COMPASS functions

	#Part of this code become from Think Bowl I2C Libraries
	#http://think-bowl.com/raspberry-pi/installing-the-think-bowl-i2c-libraries-for-python/
		
	def compass_setContinuousMode(self):
		self.setOption(self.compass_registers["MODE_REG"], self.MeasurementContinuous)
		
	def compass_setScale(self, gauss):
		if gauss == 0.88:
			self.scale_reg = 0x00
			self.scale = 0.73
		elif gauss == 1.3:
			self.scale_reg = 0x01
			self.scale = 0.92
		elif gauss == 1.9:
			self.scale_reg = 0x02
			self.scale = 1.22
		elif gauss == 2.5:
			self.scale_reg = 0x03
			self.scale = 1.52
		elif gauss == 4.0:
			self.scale_reg = 0x04
			self.scale = 2.27
		elif gauss == 4.7:
			self.scale_reg = 0x05
			self.scale = 2.56
		elif gauss == 5.6:
			self.scale_reg = 0x06
			self.scale = 3.03
		elif gauss == 8.1:
			self.scale_reg = 0x07
			self.scale = 4.35
		
		self.scale_reg = self.scale_reg << 5
		self.setOption(self.compass_registers["CONF_REG_B"], self.scale_reg)
		
	def compass_setDeclination(self, degree, min = 0):
		self.declinationDeg = degree
		self.declinationMin = min
		self.declination = (degree+min/60) * (math.pi/180)
		
	def setOption(self, register, *function_set):
		options = 0x00
		for function in function_set:
			options = options | function
		self.i2c_bus.write_byte_data(self.compass_address,register, options)
		
	# Adds to existing options of register	
	def addOption(self, register, *function_set):
		options = self.i2c_bus.read_byte_data(self.compass_address,register)
		for function in function_set:
			options = options | function
		self.i2c_bus.write_byte_data(self.compass_address,register, options)
		
	# Removes options of register	
	def removeOption(self, register, *function_set):
		options = self.i2c_bus.read_byte_data(self.compass_address,register)
		for function in function_set:
			options = options & (function ^ 0b11111111)
		self.i2c_bus.write_byte_data(self.compass_address,register, options)
		
	def compass_getDeclination(self):
		return (self.declinationDeg, self.declinationMin)
	
	def compass_getDeclinationString(self):
		return str(self.declinationDeg)+"\u00b0 "+str(self.declinationMin)+"'"
	
	# Returns heading in degrees and minutes
	def compass_getHeading(self):
		(scaled_x, scaled_y, scaled_z) = self.compass_getAxes()
		
		headingRad = math.atan2(scaled_y, scaled_x)
		headingRad += self.declination

		# Correct for reversed heading
		if(headingRad < 0):
			headingRad += 2*math.pi
			
		# Check for wrap and compensate
		if(headingRad > 2*math.pi):
			headingRad -= 2*math.pi
			
		# Convert to degrees from radians
		headingDeg = headingRad * 180/math.pi
		degrees = math.floor(headingDeg)
		minutes = round(((headingDeg - degrees) * 60))
		return (degrees, minutes)
	
	def compass_getHeadingString(self):
		(degrees, minutes) = self.compass_getHeading()
		return str(degrees)+"\u00b0 "+str(minutes)+"'"
		
	def compass_getAxes(self):
		#Read X axis value
		self.i2c_bus.write_byte(self.compass_address,self.compass_registers['OUT_X_L'])		
		OUT_X_L=self.i2c_bus.read_byte(self.compass_address)		
		self.i2c_bus.write_byte(self.compass_address,self.compass_registers['OUT_X_H'])		
		OUT_X_H=self.i2c_bus.read_byte(self.compass_address)		
		xValue=self.getSignedNumber(OUT_X_H<<8 | OUT_X_L)

		#Read Y axis value
		self.i2c_bus.write_byte(self.compass_address,self.compass_registers['OUT_Y_L'])		
		OUT_Y_L=self.i2c_bus.read_byte(self.compass_address)		
		self.i2c_bus.write_byte(self.compass_address,self.compass_registers['OUT_Y_H'])		
		OUT_Y_H=self.i2c_bus.read_byte(self.compass_address)		
		yValue=self.getSignedNumber(OUT_Y_H<<8 | OUT_Y_L)

		#Read Z axis value
		self.i2c_bus.write_byte(self.compass_address,self.compass_registers['OUT_Z_L'])		
		OUT_Z_L=self.i2c_bus.read_byte(self.compass_address)		
		self.i2c_bus.write_byte(self.compass_address,self.compass_registers['OUT_Z_H'])		
		OUT_Z_H=self.i2c_bus.read_byte(self.compass_address)		
		zValue=self.getSignedNumber(OUT_Z_H<<8 | OUT_Z_L)
		
		if (xValue == -4096):
			xValue = None
		else:
			xValue = round(xValue * self.scale, 4)
			
		if (yValue == -4096):
			yValue = None
		else:
			yValue = round(yValue * self.scale, 4)
			
		if (zValue == -4096):
			zValue = None
		else:
			zValue = round(zValue * self.scale, 4)
			
		return (xValue, yValue, zValue)

## DAISY-8 #############################################################

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
			
		self.kernel_id = pinname2kernelid(connector + "." + pin)

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
			
## DAISY-10 ############################################################

class Daisy10():

	"""
	DAISY-10 (RS422/RS485) related class
	http://www.acmesystems.it/DAISY-10
	"""

	global serial_ports
	serial = None
	fd=None
	timeout = 0

	def __init__(self, *args, **kwargs):
		#print serial_ports[kwargs.get('port')]
		kwargs['port'] = serial_ports[kwargs.get('port')]
		self.serial = serial.Serial(*args, **kwargs)
		#Serial.__init__(self, *args, **kwargs)
		self.buf = ''
		self.timeout = self.serial.timeout

	def mode(self,mode):
		if mode=="RS485":
			#Read these doc to understand this part
			#http://lxr.free-electrons.com/source/Documentation/serial/serial-rs485.txt
			#http://docs.python.org/2/library/struct.html
			fd=self.serial.fileno()
			serial_rs485 = struct.pack('hhhhhhhh', 1, 0, 0, 0, 0, 0, 0, 0)
			fcntl.ioctl(fd,0x542F,serial_rs485)
		if mode=="RS422":
			fd=self.serial.fileno()
			serial_rs485 = struct.pack('hhhhhhhh', 0, 0, 0, 0, 0, 0, 0, 0)
			fcntl.ioctl(fd,0x542F,serial_rs485)
	
	def flushInput(self):
		self.serial.flushInput()
    
	def write(self, msg):
		self.serial.write(msg)
		
	def read(self, num_bytes):
		self.serial.read(num_bytes)
    


## DAISY-11 ############################################################

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
		self.kernel_id = pinname2kernelid(connector_id + "." + pin)

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

## DAISY-14 ############################################################

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

## DAISY-15 ############################################################

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

## DAISY-18 ############################################################

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
			
		self.kernel_id = pinname2kernelid(connector + "." + pin)

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

## DAISY-19 ############################################################

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
		'O4'  :  '5'
	}

	outputs_second = {
		'CH1' :  '6',
		'CH2' :  '7',
		'CH3' :  '8',
		'CH4' :  '9',
		'O1'  :  '6',
		'O2'  :  '7',
		'O3'  :  '8',
		'O4'  :  '9'
	}

	def __init__(self,connector_id,position,output_id):
		if (position=="first"): 
			pin=self.outputs_first[output_id]
		else:
			pin=self.outputs_second[output_id]
			
		self.kernel_id = pinname2kernelid(connector_id + "." + pin)

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

## DAISY-20 ############################################################

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
		
## DAISY-22 ############################################################

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
## DAISY-24 ############################################################

class Daisy24():

	"""
	DAISY-24 (16x2 LCD module)
	http://www.acmesystems.it/DAISY-24
	"""

	i2c_bus=-1

	lcd_address = 0x3E

	# I2C expansion address can be:
	# PCF8574T  0x27
	# PCF8574AT 0x3F 
	exp_address = 0x27

	backled = -1
	K0 = -1 
	K1 = -1 
	K2 = -1 
	K3 = -1 

	def __init__(self,bus_id=0,exp_address=-1):
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

		#if (exp_address==-1):
		#	try:
		#		self.K0=Daisy22(bus_id,exp_address,0)
		#	catch:	

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

