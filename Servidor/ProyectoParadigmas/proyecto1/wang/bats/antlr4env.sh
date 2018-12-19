#!/bin/bash -ex
# loriacarlos@gmail.com
# EIF400 II-2018

# echo off
{ set +v; } 2>/dev/null
#
export GRAMMAR_NAME=Wang.g4 
export SOURCE=./src
export GRAMMAR_PATH=./grammar
export GRAMMAR=$GRAMMAR_PATH/$GRAMMAR_NAME
export PARSER=./parser


echo "*** Setting Environment and Variables for ANTLR4-Python ***"
export ANTLR_JAR=/Users/jmiranda/antlr/antlr-4.7.1-complete.jar
export CLASSPATH=$ANTLR_JAR

export PYTHONPATH=$PARSER/grammar:$SOURCE:$PYTHONPATH
# Antlr4 the tool
alias antlr4="java -cp $CLASSPATH org.antlr.v4.Tool $*"

# antlr4 generator for python3 yielding visitor 
export JAVA_CMD="java -cp $CLASSPATH org.antlr.v4.Tool -Dlanguage=Python3" 
export JAVA_CMD_VISITOR="$JAVA_CMD -no-listener -visitor -o parser $*"

alias antlr4p3="$JAVA_CMD_VISITOR" 
alias build_parser="$JAVA_CMD_VISITOR -o $PARSER $GRAMMAR"
echo VARIABLES
echo "*** grammar_path=$GRAMMAR ***"
echo "*** parser_path=$PARSER ***"
echo "*** classpath=$CLASSPATH ***"
echo "*** pythonpath=$PYTHONPATH ***"
echo COMMANDS
echo "*** Use 'antlr4' for calling directly to antlr4"
echo "*** Use 'antlr4p3' for generating parsers for python3 target ***"
echo "*** Use 'build_parser' for generating parser from $GRAMMAR into $PARSER ***"

echo ALIASES
alias