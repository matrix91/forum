# Copyright (c) 2015 Mattia Setzu
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from libcontractvm import Wallet, ConsensusManager, DappManager

#Nella classe ForumManager sono stati definiti i sei metodi della dapp forum
class ForumManager (DappManager.DappManager):
	def __init__ (self, consensusManager, wallet):
		super (ForumManager, self).__init__(consensusManager, wallet)

	def createPost (self, title, body):
		cid = self.produceTransaction ('forum.createPost', [title, body])
		return cid
	
	def createPoll (self, title, answer, deadline):
		cid = self.produceTransaction ('forum.createPoll', [title, answer, deadline])
		return cid

	def commentPost (self, postid, comment):
		cid = self.produceTransaction ('forum.commentPost', [postid, comment])
		return cid

	def listPost (self):
		return self.consensusManager.jsonConsensusCall ('forum.listPost', [])['result']

	def listPolls (self):
		return self.consensusManager.jsonConsensusCall ('forum.listPolls', [])['result']

	def getPostInfo (self, postid):
		return self.consensusManager.jsonConsensusCall ('forum.getPostInfo', [postid])['result']

	
