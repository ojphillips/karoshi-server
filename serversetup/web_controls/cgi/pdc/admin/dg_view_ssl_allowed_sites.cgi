#!/bin/bash
#Copyright (C) 2011 Paul Sharrad

#This file is part of Karoshi Server.
#
#Karoshi Server is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Karoshi Server is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with Karoshi Server.  If not, see <http://www.gnu.org/licenses/>.

#
#The Karoshi Team can be contacted at: 
#mpsharrad@karoshi.org.uk
#jsharrad@karoshi.org.uk

#
#Website: http://www.karoshi.org.uk
############################
#Language
############################

STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
TEXTDOMAIN=karoshi-server

#Check if timout should be disabled
if [ `echo $REMOTE_ADDR | grep -c $NOTIMEOUT` = 1 ]
then
TIMEOUT=86400
fi
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$"View SSL Allowed Sites"'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi">'
echo "<link rel="stylesheet" href="/css/$STYLESHEET">"
echo '<script>'
echo '<!--'
echo 'function SetAllCheckBoxes(FormName, FieldName, CheckValue)'
echo '{'
echo '	if(!document.forms[FormName])'
echo '		return;'
echo '	var objCheckBoxes = document.forms[FormName].elements[FieldName];'
echo '	if(!objCheckBoxes)'
echo '		return;'
echo '	var countCheckBoxes = objCheckBoxes.length;'
echo '	if(!countCheckBoxes)'
echo '		objCheckBoxes.checked = CheckValue;'
echo '	else'
echo '		// set the check value for all check boxes'
echo '		for(var i = 0; i < countCheckBoxes; i++)'
echo '			objCheckBoxes[i].checked = CheckValue;'
echo '}'
echo '// -->'
echo '</script><script src="/all/stuHover.js" type="text/javascript"></script>'
echo "</head><body><div id='pagecontainer'>"
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`
#########################
#Assign data to variables
#########################
END_POINT=6
#Assign ALPHABET
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = ALPHABETcheck ]
then
let COUNTER=$COUNTER+1
ALPHABET=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo '                window.location = "/cgi-bin/admin/dg_view_ssl_allowed_sites_fm.cgi";'
echo '</script>'
echo "</div></body></html>"
exit
}
#########################
#Check https access
#########################
if [ https_$HTTPS != https_on ]
then
export MESSAGE=$"You must choose a letter."
show_status
fi
#########################
#Check user accessing this script
#########################
if [ ! -f /opt/karoshi/web_controls/web_access_admin ] || [ $REMOTE_USER'null' = null ]
then
MESSAGE=$"You must be a Karoshi Management User to complete this action."
show_status
fi

if [ `grep -c ^$REMOTE_USER: /opt/karoshi/web_controls/web_access_admin` != 1 ]
then
MESSAGE=$"You must be a Karoshi Management User to complete this action."
show_status
fi
#########################
#Check data
#########################
#Check to see that ALPHABET is not blank
if [ $ALPHABET'null' = null ]
then
MESSAGE=$"You must choose a letter."
show_status
fi

#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
echo '<form action="/cgi-bin/admin/dg_view_ssl_allowed_sites2.cgi" name="selectedsites" method="post"><b></b><div id="actionbox3"><div id="titlebox"><b>'$"View SSL Allowed Sites"'</b><br><br></div><div id="infobox">'

Checksum=`sha256sum /var/www/cgi-bin_karoshi/admin/dg_view_ssl_allowed_sites.cgi | cut -d' ' -f1`
#Show sites
echo '<input class="button" value="Submit" type="submit">'
echo '<input class="button" value="Reset" type="reset">'
echo '<'input class='"'button'"' type='"'button'"' onclick='"'SetAllCheckBoxes'('"'"selectedsites"'", "'"_SITENAME_"'", true')'';''"' value='"'Select all'"''>'
sudo -H /opt/karoshi/web_controls/exec/dg_view_ssl_allowed_sites $REMOTE_USER:$REMOTE_ADDR:$Checksum:$ALPHABET:
SITESTATUS=`echo $?`
if [ $SITESTATUS = 101 ]
then
MESSAGE=$"No sites available."
show_status
fi
#echo "</div>"
#echo '<div id="submitbox">'
echo '<input value="'$"Submit"'" class="button" type="submit"> <input value="'$"Reset"'" class="button" type="reset"> '
echo '<'input class='"'button'"' type='"'button'"' onclick='"'SetAllCheckBoxes'('"'"selectedsites"'", "'"_SITENAME_"'", true')'';''"' value='"'Select all'"''>'
echo '</div></div></form></div></body></html>'
exit
