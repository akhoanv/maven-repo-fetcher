#!/usr/bin/python3

import sys
import requests
import os
import urllib.request
import argparse
from lxml import etree

"""
Maven central repository fetcher

(C) 2022 Khoa Nguyen (akhoa.nv@gmail.com)
Released under GNU Public License (GPL)
"""

MVN_REPO_URL = "https://repo1.maven.org/maven2/"

# Parsing args
parser = argparse.ArgumentParser(description='Fetching packages from Maven central repository')
parser.add_argument("dependencies", metavar='dependencies', type=str, nargs='+', help='Dependencies to fetch')
parser.add_argument('--javadoc', dest='javadoc', action='store_true', help='Fetch Javadoc if available')
parser.add_argument('--sources', dest='sources', action='store_true', help='Fetch Source files if available')
parser.add_argument('--tests', dest='tests', action='store_true', help='Fetch Tests if available')
parser.add_argument('--recursive', dest='recursive', action='store_true', help='Recursively fetching dependencies')


parser.set_defaults(javadoc=False)
parser.set_defaults(sources=False)
parser.set_defaults(tests=False)
parser.set_defaults(recursive=False)

args = parser.parse_args()

def parsePackage(packageString):
	depSplit = dep.split(":")
	
	return depSplit[0], depSplit[1], depSplit[2]

def parsePom(pomFile):
	root = etree.parse(pomFile).getroot()
	tree = etree.ElementTree(root)
	
	depend = tree.xpath("//*[local-name()='dependency']")

	for dep in depend:
		infoList = []
		for child in dep.getchildren():
			infoList.append(child.text)
		
		# Just in case package version isn't defined...
		if (len(infoList) < 3):
			infoList.append("none")

		fetchPackage(infoList[1], infoList[0], infoList[2])

def fetchPackage(name, package, version):
	print("Package -- Name: " + name + "\n\t\\_ Group: " + package + "\n\t\\_ Version: " + version + "\n")
	
	requestUrl = MVN_REPO_URL + package.replace(".", "/") + "/" + name + "/" + version
	getRqst = requests.get(requestUrl)
	
	if getRqst.status_code == 404:
		if (version.startswith("${") and version.endswith("}")):
			print("- Version was defined as environment variable and cannot be resolved")
		print("- Package not found!\n")
	elif getRqst.status_code == 200:
		print("- Package found!")

		# Create package directory
		os.makedirs("./" + package.replace(".", "/") + "/" + name + "/" + version, exist_ok = True)
		print("- Created directory at \"" + package.replace(".", "/") + "/" + name + "/" + version + "/\"")
		
		baseFileName = name + "-" + version
		
		# Binary file
		fileName = baseFileName + ".jar"
		if requests.get(requestUrl + "/" + fileName).status_code == 200:
			urllib.request.urlretrieve(requestUrl + "/" + fileName, "./" + package.replace(".", "/") + "/" + name + "/" + version + "/" + fileName)
			print("- Fetched " + fileName)
			
		fileName = baseFileName + ".aar"
		if requests.get(requestUrl + "/" + fileName).status_code == 200:
			urllib.request.urlretrieve(requestUrl + "/" + fileName, "./" + package.replace(".", "/") + "/" + name + "/" + version + "/" + fileName)
			print("- Fetched " + fileName)
			
		fileName = baseFileName + ".apk"
		if requests.get(requestUrl + "/" + fileName).status_code == 200:
			urllib.request.urlretrieve(requestUrl + "/" + fileName, "./" + package.replace(".", "/") + "/" + name + "/" + version + "/" + fileName)
			print("- Fetched " + fileName)
			
		# Extra files
		if (args.javadoc):
			fileName = baseFileName + "-javadoc.jar"
			if requests.get(requestUrl + "/" + fileName).status_code == 200:
				urllib.request.urlretrieve(requestUrl + "/" + fileName, "./" + package.replace(".", "/") + "/" + name + "/" + version + "/" + fileName)
				print("- Fetched " + fileName)

		if (args.sources):
			fileName = baseFileName + "-sources.jar"
			if requests.get(requestUrl + "/" + fileName).status_code == 200:
				urllib.request.urlretrieve(requestUrl + "/" + fileName, "./" + package.replace(".", "/") + "/" + name + "/" + version + "/" + fileName)
				print("- Fetched " + fileName)

		if (args.tests):
			fileName = baseFileName + "-tests.jar"
			if requests.get(requestUrl + "/" + fileName).status_code == 200:
				urllib.request.urlretrieve(requestUrl + "/" + fileName, "./" + package.replace(".", "/") + "/" + name + "/" + version + "/" + fileName)
				print("- Fetched " + fileName)
		
		# POM files	
		fileName = baseFileName + ".pom"
		urllib.request.urlretrieve(requestUrl + "/" + fileName, "./" + package.replace(".", "/") + "/" + name + "/" + version + "/" + fileName)
		print("- Fetched " + fileName + "\n")
		
		if (args.recursive):
			parsePom("./" + package.replace(".", "/") + "/" + name + "/" + version + "/" + fileName)

# Go through provided dependencies
deps = args.dependencies

for dep in deps:	
	package, name, version = parsePackage(dep)
	fetchPackage(name, package, version)