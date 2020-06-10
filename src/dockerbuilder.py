#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import os.path
import sys
import subprocess
from os import path
from time import sleep
#5 no M makes the text blink
clear = lambda: os.system('clear')
green = "\033[1;32;2m"
greenblink = "\033[1;32;5m"
yellow = "\033[1;33;2m"
yellowblink = "\033[1;33;5m"
redblink = "\033[1;31;5m"
red = "\033[1;31;2m"
white = "\033[1;37;0m"
normal = "\033[0m"

def isset(variable):
	is_set = variable in globals() or variable in locals()
	return is_set

def main():
	global choice, projecturl, tags, registry_url, wpath
	param = sys.argv[1]
	if(param=="help" or param=="h" or param=="-h" or param=="--help"):
		help()
		sys.exit()
		

	clear()
	# path = os.system("realpath "+sys.argv[1])
	if not isset("wpath"):
		wpath = subprocess.check_output(['realpath', param])
		wpath = wpath.rstrip("\n")

	if (isset("choice") and (choice=="y" or choice=="Y")):
		registryok(0)
	print (normal+"=========================================================================")
	print ("                  Aqui é DockerBuilder P****a!                           ")
	print (" Script by AndersonPEM (https://github.com/andersonpem)")
	print ("")
	print (" It's about to happen! :)")
	print (green+" Working Directory: \n "+wpath+normal)
	print ("=========================================================================")
	if not path.exists(wpath+"/Dockerfile"):
		print (redblink+" I couldn't find a Dockerfile in this directory :( "+normal)
		print (" You can give a ctrl+c in this script and start it again in the proper")
		print (" working directory with your dockerfile or Specify a path below.")
		wpath = raw_input(yellow+" Path to the place with your Dockerfile: "+normal)
		main()
	else:
		print (green+" Dockerfile was found."+normal)
		print (" Have you signed into the Registry you want to publish this image on")
		choice = raw_input(" already (y/n): ")
	if (choice=="y" or choice=="Y"):
		registryok(999)
	else:		
		registry_url = raw_input(green+" OK. No panic. Give me the registry URL (defaults to registry.gitlab.com)\n"+normal+" Registry URL: [or enter to default]: ")
		if(registry_url==""):
			registry_url="registry.gitlab.com"
		attemptregistry()
	

def attemptregistry():
	global  projecturl, tags, registry_url, wpath
	print (yellow+" Requesting the 'docker login' utility..."+normal)
	login = os.system("docker login "+registry_url)
	if(login==0):
		registryok(login)
	else:
		clear()
		print ("=========================================================================")
		print ("                            Error :(                                   ")
		print "========================================================================="
		print(red+" It seems something happened. Have you typed proper login credentials?"+normal)
		choice = raw_input("Wanna try again? (y/n): ")
		if(choice=="y" or choice=="Y"):
			attemptregistry()
		else:
			print(yellow+"Exiting. Bye.");
			sys.exit()

def registryok(value):
	global projecturl, tags, registry_url, login, wpath
	clear()
	print "========================================================================="
	print "                          Dockerbuilder                          "
	print green+" Working Directory: \n "+wpath+normal
	print "========================================================================="
	if(value==0):
		print(green+" It seems your credentials were accepted."+normal)
	if (value==999):
		print(yellow+" Credential checking was skipped."+normal)

	projecturl = raw_input(" What's the Registry's image URL? [ex: registry.gitlab.com/user/project]\n URL: ")
	projectUrlOk()
	
