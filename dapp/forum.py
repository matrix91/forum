# Copyright (c) 2015 Mattia Setzu
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import time

from contractvmd import dapp, config, proto
from contractvmd.chain import message

logger = logging.getLogger(config.APP_NAME)


#Nel protocollo è stato scelto come DAPP_CODE 0x58, 0x60.
#Poi sono state dichiarate le 3 costanti METHOD_MES, METHOD_COM e METHODO_POL, che indicano i 3 metodi della dapp e
#in METHOD_LIST sono stati inseriti i 3 metodi.
class ForumProto:
	DAPP_CODE = [ 0x58, 0x60 ]
	METHOD_MES = 0x00
	METHOD_COM = 0x01
	METHOD_POL = 0x03
	METHOD_LIST = [METHOD_MES, METHOD_COM, METHOD_POL]

	
#Nella classe ForumMessage sono stati definiti i metodi createPost, commentPost e createPoll. Si occupano di creare i vari oggetti
#ForumMessage.
class ForumMessage (message.Message):
	def createPost (title, body):
		m = ForumMessage ()
		m.Title = title
		m.Body = body
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_MES
		return m

	def commentPost (postid, comment):
		m = ForumMessage ()
		m.Postid = postid
		m.Comment = comment
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_COM
		return m
	
	def createPoll (title, answer, deadline):
		m = ForumMessage ()
		m.Title = title
		m.Answer = answer
		m.Deadline = deadline
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_POL
		return m

	def toJSON (self):
		data = super (ForumMessage, self).toJSON ()

		if self.Method == ForumProto.METHOD_MES:
			data['title'] = self.Title
			data['body'] = self.Body
		elif self.Method == ForumProto.METHOD_COM:
			data['postid'] = self.Postid
			data['comment'] = self.Comment
		elif self.Method == ForumProto.METHOD_POL:
			data['title'] = self.Title
			data['answer'] = self.Answer
			data['deadline'] = self.Deadline
		
		else:
			return None

		return data


#Nella classe ForumCore sono stati creati i 3 metodi createPost, commentPost e createPoll che si occupano di memorizzare i
#dati e i metodi listPost, getPostInfo e listPolls che effettuano le query al database per recuperare le informazioni
class ForumCore (dapp.Core):
	def __init__ (self, chain, database):
		super (ForumCore, self).__init__ (chain, database)
		database.init ('participants', [])
		database.init ('comments', [])
		database.init ('polls', [])		
		
	#Metodo createPost: crea un post salvando tutto nel database con chiave participants
	def createPost (self, player, hashs, title, body):
		self.database.listappend ('participants', {'player': player, 'hash': hashs, 'title': title, 'body': body})

	#Metodo createPoll: crea un sondaggio salvando tutto nel database con chiave polls, la deadline viene calcolata con timestamp di unix
	def createPoll (self, player, hashs, title, answer, deadline):
		temp = int(time.time()) + int(deadline)
		self.database.listappend ('polls', {'player': player, 'hash': hashs, 'title': title, 'answer': answer, 'deadline': temp})

	#Metodo commentPost: crea un commento salvando tutto nel database con chiave comments
	def commentPost (self, player, hashs, postid, comment):
		self.database.listappend ('comments', {'player': player, 'hash': hashs, 'postid': postid, 'comment': comment})
		
	#Metodo listPost: Restituisce la lista di tutti i post presenti in participants
	def listPost (self):
		return self.database.get ('participants')

	#Metodo listPolls: Restituisce la lista di tutti i sondaggi presenti in polls
	def listPolls (self):
		return self.database.get ('polls')
	
	#Metodo getPostInfo(postid): Restituisce il post col postid del parametro, con i relativi commenti.
	#Se il post non è presente restituisce una stringa di errore. 
	def getPostInfo (self, postid):
		a = self.database.get ('participants')
		b = self.database.get ('comments')
		
		for x in a:
			number=0
			try: #Nessun post presente sul database participants
				if x['hash'] == postid:
					lis = x
					for v in b:
						try: #Nessun commento presente nel database comments
							if v['postid'] == postid:
								number += 1
								lis['commid' + str(number)] = v['hash']
								lis['comment' + str(number)] = v['comment']
							else:
								continue
						except: #Ritorna il post senza commenti
							return lis
					return lis #Ritorna il post con o senza commenti
				else:
					continue
			except: #Non è presente nessun post sul database
				return "ATTENZIONE: Post ("+ postid +") non presente."
		
		return "ATTENZIONE: Post ("+ postid +") non presente." #Se il post non è presente ritorna questa stringa		



#Nella classe ForumAPI, sono stati inseriti i 6 metodi, 4 per la parte basic e 2 per la avanzata
class ForumAPI (dapp.API):
	def __init__ (self, core, dht, api):
		self.api = api
		rpcmethods = {}

		rpcmethods["listPost"] = {
			"call": self.method_listPost,
			"help": {"args": [], "return": {}}
		}

		rpcmethods["listPolls"] = {
			"call": self.method_listPolls,
			"help": {"args": [], "return": {}}
		}

		rpcmethods["getPostInfo"] = {
			"call": self.method_getPostInfo,
			"help": {"args": ["postid"], "return": {}}
		}

		rpcmethods["createPost"] = {
			"call": self.method_createPost,
			"help": {"args": ["title", "body"], "return": {}}
		}
	
		rpcmethods["createPoll"] = {
			"call": self.method_createPoll,
			"help": {"args": ["title", "answer", "deadline"], "return": {}}
		}

		rpcmethods["commentPost"] = {
			"call": self.method_commentPost,
			"help": {"args": ["postid", "comment"], "return": {}}
		}

		errors = { }

		super (ForumAPI, self).__init__(core, dht, rpcmethods, errors)


	def method_listPost (self):
		return self.core.listPost ()

	def method_listPolls (self):
		return self.core.listPolls ()

	def method_getPostInfo (self, postid):
		return self.core.getPostInfo (postid)

	def method_createPost (self, title, body):
		msg = ForumMessage.createPost ( title, body)
		return self.createTransactionResponse (msg)

	def method_createPoll (self, title, answer, deadline):
		msg = ForumMessage.createPoll ( title, answer, deadline)
		return self.createTransactionResponse (msg)

	def method_commentPost (self, postid, comment):
		msg = ForumMessage.commentPost ( postid, comment)
		return self.createTransactionResponse (msg)
		

#Nella classe forum è stato definito il metodo handleMessage(m) che stampa dei messaggi log quando arrivano i messaggi al client
class forum (dapp.Dapp):
	def __init__ (self, chain, db, dht, apiMaster):
		self.core = ForumCore (chain, db)
		apiprov = ForumAPI (self.core, dht, apiMaster)
		super (forum, self).__init__(ForumProto.DAPP_CODE, ForumProto.METHOD_LIST, chain, db, dht, apiprov)

	def handleMessage (self, m):
		if m.Method == ForumProto.METHOD_MES:
			logger.pluginfo ('Found new message %s from %s', m.Hash, m.Player)
			self.core.createPost (m.Player, m.Hash, m.Data['title'], m.Data['body'])	
		if m.Method == ForumProto.METHOD_COM:
			logger.pluginfo ('Found new comment %s from %s', m.Hash, m.Player)
			self.core.commentPost (m.Player ,m.Hash, m.Data['postid'], m.Data['comment'])
		if m.Method == ForumProto.METHOD_POL:
			logger.pluginfo ('Found new poll %s from %s', m.Hash, m.Player)
			self.core.createPoll (m.Player, m.Hash, m.Data['title'], m.Data['answer'], m.Data['deadline'])				