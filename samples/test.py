#!/usr/bin/python3
# Copyright (c) 2015 Mattia Setzu
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager

import os
import sys
import time

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

#PORTAFOGLIO A
walletA = WalletExplorer.WalletExplorer (wallet_file='test.walletA')
AMan = ForumManager.ForumManager (consMan, wallet=walletA)

#PORTAFOGLIO B
walletB = WalletExplorer.WalletExplorer (wallet_file='test.walletB')
BMan = ForumManager.ForumManager (consMan, wallet=walletB)

#Viene creato un nuovo post col metodo createPost ("","") dall'utente con portafoglio A.
#L'id viene memorizzato nella variabile postid.
try:
	postid=AMan.createPost ('Hello post', 'Post di test')
	print ('POST-A >', postid)
except:
	print ('Error')
time.sleep (5)


#Viene definita una funzione "listp1()". Si occupa di chiamare il metodo
#listPost() ogni 10 secondi, finchè non compare a video il post inviato precedentemente.
#Ad ogni chiamata di listPost () vengono stampati tutti i post disponibili.
def listp1():
	while True:
		os.system ('clear')
		print ('Lista dei post')
		v=AMan.listPost ()
		for x in v:
			try:
				print ('POST ->',x['hash'])
				if x['hash']==postid:
					return
			except:
				continue
		time.sleep (10)

#Viene chiamata la funzione dichiarata precedentemente.
listp1()
time.sleep (10)


#Viene creato un nuovo commento col metodo commentPost (postid,"") dall'utente con portafoglio A.
#L'id viene memorizzato nella variabile commid.
#Nella creazione del commento viene passato il postid del primo post, creato precedemente,
#per associare il commento a quel post.
try:
	commid=AMan.commentPost(postid, 'This is a comment')
	print ('COMMENT-A >', commid)
except:
	print ('Error')
time.sleep (5)


#Viene definita una funzione "getpostid1()". Si occupa di chiamare il metodo
#getPostInfo(postid) ogni 10 secondi, finchè non compare a video il post inviato inizialmente dall'utente A,
#con id postid, con commento allegato.
#Ad ogni chiamata di getpostid1 () viene stampato il post con id postid e il commento allegato se presente.
def getpostid1 ():
	while True:
		os.system ('clear')
		print ('Postid',)
		v=AMan.getPostInfo (postid)
		try:	
			if v['commid1']==commid:
				print ('POST(',v['hash'],')',v['title'],v['body'],'["',v['comment1'],'"]')
				return	
		except:
			print ('POST(',v['hash'],')',v['title'],v['body'])									
		time.sleep (10)

#Viene chiamata la funzione dichiarata precedentemente.
getpostid1()
time.sleep(10)


#Viene creato un nuovo post col metodo createPost ("","") dall'utente con portafoglio B.
#L'id viene memorizzato nella variabile postid2.
try:
	postid2=BMan.createPost ('Hello post 2', 'Post di test 2')
	print ('POST-B >', postid2)
except:
	print ('Error')
time.sleep (5)


#Viene creato un nuovo commento col metodo commentPost (postid,"") dall'utente con portafoglio B.
#L'id viene memorizzato nella variabile commid2.
#Nella creazione del commento viene passato il postid del primo post, creato precedemente, dall'utente A
#per associare il commento a quel post.
try:
	commid2=BMan.commentPost(postid, 'This is a comment of B')
	print ('COMMENT-B >', commid2)
except:
	print ('Error')
time.sleep (5)


#Viene definita una funzione "getpostid2()". Si occupa di chiamare il metodo
#getPostInfo(postid) ogni 10 secondi, finchè non compare a video il post inviato inizialmente dall'utente A,
#con id postid, con i 2 commenti allegati.
#Ad ogni chiamata di getpostid2 () viene stampato il post con id postid e i 2 commenti allegati se presenti.
def getpostid2 ():
	while True:
		os.system ('clear')
		print ('Postid',)
		v=BMan.getPostInfo (postid)
		try:	
			if v['commid2']==commid2:
				print ('POST(',v['hash'],')',v['title'],v['body'],'["',v['comment1'],'" "',v['comment2'],'"]')
				return	
		except:
			print ('POST(',v['hash'],')',v['title'],v['body'],'["',v['comment1'],'"]')									
		time.sleep (10)

#Viene chiamata la funzione dichiarata precedentemente.
getpostid2()


########################################################################################
######################################FINE TEST BASIC###################################
########################################################################################

########################################################################################
####################################INIZIO TEST ADVANCED################################
########################################################################################	

#Viene creato un nuovo sondaggio col metodo commentPoll ("","","") dall'utente con portafoglio A.
#L'id viene memorizzato nella variabile pollid.
#Nella creazione del sondaggio viene passato il titolo, le possibili risposte e la scadenza.
try:
	pollid=AMan.createPoll ('Title', ['primo', 'secondo', 'terzo'], 3600) #3600 secondi, 1 ora
	print ('SONDAGGIO-A >', pollid)
except:
	print ('Error')
time.sleep (5)


#Viene definita una funzione "listpoll()". Si occupa di chiamare il metodo
#listPolls() ogni 10 secondi, finchè non compare a video il sondaggio inviato precedentemente.
#Ad ogni chiamata di listPolls () vengono stampati tutti i sondaggi disponibili.
def listpoll():
	while True:
		os.system ('clear')
		print ('Lista dei sondaggi')
		v=AMan.listPolls ()
		for x in v:
			try:
				print ('SONDAGGIO-A >',x['hash'], x['title'], x['answer'])
				if x['hash']==pollid:
					return
			except:
				continue
		time.sleep (10)

#Viene chiamata la funzione dichiarata precedentemente.
listpoll()