def projectUrlOk():
	global projecturl, tags, wpath, arrTags, choice
	clear()
	print "========================================================================="
	print "                          Dockerbuilder                          "
	print green+" Working Directory: \n "+wpath+normal
	print(green+" Building image:\n"+yellow+" "+projecturl+normal)
	if(isset("tags")):
		print " Tags: "+tags
	print "========================================================================="
	if(not isset("tags") or (tags=="")):
		print (" Please provide the tags you want to publish separaded ")
		print (" by comma (ex: 1.0.0,latest)")
		tags = raw_input(" Tags: ")
		if(tags<>""):
			arrTags = tags.split(',')
			print(str(arrTags))
			projectUrlOk()

	else:
		print yellow+" We're ready to roll. What do we wanna do?"+normal
		print "========================================================================="
		print " 1 - Build and push the image with selected tags"
		print " 2 - Build and push the image with selected tags (no cache)"
		print " 3 - Change which tags to use"
		print " 4 - Start all over again"
		print " 5 - Quit"
		c = raw_input(" Your choice: ")
		if (c=="1"):
			print "========================================================================="
			print yellow+"Build stage..."+normal
			print "========================================================================="
			for x in arrTags:
				print yellow+" Executing: [docker build -t "+projecturl+":"+x+" "+wpath+"]..."+normal
				build = os.system("docker build -t "+projecturl+":"+x+" "+wpath)
				if(build==0):
					print green+" It seems the build went smoothly."+normal
				else:
					buildfail()
			print "========================================================================="
			print yellow+"Publishing stage..."+normal
			print "========================================================================="
			for x in arrTags:
				print yellow+" Executing: [docker push -t "+projecturl+":"+x+"]..."+normal
				build = os.system("docker push "+projecturl+":"+x)
				if(build==0):
					print green+" It seems the push went smoothly."+normal
				else:
					pushfail()
			print "========================================================================="			
			print greenblink+"Everything went according to plan. Have a nice cup of coffee :)"+normal
			sleep(5)
			projectUrlOk()

		elif (c=="2"):
			print "========================================================================="
			print yellow+"[no cache] Build stage..."+normal
			print "========================================================================="
			for x in arrTags:
				print yellow+" Executing: [docker build --no-cache -t "+projecturl+":"+x+" "+wpath+"]..."+normal
				build = os.system("docker build --no-cache  -t "+projecturl+":"+x+" "+wpath)
				if(build==0):
					print green+" It seems the build went smoothly."+normal
				else:
					buildfail()
			print "========================================================================="
			print yellow+"Publishing stage..."+normal
			print "========================================================================="
			for x in arrTags:
				print yellow+" Executing: [docker push -t "+projecturl+":"+x+"]..."+normal
				build = os.system("docker push "+projecturl+":"+x)
				if(build==0):
					print green+" It seems the push went smoothly."+normal
				else:
					pushfail()
			print "========================================================================="			
			print greenblink+"Everything went according to plan. Have a nice cup of coffee :)"+normal
			sleep(5)
			projectUrlOk()
		elif (c=="3"):
			del tags
			projectUrlOk()
		elif (c=="4"):
			del projecturl, tags, arrTags,choice
			main()
		elif (c=="5"):
			print yellow+" Ok. See you again soon! Bye!"+normal
			sys.exit()



def buildfail():
	print red+" It looks like the build has failed. Aborting. Please press enter.\n[Enter]"
	s = raw_input("")
	projectUrlOk()

def pushfail():
	print red+" It looks like the push has failed. Aborting. Please press enter.\n[Enter]"
	s = raw_input("")
	projectUrlOk()

def help():
	print green+"Dockerbuilder (dbd) - Developer by andersonpem (https://github.com/andersonpem/dockerbuilder)"+normal
	print "A small python utility to automate the proccess of building and pushing images to Registries"
	print "Why? I'm still to implement CI/CD in my workplace and manually inputting everything every time is tiresome."
	print yellow+"\nHow to use: \n"
	print "dbd "+green+"<path or .> -r=<[optional] URL of the Registry> -iurl=<[optional]> -tags=<[optional]> -y -ol -nc"+normal
	print "I recommend using all the parameters if you're using the optional ones. I haven't configured the script to check for specific ones yet. Except the last one."
	print yellow+"\npath"+normal+" is the folder where the Dockerfile is located at."
	print yellow+"-r"+normal+" is the registry's URL, like registry.gitlab.com. It's optional."
	print yellow+"-iurl"+normal+" The target image URL (example: registry.gitlab.com/user/project)"
	print yellow+"-tags"+normal+" are the desired tags to publish separated by commas with no spaces ex: -tags=1.0.0,stable"
	print yellow+"-y"+normal+" you confirm that you're already logged into the registry"
	print yellow+"-ol"+normal+" One liner. You wanna do everything without confirmation."
	print yellow+"-nc"+normal+" Build images with no cache."
	sys.exit()


main()
