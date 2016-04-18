#   Copyright (c) 2016, Xilinx, Inc.
#   All rights reserved.
# 
#   Redistribution and use in source and binary forms, with or without 
#   modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution.
#
#   3.  Neither the name of the copyright holder nor the names of its 
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION). HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__author__      = "Yun Rock Qu"
__copyright__   = "Copyright 2016, Xilinx"
__email__       = "xpp_support@xilinx.com"


from . import pmod_const
from .pmod_io import PMOD_IO

class PMOD_Cable(PMOD_IO):
    """This class can be used for a cable connecting PMOD interfaces.
    
    This class inherits from the PMODIO class.
    
    Note
    ----
    When 2 PMODs are connected using a cable, the parameter 'cable' decides 
    whether the cable is a 'loopback' or 'straight' cable.
    The default is a straight cable (no internal wire twisting).
    For pin mapping, please check the PMODIO class.
    
    Attributes
    ----------
    iop : _IOP
        The _IOP object returned from the DevMode.
    index : int
        The index of the PMOD pin, from 0 to 7.
    direction : str
        Input 'in' or output 'out'.
    cable : str
        Either 'straight' or 'loopback'.
    
    """
    def __init__(self, pmod_id, index, direction, cable): 
        """Return a new instance of a Cable object.
    
        Only the cable type is checked during initialization, since all the
        other parameters are checked by PMODIO class.
        
        Note
        ----
        The pmod_id 0 is reserved for XADC (JA).
        
        Parameters
        ----------
        pmod_id : int
            The PMOD ID (1, 2, 3, 4) corresponding to (JB, JC, JD, JE).
        index: int
            The index of the pin in a PMOD, from 0 to 7.
        direction : str
            Input 'in' or output 'out'.
        cable : str
            Either 'straight' or 'loopback'.
            
        """
        if (cable not in ['straight', 'loopback']):
            raise ValueError("Cable can only be 'straight', or 'loopback'.")
        
        super().__init__(pmod_id, index, direction)
        self.cable = cable
        
    def set_cable(self, cable):
        """Set the type for the cable.

        Note
        ----------
        The default cable type is 'straight'. Only straight cable or loop-back
        cable can be recognized.
       
        Parameters
        ----------
        cable : str
            Either 'straight' or 'loopback'.
            
        Returns
        -------
        None
        
        """
        if (cable not in ['straight', 'loopback']):
            raise ValueError("Cable can only be 'straight', or 'loopback'.")
        self.cable = cable

    def read(self):
        """Receive the value from the PMOD cable.
        
        This class overrides the read() method in the PMODIO class.
        
        Note
        ----
        Only use this function when direction = 'in'.
        
        When two PMODs are connected on the same board, for any received raw 
        value, a "straignt" cable flips the upper 4 pins and the lower 4 pins:
        A PMOD interface       <=>      Another PMOD interface
        {vdd,gnd,3,2,1,0}      <=>      {vdd,gnd,7,6,5,4}
        {vdd,gnd,7,6,5,4}      <=>      {vdd,gnd,3,2,1,0}
        
        A "loop-back" cable satisfies the following mapping 
        between two PMODs:
        A PMOD interface       <=>      Another PMOD interface
        {vdd,gnd,3,2,1,0}      <=>      {vdd,gnd,3,2,1,0}
        {vdd,gnd,7,6,5,4}      <=>      {vdd,gnd,7,6,5,4}
        
        Parameters
        ---------
        None
        
        Returns
        -------
        int
            The data (0 or 1) on the specified PMOD IO pin.
        
        """
        raw_value = self.iop.read_cmd(pmod_const.IOPMM_PMODIO_BASEADDR+
                                        pmod_const.IOPMM_PMODIO_DATA_OFFSET)
                                        
        if self.cable=='straight':
            if (self.index < 4):
                return (raw_value >> (self.index+4)) & 0x1
            else:
                return (raw_value >> (self.index-4)) & 0x1
        else:
                return (raw_value >> (self.index)) & 0x1