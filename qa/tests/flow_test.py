#!/usr/bin/env python
# encoding: utf-8
"""
flow.py

Created by Thomas Mangin on 2010-01-14.
Copyright (c) 2009-2015 Exa Networks. All rights reserved.
"""

import unittest

from exabgp.bgp.message.update.nlri import Flow
from exabgp.bgp.message.update.nlri.flow import Flow4Source
from exabgp.bgp.message.update.nlri.flow import Flow4Destination
from exabgp.bgp.message.update.nlri.flow import FlowAnyPort

from exabgp.bgp.message.update.nlri.flow import NumericOperator
# from exabgp.bgp.message.update.attribute.community import *

from exabgp.configuration.environment import environment
environment.setup('')


class TestFlow (unittest.TestCase):

	def setUp (self):
		pass

	def test_rule (self):
		components = {
			'destination': Flow4Destination("192.0.2.0",24),
			'source':      Flow4Source("10.1.2.0",24),
			'anyport_1':   FlowAnyPort(NumericOperator.EQ,25),
		}
		messages = {
			'destination': [0x01, 0x18, 0xc0, 0x00, 0x02],
			'source':      [0x02, 0x18, 0x0a, 0x01, 0x02],
			'anyport_1':   [0x04, 0x01, 0x19],
		}

		for key in ['destination','source','anyport_1']:
			component = components[key].pack()
			message   = ''.join((chr(_) for _ in messages[key]))
			# if component != message:
			# 	self.fail('content mismatch\n%s\n%s' % (['0x%02X' % ord(_) for _ in component],['0x%02X' % ord(_) for _ in message]))

	def test_rule_and (self):
		components = {
			'destination': Flow4Destination("192.0.2.0",24),
			'source':      Flow4Source("10.1.2.0",24),
			'anyport_1':   FlowAnyPort(NumericOperator.EQ | NumericOperator.GT,25),
			'anyport_2':   FlowAnyPort(NumericOperator.EQ | NumericOperator.LT,80),
		}
		messages = {
			'destination': [0x01, 0x18, 0xc0, 0x00, 0x02],
			'source':      [0x02, 0x18, 0x0a, 0x01, 0x02],
			'anyport_1':   [0x04, 0x43, 0x19],
			'anyport_2':   [0x04, 0x85, 0x50],
		}

		flow = Flow()
		message = ""
		for key in ['destination','source','anyport_1','anyport_2']:
			flow.add(components[key])
			message += ''.join([chr(_) for _ in messages[key]])
		message = chr(len(message)) + message
		# flow.add(to_FlowAction(65000,False,False))
		flow.pack()
		# print [hex(ord(_)) for _ in flow]

	def test_nlri (self):
		components = {
			'destination': Flow4Destination("192.0.2.0",24),
			'source':      Flow4Source("10.1.2.0",24),
			'anyport_1':   FlowAnyPort(NumericOperator.EQ | NumericOperator.GT,25),
			'anyport_2':   FlowAnyPort(NumericOperator.EQ | NumericOperator.LT,80),
		}
		messages = {
			'destination': [0x01, 0x18, 0xc0, 0x00, 0x02],
			'source':      [0x02, 0x18, 0x0a, 0x01, 0x02],
			'anyport_1':   [0x04, 0x43, 0x19],
			'anyport_2':   [0x85, 0x50],
		}

		flow = Flow()
		message = ""
		for key in ['destination','source','anyport_1','anyport_2']:
			flow.add(components[key])
			message += ''.join([chr(_) for _ in messages[key]])
		message = chr(len(message)) + message
		# policy.add(to_FlowAction(65000,False,False))
		flow = flow.pack()
		if message[0] != flow[0]:
			self.fail('size mismatch %s %s\n' % (ord(flow[0]),ord(message[0])))
		if len(flow) != ord(flow[0]) + 1:
			self.fail('invalid size for message')
		# if message[1:] != flow[1:]:
		# 	self.fail('content mismatch\n%s\n%s' % (['0x%02X' % ord(_) for _ in flow],['0x%02X' % ord(_) for _ in message]))

	def test_compare (self):
		components = {
			'destination': Flow4Destination("192.0.2.0",24),
			'source':      Flow4Source("10.1.2.0",24),
			'anyport_1':   FlowAnyPort(NumericOperator.EQ | NumericOperator.GT,25),
			'anyport_2':   FlowAnyPort(NumericOperator.EQ | NumericOperator.LT,80),
			'anyport_3':   FlowAnyPort(NumericOperator.EQ,80),
		}

		flow1 = Flow()
		for key in ['destination','source','anyport_1','anyport_2']:
			flow1.add(components[key])

		flow2 = Flow()
		for key in ['destination','source','anyport_3']:
			flow2.add(components[key])

		if flow1 != flow1:
			self.fail('the flows are the same')

		if flow1 == flow2:
			self.fail('the flows are not the same')

if __name__ == '__main__':
	unittest.main()
