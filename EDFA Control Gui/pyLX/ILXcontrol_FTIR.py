# A class enclosing relevant serial commands to the ILX 16-Ch diode controller
# for pumping EDFAs (& the FTIR CW reference).
# Called by ILX_GUI_FTIR.py for graphically commanding the controller.
#
# Serial commands replaced by print-outs for testing purposes.
#
# To do:
# - Adjust injected time delays depending on ILX response time.
#
# Jay Rutledge, 10.20.2022

import serial
import time
import numpy as np

# ---------------------------------------------------------
# Define the class
class ILXcontrol:           # To create an instance of this class: ilx = ILXcontrol()

    # ---------------------------------------------------------
    # Initialize the class instance

    def __init__(self):
       print("init")
       self.sleeptime = 1
       self.init_serial()
       self.init_amps()
       self.init_Ilim()
       self.beep()

    # ---------------------------------------------------------
    # Initialize properties: serial connection and amplifier diode channels/currents.

    def init_serial(self):
        self.testmode = False # True = testing; False = real serial connection
        self.serialpath = "COM1"  # Specify path to serial-to-usb port where device is plugged.
        # self.serialpath = "COM4" # Test direct serial port connection

        # -------------------------------------------------------------
        # Initiate serial connections
        if self.testmode == False:
            self.s = serial.Serial(self.serialpath, baudrate = 19200, timeout = 2, rtscts = False)  # Open the serial connection to specified path = here/is/port
            print(self.s)
            print('The path to serial device is '+self.s.name)
            # self.s.baudrate = 9600  # Matched with ILX baudrate. Otherwise, communication fails.

            if self.s.is_open == True:  # Output ‘true’ verifies that the port is indeed open
                print('Successfully established initial serial connection.')
            if self.s.is_open == False:
                print('Failed to establish initial serial connection.')
        else:
            print('Program in testing mode; no real serial connection attempted.')
            self.s = serial.Serial(self.serialpath)  # Open the serial connection to specified path = here/is/port


    def init_amps(self):
        # Initialize in this separated way so that channels/currents may be
        # updated in hindsight with update_amps().

        # preAmp
        self.preAmp_channels_fwd = [16]
        self.preAmp_channels_bwd = []
        self.preAmp_channels = self.preAmp_channels_fwd + self.preAmp_channels_bwd
        print('The pre-set preAmp channels are fwd: '+str(self.preAmp_channels)+' and bwd: '+str(self.preAmp_channels_bwd)+ '.')

        self.preAmp_currents_fwd = [0]
        self.preAmp_currents_bwd = []
        self.preAmp_currents =   self.preAmp_currents_fwd + self.preAmp_currents_bwd
        print('The pre-set preAmp currents are '+str(self.preAmp_currents)+' mA.')

    def init_Ilim(self):

        if self.testmode == False:
            print('setting diode current limits, non-testing mode')
            self.Ilim_set_3S = 1300.0
            # for ch in [16,15]:
            #     lim_bytes = 'CHANNEL {:d};LAS:LIM:I {:.1f};\n'.format(
            #             ch, self.Ilim_set_3S).encode('ascii')
            #     self.s.write(lim_bytes)
            lim_bytes = 'CHAN ALL;LAS:LIM:I 100.0;\n'.encode('ascii')
            # self.s.write(b'CHANNEL ALL;LAS:LIM:I 1300.0;\n') # (Note: Change this from 'ALL' to {[1,2],[3], [7,8]})
            self.s.write(lim_bytes)
            print('way point 1')
            time.sleep(self.sleeptime)
            # readbytes = 'CHANNEL 16;LAS:LIM:I?;\n'.encode('ascii')
            readbytes = 'ALLCOND?;\n'.encode('ascii')
            self.s.write(readbytes)  # Choose a representative
            self.s.write(readbytes)
            time.sleep(3)
            print(self.s.inWaiting())
            print('way point 2')
            time.sleep(self.sleeptime)
            print('way point 2.5')
            self.Ilim_3S = self.s.readline() # THIS IS THE PROBLEM LINE
            print(self.Ilim_3S)
            print('way point 3')
            time.sleep(self.sleeptime)
            print('way point 4')
            Ilim_3S_str = self.Ilim_3S.decode().strip()
            print('way point 5')
            print('All 3S diode channel LAS current limits set to '+Ilim_3S_str+' mA')
        else:
            print('setting diode current limits, testing mode')


    def update_amps(self):

        self.preAmp_channels = self.preAmp_channels_fwd + self.preAmp_channels_bwd
        self.preAmp_currents = self.preAmp_channels_fwd + self.preAmp_channels_bwd
        print('The pre-set EDFA1 channels are now fwd/bwd: '+str(self.preAmp_channels)+'.')



    # ---------------------------------------------------------
    # Open/close serial port connection (anytime after the opening at time of __init__)

    def check_serial(self):
        if self.testmode == False:
            if self.s.is_open == True:
                print('The serial connection is open.')
            if self.s.is_open == False:
                print('The serial connection is closed.')
        else:
            print("No serial connection attempted in testing mode.")

    def open_serial(self):
        if self.testmode == False:
            if self.s.is_open == True:
                print('Error: Connection already open.')
            else:
                self.s.open()
                if self.s.is_open == True:  # Should be true
                    print('Connected ILX serial port.')
                if self.s.is_open == False:
                    print('Error: Failed to connect ILX serial port')

    def close_serial(self):
        #self.EDFA1_currents = [0, 0, 0, 0]
        #self.preAmp_currents = [0]
        #self.EDFA1_off()
        #self.preAmp_off()
        if self.testmode == False:
            if self.s.is_open == False:
                print('Error: Connection already closed.')
            else:
                self.s.close()
                if self.s.is_open == False: # Should be false
                    print("Disconnected ILX serial port.")
                if self.s.is_open == True: # Should be false
                    print("Error: Failed to disconnect ILX serial port.")

    # ---------------------------------------------------------
    # Test beeper

    def beep(self):
        self.s.write(b'BEEP 2;\n')
        print("Beeped :-)")

    # ---------------------------------------------------------
    # Change menu to a different channel
    def menu_ch(self, ch):
        self.s.write(('CHANNEL '+str(ch)+';MENU 1;\n').encode())
        print('Menu changed to Ch. '+str(ch))

    def menu_all(self):
        self.s.write(('MENU 3;\n').encode())
        print('Menu changed to all channel summary.')

    # ---------------------------------------------------------
    # LAS settings ---------------------------------------------------

    def LAS_onoff(self, ch, onoff):
        print('First zero LAS current before turning on/off...')
        self.LDI_setzero(ch)
        time.sleep(self.sleeptime)
        self.s.write(('CHANNEL ' + str(ch) + '; LAS:OUT ' + str(onoff) + ';\n').encode())
        time.sleep(self.sleeptime)
        print('Confirming LAS status...')
        self.LAS_status(ch)
        time.sleep(self.sleeptime)
        if self.LAS_stat_float == 1 and onoff == 1:
            print('Ch.'+str(ch)+' LAS successfully turned on')
        elif self.LAS_stat_float == 0 and onoff == 1:
            print('Ch.'+str(ch)+' LAS failed to turn on.')
        elif self.LAS_stat_float == 0 and onoff == 0:
            print('Ch.' + str(ch) + ' LAS successfully turned off.')
        elif self.LAS_stat_float == 1 and onoff == 0:
            print('Ch.' + str(ch) + ' LAS failed to turn off.')
        # if onoff == 1 and ch >= 1 and ch <= 12:
        #     self.s.write(('CHANNEL '+str(ch)+'; LAS:OUT '+str(onoff)+';\n').encode())
        #     print('Ch.'+str(ch)+' LAS turned on')
        # elif onoff == 0 and ch >= 1 and ch <= 12:
        #     # s.write(b'CHANNEL 1; LAS:OUT 0;\n')
        #     print('Ch.'+str(ch)+' LAS turned off')
        # else:
        #     print('Error: Expected LAS_onoff(channel = integer 1-12, onoff = boolean).')
        self.beep()

    def LAS_status(self, ch):
        self.s.write(('CHANNEL '+str(ch)+'; LAS:OUT?;\n').encode())
        time.sleep(self.sleeptime)
        LAS_stat_byte = self.s.readline()
        LAS_stat_str = LAS_stat_byte.decode().strip()
        self.LAS_stat_float = float(LAS_stat_str)
        if self.LAS_stat_float == 0:
            print('Ch.'+str(ch)+' LAS is off.')
        if self.LAS_stat_float == 1:
            print('Ch.'+str(ch)+' LAS is on.')

    def LDI_set(self, ch, ImA_set):
        print('First check LAS current before re-setting...')
        self.LDI_read(ch)
        time.sleep(self.sleeptime)
        #print('Ch.'+str(ch)+' current before re-setting is '+str(self.ImA_last)+' mA.')
        # --------------------------------------------------------------------------------------------
        # Redundantly ensure current limit is not exceeded:
        above_limit = False
        if ch in [1, 2, 3, 7, 8]:
            if ImA_set >= self.Ilim_set_3S:
                above_limit = True
        elif ch == 10:
            if ImA_set >= self.Ilim_set_aero:
                above_limit = True

        if above_limit:
            print('Error: Target current exceeds maximum current limit')
            return
        # --------------------------------------------------------------------------------------------
        # Step-down current if previous value > 500 mA and target value < 500 mA:
        elif ImA_set > 515 and self.ImA_last < 500:
            self.s.write(('CHANNEL '+str(ch)+'; LAS:LDI 500;\n').encode())
            time.sleep(0.5)
            #self.s.write(('CHANNEL '+str(ch)+'; LAS:LDI '+str(ImA_set)+';\n').encode())
            print('Ch.'+str(ch)+' current stepped up to 500 mA before setting to '+str(ImA_set)+' mA.')
            # self.s.write(('CHANNEL ' + str(ch) + '; LAS:LDI ' + str(ImA_set) + ';\n').encode())
        # --------------------------------------------------------------------------------------------
        # Step-up current if previous value < 500 mA and target value > 500 mA:
        elif ImA_set < 500 and self.ImA_last > 515:
            self.s.write(('CHANNEL ' + str(ch) + '; LAS:LDI 500;\n').encode())
            time.sleep(0.5)
            # self.s.write(('CHANNEL '+str(ch)+'; LAS:LDI '+str(ImA_set)+';\n').encode())
            print('Ch.' + str(ch) + ' current stepped down to 500 mA before setting to ' + str(ImA_set) + ' mA.')
            # self.s.write(('CHANNEL ' + str(ch) + '; LAS:LDI ' + str(ImA_set) + ';\n').encode())
        # --------------------------------------------------------------------------------------------
        # For all other situations:
        # else:
        #     print('Setting Ch.' + str(ch) + ' current in one step:')
        #     self.s.write(('CHANNEL ' + str(ch) + '; LAS:LDI ' + str(ImA_set) + ';\n').encode())
        self.s.write(('CHANNEL ' + str(ch) + '; LAS:LDI ' + str(ImA_set) + ';\n').encode())
        print('Ch.'+str(ch)+' LAS current target set to '+str(ImA_set)+' mA.')
        time.sleep(self.sleeptime)
        print('Confirming LAS current set to target value...')
        self.LDI_read(ch)
        self.beep()

    def LDI_setzero(self, ch):
        print('First check LAS current before zeroing...')
        self.LDI_read(ch)
        time.sleep(self.sleeptime)
        #print('Ch.'+str(ch)+' current before zeroing is'+str(self.ImA_last)+' mA.')
        if self.ImA_last > 500:  # Step diode down if current above 500 mA.
            self.LDI_set(ch, 500)
            time.sleep(self.sleeptime)
            self.LDI_read(ch)
            time.sleep(self.sleeptime)
            print('Ch.'+str(ch)+' LAS current stepped down to'+str(self.ImA_last)+' mA.')
        self.LDI_set(ch, 0)
        time.sleep(self.sleeptime)
        print('Confirming LAS current set to zero...')
        self.LDI_read(ch)
        #print('Ch.'+str(ch)+' current set to 0 mA.')

    def LDI_read(self, ch):
        self.s.write(('CHANNEL '+str(ch)+';LAS:LDI?;\n').encode())
        time.sleep(0.25)
        ImA_byte = self.s.readline()
        ImA_str = ImA_byte.decode().strip()
        self.ImA_last = float(ImA_str)
        print('Ch.'+str(ch)+' LAS current is '+ImA_str+' mA.')

    def LDI_setlim(self, ch, Ilim_mA):
        print('Ch.'+str(ch)+' LAS current limit set to '+str(Ilim_mA)+' mA.')

    # ---------------------------------------------------------
    # TEC settings ---------------------------------------------------

    def TEC_onoff(self, ch, onoff):
        #s.write(b'CHANNEL 1; TEC:OUT 1;\n')
        if onoff == 1:
            print('Ch.'+str(ch)+' TEC turned on')
        elif onoff == 0:
            print('Ch.'+str(ch)+' TEC turned off')
        else:
            print('Error: Expected TEC_onoff(channel = integer, onoff = boolean).')

    def TEC_status(self, ch):
        #s.write(b'CHANNEL 1; LAS 1;\n')
        print('Ch.'+str(ch)+' TEC is ON')

    def TEC_set(self, ch, I_mA):
        print('Ch.'+str(ch)+' TEC current set to '+str(I_mA)+' mA.')

    def TEC_read(self, ch):
        I_mA = 500  # This # actually obtained from serial read.
        print('Ch.'+str(ch)+' TEC current is '+str(I_mA)+' mA.')

    def TEC_setlim(self, ch, Ilim_mA):
        print('Ch.'+str(ch)+' TEC current limit set to '+str(Ilim_mA)+' mA.')




    # -----------------------------------------------------------
    # Turn on/update/off preAmp (Ch. 3)
    def preAmp_on(self):
        i = 0
        for ch in self.preAmp_channels:
            self.LDI_setzero(ch)            # First ensure all diodes are set to zero current.
            time.sleep(self.sleeptime)                   # Wait a moment
            self.LAS_onoff(ch, 1)           # Now turn on LAS
            time.sleep(self.sleeptime)                   # Wait a moment
            self.LDI_set(ch, self.preAmp_currents[i])         # And set currents to specified values.
            time.sleep(self.sleeptime)                   # Wait a moment
            i += 1
        self.beep()

    def preAmp_off(self):
        for ch in self.preAmp_channels:
            self.LDI_setzero(ch)            # First ensure all diodes are set to zero current.
            time.sleep(self.sleeptime)                   # Wait a moment
            self.LAS_onoff(ch, 0)           # Now turn off LAS
            time.sleep(self.sleeptime)                   # Wait a moment
        self.beep()



# -----------------------------------------------------------
# Test class

#ilx = ILXcontrol()
#
# ilx.beep()
# ilx.LAS_onoff(8,1)
