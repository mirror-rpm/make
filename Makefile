# Makefile for source rpm: make
# $Id$
NAME := make
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
