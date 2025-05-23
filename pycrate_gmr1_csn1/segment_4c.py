# -*- coding: UTF-8 -*-
#/**
# * Software Name : pycrate
# * Version : 0.4
# *
# * Copyright 2018. Benoit Michau. P1sec.
# *
# * This library is free software; you can redistribute it and/or
# * modify it under the terms of the GNU Lesser General Public
# * License as published by the Free Software Foundation; either
# * version 2.1 of the License, or (at your option) any later version.
# *
# * This library is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# * Lesser General Public License for more details.
# *
# * You should have received a copy of the GNU Lesser General Public
# * License along with this library; if not, write to the Free Software
# * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 
# * MA 02110-1301  USA
# *
# *--------------------------------------------------------
# * File Name : pycrate_gmr1_csn1/segment_4c.py
# * Created : 2023-10-24
# * Authors : Benoit Michau
# *--------------------------------------------------------
#*/
# specification: ETSI TS 101 376-04-08
# section: 11.5.2.87         Segment 4C
# top-level object: Segment 4C



# code automatically generated by pycrate_csn1
# change object type with type=CSN1T_BSTR (default type is CSN1T_UINT) in init
# add dict for value interpretation with dic={...} in CSN1Bit init
# add dict for key interpretation with kdic={...} in CSN1Alt init

from pycrate_csn1.csnobj import *

power_control_parameters = CSN1List(name='power_control_parameters', list=[
  CSN1Bit(name='hht_sqt', bit=7),
  CSN1Bit(name='hht_data_sqt', bit=7),
  CSN1Bit(name='vt_sqt', bit=7),
  CSN1Bit(name='vt_data_sqt', bit=7),
  CSN1Bit(name='ft_sqt', bit=7),
  CSN1Bit(name='ft_data_sqt', bit=7),
  CSN1Bit(name='paninit', bit=6),
  CSN1Bit(name='panmin', bit=6),
  CSN1Bit(name='panmax', bit=6),
  CSN1Bit(name='gainup', bit=5),
  CSN1Bit(name='gaindn', bit=5),
  CSN1Bit(name='olthresh', bit=5),
  CSN1Bit(name='olupgain', bit=5),
  CSN1Bit(name='oldngain', bit=5),
  CSN1Bit(name='varup', bit=5),
  CSN1Bit(name='vardn', bit=5),
  CSN1Bit(name='sqifactor', bit=5),
  CSN1Bit(name='mestep', bit=4),
  CSN1Bit(name='lqi_n1', bit=4),
  CSN1Bit(name='lqi_n2', bit=4)])

header_segment_4c = CSN1List(name='header_segment_4c', list=[
  CSN1Val(name='class_type_4', val='110'),
  CSN1Val(name='segment_type', val='0010')])

segment_4c = CSN1List(name='segment_4c', list=[
  CSN1Ref(obj=power_control_parameters),
  CSN1Bit(name='spare')])

